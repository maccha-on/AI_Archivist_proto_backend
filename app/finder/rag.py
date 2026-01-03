"""
RAG用のプロンプト作成と回答生成を行うモジュール
"""

import os
from openai import OpenAI
from app.core.clients import get_gemini_client, get_openai_client


def build_rag_prompt(question: str, contexts: list[dict]) -> str:
    # 検索結果を文章としてまとめる
    context_text = "\n\n".join(
        f"[p{c['page']}] {c['text']}"
        for c in contexts
    )

    # RAG用プロンプト
    # 2026/1/3修正: 役割の記載が2重になっていたため削除
    return f"""
以下の資料を参考に質問に答えてください。

### 資料
{context_text}

### 質問
{question}
"""


def generate_answer(prompt: str) -> str:
    # GPTで回答生成
    # client = get_openai_client()
    # => 2026/1/3修正: クライアント呼び出しはcore/clients.pyに集約しています。
    #    もし新規にクライアントを生成する必要があれば修正してください。
    client = get_openai_client()
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
