import numpy as np
from app.core.clients import get_gemini_client


def get_embedding(text: str) -> np.ndarray:
    """
    Gemini Embedding を取得して float32 の numpy配列で返す
    """
    client_gemini = get_gemini_client()
    res = client_gemini.models.embed_content(
        model="gemini-embedding-001",
        contents=text
    )
    return np.array(res.embeddings[0].values, dtype="float32")