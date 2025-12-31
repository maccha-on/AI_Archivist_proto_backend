"""
PDFフォルダ内のファイルを読み込み、
文章を分割 → Embedding → FAISSへ登録する
"""

import os
from analyzer.file_loader import load_pdf
from analyzer.text_splitter import split_text_with_overlap
from analyzer.embedder import get_embedding
from analyzer.index_manager import add_vector, index


def analyze_files(dir: str):
    # PDFフォルダ内のPDF一覧を取得
    pdf_paths = [
        os.path.join(dir, f)
        for f in os.listdir(dir)
        if f.lower().endswith(".pdf")
    ]

    # 各PDFを処理
    for pdf_path in pdf_paths:
        doc_id = os.path.basename(pdf_path).split(".")[0]

        # PDF → ページ単位で読み込み
        pages = load_pdf(pdf_path)

        for page in pages:
            # ページ文章をチャンク分割
            chunks = split_text_with_overlap(page["text"])

            for i, chunk in enumerate(chunks):
                # チャンクをEmbedding
                embedding = get_embedding(chunk)

                # FAISSへ登録
                add_vector(
                    embedding,
                    {
                        "doc_id": doc_id,
                        "page": page["page"],
                        "chunk_id": i,
                        "text": chunk,
                    },
                )

    # 登録結果を表示
    print(f"FAISS登録済みベクトル数: {index.ntotal}")







# =========== 以下、25年12月 当初の内容（消してOK）============
#
#
# def process_pdf(file_path: str, storage_path: str) -> DocumentProcessResult:
#     """
#     1つの PDF を処理するためのメイン関数です。

#     この関数がやること：
#       1. PDF からテキスト・メタデータを取り出す（バックエンドA）
#       2. 文書メタ情報を DB に保存して document_id を発行（バックエンドC）
#       3. チャンクごとにベクトル（embedding）を作る（バックエンドB）
#       4. ベクトル付きチャンクを DB に保存（バックエンドC）
#       5. 文書の処理ステータスを完了状態にする

#     ★ この関数は「処理の流れ」をわかりやすく書くことが最重要です。
#     """
#     document_id = None  # エラーが起きた時でも参照できるように最初に None をセット

#     try:
#         # -------------------------------------------------------
#         # ① PDF を解析して、文書情報 & チャンク化されたテキストを得る
#         # -------------------------------------------------------
#         # extract_from_pdf の戻り値は以下の2つ：
#         #   - DocumentMeta（文書のメタ情報）
#         #   - list[Chunk]   （チャンクごとのテキスト）
#         doc_meta, chunks = extract_from_pdf(file_path)

#         # -------------------------------------------------------
#         # ② 文書メタ情報を DB に保存して document_id を発行
#         # -------------------------------------------------------
#         # 注意：storage_path は、実際の PDF ファイルが保存されている場所。
#         document_id = create_document_record(doc_meta, storage_path)

#         # ステータスを「処理中」に変更
#         update_document_status(document_id, "processing")

#         # -------------------------------------------------------
#         # ③ 各チャンクに対して“意味ベクトル”を作る（embedding）
#         # -------------------------------------------------------
#         # embed_chunks の戻り値は list[EmbeddedChunk]。
#         embedded_chunks = embed_chunks(chunks)

#         # -------------------------------------------------------
#         # ④ ベクトル付きチャンクを DB に保存
#         # -------------------------------------------------------
#         chunks_saved = save_document_chunks(document_id, embedded_chunks)

#         # -------------------------------------------------------
#                # ⑤ 文書を「処理完了」に更新
#         # -------------------------------------------------------
#         update_document_status(document_id, "completed")

#         # -------------------------------------------------------
#         # ⑥ 最終結果を返す
#         # -------------------------------------------------------
#         return DocumentProcessResult(
#             document_id=document_id,
#             chunks_saved=chunks_saved,
#         )

#     except Exception as e:
#         # エラー時の処理
#         if document_id is not None:
#             # 失敗したことをDBに記録しておくと、あとで状況が確認しやすい
#             update_document_status(document_id, "failed", error_message=str(e))

#         print(f"[ERROR] 予期しないエラーが発生しました: {e}")

#         # エラーを上位に投げて、FastAPI や CLI 側で処理してもらう
#         raise

