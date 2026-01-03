"""
文章をEmbedding用のサイズに分割するモジュール
"""

def split_text_with_overlap(
    text: str,
    chunk_size: int = 400,
    overlap: int = 80,
) -> list[str]:

    chunks = []
    start = 0

    # 文章を少し重ねながら分割
    while start < len(text):
        end = start + chunk_size

        # 2026.1.3例外処理を追加：空白チャンクや極小チャンクを除外する
        chunk = text[start:end]
        if not chunk.strip() or (chunks and len(chunk) < overlap):
            break

        chunks.append(chunk)
        start = end - overlap

    return chunks
