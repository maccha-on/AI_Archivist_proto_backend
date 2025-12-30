"""
backend_embedder.py（ダミー版）

このファイルは「テキストをベクトル化する（embedding）」役割を持つ
バックエンドBのモジュールです。

本来なら OpenAI や Azure OpenAI の embedding API を呼び出して
“意味を持つベクトル” を作ります。

しかし、まだ本番実装は後で良いので、
ここではランダムな数値リストを作るだけのダミー実装です。

ポイント：
- main.py の処理の流れを完成させるための仮実装
- ベクトルの長さは「適当」でOK（例えば 32 次元）
- 後で本物の API に差し替えればよい
"""

import random
from core_types import Chunk, EmbeddedChunk


def embed_chunks(chunks: list):
    """
    チャンクのリストを受け取り、
    “ランダムなベクトル” を付けて EmbeddedChunk にして返すダミー関数。

    本物の embedding モデルを使う前のテスト目的です。

    パラメータ：
      chunks : list[Chunk]
        PDF抽出モジュール（extractor）が返すチャンクのリスト

    戻り値：
      list[EmbeddedChunk]
        embedding（ベクトル）が付与された新しいチャンク
    """

    embedded_list = []

    # ダミーのベクトルのサイズ（本物なら 1536 などになる）
    VECTOR_SIZE = 32

    for ch in chunks:
        # ---------------------------------------------------------
        # ① ランダムな embedding ベクトルを作成
        # ---------------------------------------------------------
        dummy_vector = [
            random.uniform(-1, 1)  # -1〜1 の間でランダムな浮動小数点数
            for _ in range(VECTOR_SIZE)
        ]

        # ---------------------------------------------------------
        # ② EmbeddedChunk を作成
        # ---------------------------------------------------------
        embedded_chunk = EmbeddedChunk(
            chunk_index=ch.chunk_index,
            text=ch.text,
            metadata=ch.metadata,
            embedding=dummy_vector,
        )

        embedded_list.append(embedded_chunk)

    # ---------------------------------------------------------
    # ③ embedding が付与されたチャンク一覧を main.py に返す
    # ---------------------------------------------------------
    return embedded_list
