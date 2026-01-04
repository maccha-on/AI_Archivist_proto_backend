"""
main.py

このファイルは、起動時にPDFファイルを読み込んで分析を行います。
その後、クエリ受信時に該当するファイルを探して応答します。

"""

from __future__ import annotations  # 型ヒントをシンプルに書けるようにするための 魔法 のようなもの

import os

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from dotenv import load_dotenv


# ==================== 関数定義 =======================

# 分析処理が、API起動時のみ走るように指示
@asynccontextmanager
async def lifespan(app: FastAPI):
    analyze_files("./test/import_documents")  # 起動時にPDFを読み込んで分析を実行
    yield  # ← FastAPI がリクエスト受付を開始するポイント



# ==================== メイン処理 ======================

# 環境変数を読み込んでから各モジュールをインポート
load_dotenv(override=False)
from app.analyzer.analyzer import analyze_files
from app.finder.finder import answer_query

 # FastAPI起動
app = FastAPI(title="MOF2 Prototype API", lifespan=lifespan)

# CORSミドルウェアの設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)


# ================== APIサービス定義 ==================

# トップページの表示
@app.get("/")
def index():
    return {"message": "MOF^2 FastAPI top page!"}

# ヘルスチェック用エンドポイント
@app.get("/health")
def health():
    return {"status": "ok"}

# ファイル問合せ用エンドポイント
# 使用例 http://localhost:8000/ask?q=質問文
# askはURLログに残りやすいため本来はPOSTメソッド化が推奨される(未対応)
@app.get("/ask")
def ask(q: str = Query(..., description="質問文")):
    if not q or not q.strip():
        raise HTTPException(status_code=400, detail="404 No query message.")

    try:
        result = answer_query(q)
        return result
 
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

