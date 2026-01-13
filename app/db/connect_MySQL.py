"""
app.db.connect_MySQL

アプリ全体で共有する DB エンジンを、1回だけ作るモジュール。
import時に実行される（副作用あり）ので、ここは最小限＆安全に。
"""

from __future__ import annotations

import os
import tempfile
from sqlalchemy import create_engine


def _require_env(name: str) -> str:
    v = os.getenv(name)
    if not v:
        raise RuntimeError(f"Missing env var: {name}")
    return v


# --- 必須：DB接続情報 ---
DB_USER = _require_env("DB_USER")
DB_PASSWORD = _require_env("DB_PASSWORD")
DB_HOST = _require_env("DB_HOST")
DB_PORT = _require_env("DB_PORT")
DB_NAME_DOCUMENTS = _require_env("DB_NAME_DOCUMENTS")
DB_NAME_CHUNKS = _require_env("DB_NAME_CHUNKS")

# --- 任意：ローカル実行用 CA パス ---
SSL_CA_PATH = os.getenv("SSL_CA_PATH")

# --- Azure用：CA本文（PEM）を環境変数から受け取りtmpに保存 ---
def prepare_ca_file_from_env() -> str | None:
    pem = os.getenv("PEM_CONTENT")
    if not pem:
        return None
    pem = pem.replace("\\n", "\n")
    ca_path = os.path.join(tempfile.gettempdir(), "mysql-ca.pem")
    with open(ca_path, "w", encoding="utf-8") as f:
        f.write(pem)
    return ca_path


ca_path = prepare_ca_file_from_env() or SSL_CA_PATH

connect_args = {}
if ca_path:
    # PoC向け。可能なら本番は check_hostname=True を推奨
    connect_args = {"ssl": {"ca": ca_path, "check_hostname": False}}

# echoは環境変数で切替（PoCではtrueが便利）
ECHO = os.getenv("DB_ECHO", "false").lower() == "true"

# charsetは明示しておく（日本語/記号で詰まらないため）
DATABASE_URL_DOCUMENTS = (
    f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME_DOCUMENTS}"
    f"?charset=utf8mb4"
)
DATABASE_URL_CHUNKS = (
    f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME_CHUNKS}"
    f"?charset=utf8mb4"
)

engine_documents = create_engine(
    DATABASE_URL_DOCUMENTS,
    echo=ECHO,
    pool_pre_ping=True,
    pool_recycle=3600,
    connect_args=connect_args,
)

engine_chunks = create_engine(
    DATABASE_URL_CHUNKS,
    echo=ECHO,
    pool_pre_ping=True,
    pool_recycle=3600,
    connect_args=connect_args,
)
