"""
RDB（関係データベース）向けの永続化処理（ダミー実装）

このファイルは `persistence.py` から分割したものです。
Document のレコード作成やステータス更新など、RDB に関係する処理をここに置きます。
"""

from app.core_types import DocumentMeta


def create_document_record(meta: DocumentMeta, storage_path: str) -> int:
    """
    文書（documents）のレコードを作成するダミー関数（RDB担当）。
    戻り値は擬似的な document_id を返します。
    """

    print("\n[RDB-DUMMY] 文書レコードを作成します:")
    print(f"  original_filename: {meta.original_filename}")
    print(f"  mime_type        : {meta.mime_type}")
    print(f"  page_count       : {meta.page_count}")
    print(f"  tags             : {meta.tags}")
    print(f"  storage_path     : {storage_path}")

    fake_document_id = 1
    print(f"[RDB-DUMMY] 返却 document_id = {fake_document_id}")

    return fake_document_id


def update_document_status(document_id: int, status: str, error_message: str | None = None) -> None:
    """
    文書のステータスを更新するダミー関数（RDB担当）。
    """

    print("\n[RDB-DUMMY] ステータス更新:")
    print(f"  document_id = {document_id}")
    print(f"  status      = {status}")

    if error_message:
        print(f"  error_message = {error_message}")
