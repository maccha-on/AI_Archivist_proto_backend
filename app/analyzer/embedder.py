"""
文章からEmbedding（ベクトル）を生成するモジュール
"""

import os
import numpy as np
from google import genai
from dotenv import load_dotenv

# 環境変数の読み込み
load_dotenv()

# APIキー取得
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    raise RuntimeError("GOOGLE_API_KEY is not set")

# Gemini クライアント初期化
client = genai.Client()


def get_embedding(text: str) -> np.ndarray:
    # 文章をEmbeddingに変換
    result = client.models.embed_content(
        model="gemini-embedding-001",
        contents=text,
    )

    # numpy配列に変換して返す
    return np.array(result.embeddings[0].values, dtype="float32")
