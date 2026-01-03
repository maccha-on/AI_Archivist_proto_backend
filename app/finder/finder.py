"""
検索とRAGをまとめた窓口モジュール
"""

from app.finder.search import search_chunks
from app.finder.rag import build_rag_prompt, generate_answer


def answer_query(question: str, top_k: int = 3) -> dict:
    # 類似文章を検索
    contexts = search_chunks(question, top_k)

    # RAG用プロンプト作成
    prompt = build_rag_prompt(question, contexts)

    # 回答生成
    answer = generate_answer(prompt)

    return {
        "answer": answer,
        "contexts": contexts,
    }
