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
        chunks.append(text[start:end])
        start = end - overlap

    return chunks
