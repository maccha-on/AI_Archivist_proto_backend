"""
RAG用のプロンプト作成と回答生成を行うモジュール
"""

import os
from openai import OpenAI
from dotenv import load_dotenv

# 環境変数の読み込み
load_dotenv()

# APIキー取得
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise RuntimeError("OPENAI_API_KEY is not set")

# OpenAIクライアント初期化
client = OpenAI(api_key=OPENAI_API_KEY)


def build_rag_prompt(question: str, contexts: list[dict]) -> str:
    # 検索結果を文章としてまとめる
    context_text = "\n\n".join(
        f"[p{c['page']}] {c['text']}"
        for c in contexts
    )

    # RAG用プロンプト
    return f"""
あなたは社内規定に詳しいアシスタントです。
以下の資料を参考に質問に答えてください。

### 資料
{context_text}

### 質問
{question}
"""


def generate_answer(prompt: str) -> str:
    # GPTで回答生成
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "あなたは社内規定に詳しいアシスタントです。"},
            {"role": "user", "content": prompt},
        ],
        temperature=0.2,
        max_tokens=1024,
    )

    return response.choices[0].message.content
