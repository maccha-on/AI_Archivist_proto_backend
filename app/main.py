"""
main.py

このファイルは、起動時にPDFファイルを読み込んで分析を行います。
その後、クエリ受信時に該当するファイルを探して応答します。

"""

import requests, json
import sys                          # コマンドライン引数（python main.py sample.pdf）を扱うため

from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from pathlib import Path            # ファイルの存在確認や名前取得を簡単にするための標準ライブラリ
from __future__ import annotations  # 型ヒントをシンプルに書けるようにするための 魔法 のようなもの

from analyzer.analyzer import analyze_files
from finder.finder import answer_query


# メイン実行処理
load_dotenv()
app = FastAPI(title="MOF2 Prototype API")
analyze_files("./test/import_documents")  # 起動時にPDFを読み込んで分析を実行

# CORSミドルウェアの設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# トップページの表示
@app.get("/")
def index():
    return {"message": "MOF^2 FastAPI top page!"}

# ヘルスチェック用エンドポイント
@app.get("/health")
def health():
    return {"status": "ok"}

# ファイル問合せ用エンドポイント
@app.get("/ask")
def ask(q: str = Query(..., description="質問文")):
    """
    GET /ask?q=適用範囲を教えてください
    のように質問を受け取って回答する。
    """
    result = answer_query(q)
    print("\n=== 参照チャンク ===")
    for c in result["contexts"]:
        print(f"page {c['page']}: {c['text'][:80]}...")
    return result