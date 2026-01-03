"""
Embeddingを使ってFAISSから類似文章を検索するモジュール
"""

import faiss
from app.analyzer.embedder import get_embedding
from app.analyzer.index_manager import index, meta_data


def search_chunks(query: str, top_k: int = 3) -> list[dict]:
    # 質問文をEmbedding
    query_embedding = get_embedding(query)

    # cos類似度検索のため正規化
    faiss.normalize_L2(query_embedding.reshape(1, -1))

    # FAISSで検索
    _, indices = index.search(
        query_embedding.reshape(1, -1),
        top_k,
    )

    # 対応するメタデータを返す
    return [meta_data[i] for i in indices[0]]
