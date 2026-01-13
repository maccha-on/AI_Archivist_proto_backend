# app/db/crud.py

# =================== CRUD 利用例 ===================
# from app.db.connect_MySQL import SessionLocal
# from app.db.crud import insert_document

# db = SessionLocal()
# doc = insert_document(db, {
#     "original_filename": "sample.pdf",
#     "local_path": "data/pdfs/sample.pdf",
#     "status": "processing",
#     "is_latest": True,
# })
# db.close()


from __future__ import annotations

from typing import Any, Optional, Sequence
from sqlalchemy.orm import Session
from sqlalchemy import select, update

from app.db.mymodels_MySQL import Document


# --- Create ---
def insert_document(db: Session, data: dict[str, Any]) -> Document:
    """
    documents に1件追加
    data: Documentのカラム名に一致するdict（余計なキーは入れない）
    """
    doc = Document(**data)
    db.add(doc)
    db.commit()
    db.refresh(doc)
    return doc


# --- Read ---
def get_document(db: Session, doc_id: int) -> Optional[Document]:
    return db.get(Document, doc_id)


def list_documents(db: Session, status: Optional[str] = None, limit: int = 50) -> Sequence[Document]:
    stmt = select(Document).order_by(Document.id.desc()).limit(limit)
    if status:
        stmt = select(Document).where(Document.status == status).order_by(Document.id.desc()).limit(limit)
    return db.execute(stmt).scalars().all()


# --- Update ---
def update_document(db: Session, doc_id: int, patch: dict[str, Any]) -> Optional[Document]:
    """
    doc_id のレコードを部分更新（patchのキーだけ更新）
    """
    doc = db.get(Document, doc_id)
    if not doc:
        return None

    for k, v in patch.items():
        if hasattr(doc, k):
            setattr(doc, k, v)

    db.commit()
    db.refresh(doc)
    return doc


def increment_access_counter(db: Session, doc_id: int, inc: int = 1) -> bool:
    """
    access_counter を +1（検索で参照された回数カウント用）
    """
    stmt = update(Document).where(Document.id == doc_id).values(
        access_counter=Document.access_counter + inc
    )
    result = db.execute(stmt)
    db.commit()
    return result.rowcount > 0


def set_latest_for_family(db: Session, family_key: str, latest_doc_id: int) -> None:
    """
    family_key 内で最新1件だけ is_latest=true にする
    """
    # まず全部false
    db.execute(
        update(Document).where(Document.family_key == family_key).values(is_latest=False)
    )
    # 指定だけtrue
    db.execute(
        update(Document).where(Document.id == latest_doc_id).values(is_latest=True)
    )
    db.commit()


# --- Delete ---
def delete_document(db: Session, doc_id: int) -> bool:
    doc = db.get(Document, doc_id)
    if not doc:
        return False
    db.delete(doc)
    db.commit()
    return True
