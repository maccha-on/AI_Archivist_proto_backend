# app/db/mymodels_MySQL.py
from sqlalchemy import (
    Column, BigInteger, Integer, String, Text, DateTime, Boolean,
    Enum, DECIMAL, CheckConstraint, func
)
from sqlalchemy.orm import declarative_base
from sqlalchemy.dialects.mysql import JSON

Base = declarative_base()

STATUS_ENUM = ("processing", "completed", "failed")
CONTENT_TYPE_ENUM = ("technical", "business", "rules", "contract", "minute", "email", "memo", "misc")
SECURITY_ENUM = ("public", "internal", "confidential", "secret")


class Document(Base):
    """
    documents テーブル（PoC版）
    """
    __tablename__ = "documents"

    # 基本データ
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    original_filename = Column(String(512), nullable=False)
    local_path = Column(String(2048), nullable=False)
    os_modified_date = Column(DateTime, nullable=True)
    mime_type = Column(String(255), nullable=True)

    # 管理情報
    is_latest = Column(Boolean, nullable=False, default=True)
    status = Column(Enum(*STATUS_ENUM), nullable=False, default="processing")
    sha256 = Column(String(64), nullable=True, unique=True)  # sha256の重複防止（NULLは重複可）
    version_label = Column(String(128), nullable=True)
    family_key = Column(String(512), nullable=True)
    access_counter = Column(Integer, nullable=False, default=0)
    pages = Column(Integer, nullable=True)

    # 解析結果
    estimated_timestamp = Column(DateTime, nullable=True)
    estimated_author = Column(String(255), nullable=True)
    content_summary = Column(Text, nullable=True)
    content_type = Column(Enum(*CONTENT_TYPE_ENUM), nullable=True)
    ai_tags_json = Column(JSON, nullable=True)  # ["tag1","tag2"] のような配列を想定
    created_company = Column(String(255), nullable=True)
    department = Column(String(255), nullable=True)
    project_name = Column(String(255), nullable=True)

    # スコア
    content_formality_level = Column(DECIMAL(5, 4), nullable=True)  # 0..1
    approval_position_level = Column(DECIMAL(5, 4), nullable=True)  # 0..1（役職の高さ）
    security_level = Column(Enum(*SECURITY_ENUM), nullable=True)
    jargon_level = Column(DECIMAL(5, 4), nullable=True)            # 0..1
    public_moral_level = Column(DECIMAL(5, 4), nullable=True)      # 0..1
    financial_scale = Column(BigInteger, nullable=True)            # JPY（整数）
    content_entropy = Column(DECIMAL(5, 4), nullable=True)         # 0..1
    text_density = Column(Integer, nullable=True)                  # 1ページあたり文字数（整数）
    technical_level = Column(DECIMAL(5, 4), nullable=True)         # 0..1

    # 監査（あると便利）
    uploaded_at = Column(DateTime, nullable=False, server_default=func.now())
    updated_at = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())

    __table_args__ = (
        # 0..1チェック（MySQLは8.0.16+で有効に働きやすい）
        CheckConstraint("content_formality_level IS NULL OR (content_formality_level >= 0 AND content_formality_level <= 1)"),
        CheckConstraint("approval_position_level IS NULL OR (approval_position_level >= 0 AND approval_position_level <= 1)"),
        CheckConstraint("jargon_level IS NULL OR (jargon_level >= 0 AND jargon_level <= 1)"),
        CheckConstraint("public_moral_level IS NULL OR (public_moral_level >= 0 AND public_moral_level <= 1)"),
        CheckConstraint("content_entropy IS NULL OR (content_entropy >= 0 AND content_entropy <= 1)"),
        CheckConstraint("technical_level IS NULL OR (technical_level >= 0 AND technical_level <= 1)"),
        CheckConstraint("financial_scale IS NULL OR financial_scale >= 0"),
    )
