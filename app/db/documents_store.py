"""
documents_store.py

documents.json を「簡易データベース」として使うためのモジュール。
PoC（試作）用に、できるだけシンプルな実装にしている。

【このモジュールの役割】
- PDFファイル1つにつき、documents.json に1レコードを追加する
- DBやORMは使わない
- 「PDFを読み取った事実」を残すことが目的

【以下は未実施】
- 重複チェック
- バージョン管理
- 排他制御
- 高速化
"""

from __future__ import annotations

import json
import os
from pathlib import Path
from datetime import datetime, timezone
from typing import Any


# ============================================================
# 保存先設定
# ============================================================

# documents.json の保存場所
# 環境変数があればそちらを優先（将来切り替えしやすくするため）
DOC_PATH = Path(
    os.getenv("DOCUMENTS_JSON_PATH", "data/db_data/documents.json")
)


# ============================================================
# 内部ユーティリティ関数
# ============================================================

def _ensure_file() -> None:
    """
    documents.json が存在しない場合に作成する。
    初回実行時でもエラーにならないようにするための処理。
    
    現在は毎回初期化する処理にしているため、追加にする場合はif文を復活させる。
    """
    DOC_PATH.parent.mkdir(parents=True, exist_ok=True)
    # if not DOC_PATH.exists():
    DOC_PATH.write_text("[]", encoding="utf-8")


def _read_all() -> list[dict[str, Any]]:
    """
    documents.json を読み込み、Pythonのlistとして返す。
    """
    _ensure_file()
    text = DOC_PATH.read_text(encoding="utf-8")
    return json.loads(text) if text else []


def _write_all(items: list[dict[str, Any]]) -> None:
    """
    Pythonのlistを documents.json に書き戻す。
    indent を入れて、人が見やすいJSONにする。
    """
    DOC_PATH.write_text(
        json.dumps(items, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def _next_id(items: list[dict[str, Any]]) -> int:
    """
    次に使う id を決める。
    DBの AUTO_INCREMENT の簡易版。
    """
    return max([x.get("id", 0) for x in items], default=0) + 1


def _mtime_iso(path: str) -> str | None:
    """
    ファイルの最終更新日時（mtime）を
    ISO8601形式の文字列に変換する。

    取得できなかった場合は None を返す。
    """
    try:
        mtime = os.stat(path).st_mtime
        return (
            datetime.fromtimestamp(mtime, tz=timezone.utc)
            .replace(microsecond=0)
            .isoformat()
            .replace("+00:00", "Z")
        )
    except Exception:
        return None


# ============================================================
# 外部から呼ぶ関数（公開API）
# ============================================================

def add_document_record(pdf_path: str, pages_count: int, summary: str, estimated_timestamp: str) -> dict[str, Any]:
    """
    documents.json に1件レコードを追加する。

    【呼び出しタイミング】
    - load_pdf() が正常に完了した直後

    【引数】
    - pdf_path: PDFファイルのパス
    - pages_count: PDFのページ数

    【戻り値】
    - 追加したレコード（dict）
    """
    print("add_document_record called: pdf_path=", pdf_path, " pages_count=", pages_count) # デバッグ用出力
    items = _read_all()
    print("_read_all() returned ", items) # デバッグ用出力



    # 新しく追加するレコード
    record = {
        # 基本情報
        "id": _next_id(items),
        "original_filename": os.path.basename(pdf_path),
        "local_path": pdf_path,
        "os_modified_date": _mtime_iso(pdf_path),
        "mime_type": "application/pdf",
        "doc_summary": summary, 

        # 管理用（PoCでは最小限）
        "status": "completed",
        "pages": pages_count,
        "family_key": None,     # この時点では未確定
        "is_latest": True,      # 仮置き
        "version_label": None,
        "access_counter": 0,

        # AI解析結果（後で埋める前提）
        "estimated_timestamp": estimated_timestamp,
        "estimated_author": None,
        "content_summary": summary,
        "content_type": None,
        "ai_tags_json": None,
        "created_company": None,
        "department": None,
        "project_name": None,

        # スコア系（後工程で埋める）
        "content_formality_level": None,
        "approval_position_level": None,
        "security_level": None,
        "jargon_level": None,
        "public_moral_level": None,
        "financial_scale": None,
        "content_entropy": None,
        "text_density": None,
        "technical_level": None,
    }
    # print("New record to add: ", record) # デバッグ用出力

    # 追記して保存
    items.append(record)
    _write_all(items)

    return record
