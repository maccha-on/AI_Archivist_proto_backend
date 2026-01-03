"""
FAISSのインデックス管理を行うモジュール

役割：
- ベクトル検索用の FAISS index を初期化する
- ベクトルと一緒に保持するメタ情報（文章・ページ番号など）を管理する
- analyzer 側・finder 側の両方から利用される
"""

import faiss
from app.analyzer.embedder import get_embedding

# ----------------------------------------
# 1. FAISSインデックスの初期化
# ----------------------------------------

# FAISSは「ベクトルの次元数」を最初に決める必要があるため、
# ダミーの文章を1つEmbeddingして次元数を取得する
_dummy_embedding = get_embedding("dummy text")
EMBEDDING_DIM = len(_dummy_embedding)

# 内積（cos類似度用）で検索するシンプルなIndex
# 初級者向けには IndexFlatIP が一番分かりやすい
index = faiss.IndexFlatIP(EMBEDDING_DIM)

# ----------------------------------------
# 2. メタデータ格納用リスト
# ----------------------------------------

# FAISSは「ベクトル」しか覚えないため、
# 元の文章やページ番号などは自分で管理する必要がある
#
# index に追加した順番と meta_data の順番を一致させる
meta_data: list[dict] = []

# ----------------------------------------
# 3. ベクトルをインデックスに追加する関数
# ----------------------------------------

def add_vector(embedding, meta: dict):
    """
    ベクトルとメタ情報をFAISSに登録する

    Parameters
    ----------
    embedding : np.ndarray
        文章から生成したEmbeddingベクトル
    meta : dict
        {
            "doc_id": ファイル名,
            "page": ページ番号,
            "chunk_id": チャンク番号,
            "text": 実際の文章
        }
    """

    # cos類似度検索のため、L2正規化を行う
    faiss.normalize_L2(embedding.reshape(1, -1))

    # FAISSインデックスへ追加
    index.add(embedding.reshape(1, -1))

    # 同じ順番でメタ情報も保存
    meta_data.append(meta)
