"""
backend_persistence.py（ダミー版・初心者向け）

このファイルは本来、
  ・documents テーブルの作成
  ・document_chunks テーブルへの保存
  ・ステータス管理（uploaded → processing → completed など）
を行う「データベースとのやり取り担当」です。

ですが、MVPの最初の段階では「まずは処理の流れを完成させること」が大切なので、
ここでは DB 処理の代わりに *print（画面への出力）だけ* を行うダミー版として作っています。

本番で PostgreSQL / Supabase / MySQL などに接続するときは、
この中身を差し替えるだけでOKです。
"""

from core_types import DocumentMeta, EmbeddedChunk


# ---------------------------------------------------------------
# ① 文書のレコードを作成する関数（ダミー版）
# ---------------------------------------------------------------

def create_document_record(meta: DocumentMeta, storage_path: str) -> int:
    """
    文書（documents）のレコードを作成するダミー関数。

    本来は DB に INSERT を実行して document_id を生成しますが、
    ダミー版では print して “作ったことにする” だけです。

    戻り値：
        擬似的な document_id（今回は 1 で固定）
    """

    print("\n[DB-DUMMY] 文書レコードを作成します:")
    print(f"  original_filename: {meta.original_filename}")
    print(f"  mime_type        : {meta.mime_type}")
    print(f"  page_count       : {meta.page_count}")
    print(f"  tags             : {meta.tags}")
    print(f"  storage_path     : {storage_path}")

    # 本来は DB から「自動採番されたID」を返すが、
    # ダミーでは 1 を返しておく（連番の代わりとして）
    fake_document_id = 1
    print(f"[DB-DUMMY] 返却 document_id = {fake_document_id}")

    return fake_document_id



# ---------------------------------------------------------------
# ② チャンクを保存する関数（ダミー版）
# ---------------------------------------------------------------

def save_document_chunks(document_id: int, chunks: list[EmbeddedChunk]) -> int:
    """
    embedding が付いたチャンクを保存するダミー関数。

    実際には document_chunks テーブルに INSERT を行いますが、
    ダミー版では内容を print するだけにしています。

    戻り値：
        保存したチャンク数（len(chunks)）
    """

    print("\n[DB-DUMMY] チャンクを保存します:")
    print(f"  document_id = {document_id}")
    print("  --- チャンク一覧 ---")

    for ch in chunks:
        print(f"   - chunk_index : {ch.chunk_index}")
        print(f"     text        : {ch.text[:20]}...")  # 長すぎるテキストは短く表示
        print(f"     metadata    : {ch.metadata}")
        print(f"     embedding(サイズ): {len(ch.embedding)} 次元")
        print("")

    print(f"[DB-DUMMY] チャンク保存完了（{len(chunks)} 件）")

    return len(chunks)



# ---------------------------------------------------------------
# ③ ステータス更新関数（ダミー版）
# ---------------------------------------------------------------

def update_document_status(document_id: int, status: str, error_message: str | None = None) -> None:
    """
    文書のステータス（uploaded / processing / completed / failed）
    を更新するダミー関数。

    本来は DB 側の `documents.status` を UPDATE しますが、
    ダミー版では print して雰囲気だけつかむようにしています。
    """

    print("\n[DB-DUMMY] ステータス更新:")
    print(f"  document_id = {document_id}")
    print(f"  status      = {status}")

    if error_message:
        print(f"  error_message = {error_message}")
