"""
VectorDB（埋め込みベクトル保存）向けの永続化処理（ダミー実装）

このファイルは `persistence.py` から分割したもので、
埋め込み付きチャンクを保存する処理を担当します。
"""

from app.core_types import EmbeddedChunk


def save_document_chunks(document_id: int, chunks: list[EmbeddedChunk]) -> int:
    """
    embedding が付いたチャンクを保存するダミー関数（VectorDB担当）。

    実運用では Vector DB（Pinecone, Milvus, Weaviate など）へ保存しますが、
    このダミー実装では内容を print するだけにしています。
    戻り値は保存したチャンク数です。
    """

    print("\n[VECTOR-DB-DUMMY] チャンクを保存します:")
    print(f"  document_id = {document_id}")
    print("  --- チャンク一覧 ---")

    for ch in chunks:
        print(f"   - chunk_index : {ch.chunk_index}")
        print(f"     text        : {ch.text[:20]}...")
        print(f"     metadata    : {ch.metadata}")
        print(f"     embedding(サイズ): {len(ch.embedding)} 次元")
        print("")

    print(f"[VECTOR-DB-DUMMY] チャンク保存完了（{len(chunks)} 件）")

    return len(chunks)
