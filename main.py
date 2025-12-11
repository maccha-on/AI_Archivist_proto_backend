"""
main.py

このファイルは、バックエンドA/B/Cを「順番に」呼び出す
オーケストレーター（司令塔）としての役割を持ちます。

・A: PDFからテキスト＆メタデータ抽出
・B: 抽出したチャンクをベクトル化（embedding）
・C: DBに保存して、処理ステータスを更新


※ まだ実際のPDF処理やDB処理の中身は空（NotImplemented）の想定です。
  まずは「流れを理解する」ことを最優先にしています。
"""


from __future__ import annotations  # 型ヒントをシンプルに書けるようにするための 魔法 のようなもの
import sys                         # コマンドライン引数（python main.py sample.pdf）を扱うため
from pathlib import Path            # ファイルの存在確認や名前取得を簡単にするための標準ライブラリ

# core_types.py に定義してある、処理結果をまとめるためのクラス
from core_types import DocumentProcessResult


# 3つのバックエンド（A：抽出、B：ベクトル化、C：保存）を import
# ※ これらの関数の中身は後で実装します。
from backend_extractor import extract_from_pdf
from backend_embedder import embed_chunks
from backend_persistence import (
    create_document_record,
    save_document_chunks,
    update_document_status,
)

def process_pdf(file_path: str, storage_path: str) -> DocumentProcessResult:
    """
    1つの PDF を処理するためのメイン関数です。

    この関数がやること：
      1. PDF からテキスト・メタデータを取り出す（バックエンドA）
      2. 文書メタ情報を DB に保存して document_id を発行（バックエンドC）
      3. チャンクごとにベクトル（embedding）を作る（バックエンドB）
      4. ベクトル付きチャンクを DB に保存（バックエンドC）
      5. 文書の処理ステータスを完了状態にする

    ★ この関数は「処理の流れ」をわかりやすく書くことが最重要です。
    """
    document_id = None  # エラーが起きた時でも参照できるように最初に None をセット

    try:
        # -------------------------------------------------------
        # ① PDF を解析して、文書情報 & チャンク化されたテキストを得る
        # -------------------------------------------------------
        # extract_from_pdf の戻り値は以下の2つ：
        #   - DocumentMeta（文書のメタ情報）
        #   - list[Chunk]   （チャンクごとのテキスト）
        doc_meta, chunks = extract_from_pdf(file_path)

        # -------------------------------------------------------
        # ② 文書メタ情報を DB に保存して document_id を発行
        # -------------------------------------------------------
        # 注意：storage_path は、実際の PDF ファイルが保存されている場所。
        document_id = create_document_record(doc_meta, storage_path)

        # ステータスを「処理中」に変更
        update_document_status(document_id, "processing")

        # -------------------------------------------------------
        # ③ 各チャンクに対して“意味ベクトル”を作る（embedding）
        # -------------------------------------------------------
        # embed_chunks の戻り値は list[EmbeddedChunk]。
        embedded_chunks = embed_chunks(chunks)

        # -------------------------------------------------------
        # ④ ベクトル付きチャンクを DB に保存
        # -------------------------------------------------------
        chunks_saved = save_document_chunks(document_id, embedded_chunks)

        # -------------------------------------------------------
               # ⑤ 文書を「処理完了」に更新
        # -------------------------------------------------------
        update_document_status(document_id, "completed")

        # -------------------------------------------------------
        # ⑥ 最終結果を返す
        # -------------------------------------------------------
        return DocumentProcessResult(
            document_id=document_id,
            chunks_saved=chunks_saved,
        )

    except Exception as e:
        # エラー時の処理
        if document_id is not None:
            # 失敗したことをDBに記録しておくと、あとで状況が確認しやすい
            update_document_status(document_id, "failed", error_message=str(e))

        print(f"[ERROR] 予期しないエラーが発生しました: {e}")

        # エラーを上位に投げて、FastAPI や CLI 側で処理してもらう
        raise


def main():
    """
    コマンドラインから実行する時の入り口です。

    例：python main.py ./samples/sample.pdf

    初級者でも手軽に「処理の流れを試せるように」わかりやすい構成にしています。
    """
    if len(sys.argv) < 2:
        print("使い方: python main.py <PDFファイルパス>")
        sys.exit(1)

    # ユーザーが入力した PDF のパス
    pdf_path_str = sys.argv[1]
    pdf_path = Path(pdf_path_str)

    if not pdf_path.exists():
        print(f"[ERROR] ファイルが見つかりません: {pdf_path}")
        sys.exit(1)

    # storage_path は「PDF が保存される場所」を表す文字列。
    # MVP ではシンプルに “documents/<ファイル名>” としておけばOKです。
    storage_path = f"documents/{pdf_path.name}"

    print(f"[INFO] PDF処理を開始します: {pdf_path}")
    print(f"[INFO] 保存先パス (storage_path): {storage_path}")

    result = process_pdf(str(pdf_path), storage_path)

    print("[INFO] 処理が完了しました！")
    print(f"  document_id:  {result.document_id}")
    print(f"  chunks_saved: {result.chunks_saved}")


# Python ファイルを直接実行した時だけ main() を動かすおまじない
# 実行例: python main.py sample.pdf
if __name__ == "__main__":
    main()