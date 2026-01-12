"""
PDFフォルダ内のファイルを読み込み、
文章を分割 → Embedding → FAISSへ登録する
"""

import os
from app.analyzer.file_loader import load_pdf
from app.analyzer.text_splitter import split_text_with_overlap
from app.analyzer.embedder import get_embedding
from app.analyzer.index_manager import add_vector, index

# ファイルのメタ情報読み取り用
from app.db.documents_store import add_document_record
from datetime import datetime, timezone


def analyze_files(file_dir: str):
    # PDFフォルダ内のPDF一覧を取得
    pdf_paths = [
        os.path.join(file_dir, f)
        for f in os.listdir(file_dir)
        if f.lower().endswith(".pdf")
    ]

    # 各PDFを処理
    for pdf_path in pdf_paths:
        # ドキュメントIDはファイル名（拡張子なし）で一意と仮定
        doc_id = os.path.splitext(os.path.basename(pdf_path))[0]
        try:
            # PDF → ページ単位で読み込み   pages: list[dict]
            pdf_data = load_pdf(pdf_path)
            # 後で使うため独立変数化
            pages = pdf_data["pages"]
            # ★ load_pdf 完了直後に documents.json へ追記
            add_document_record(pdf_path, pages_count=len(pages), summary=pdf_data["summary"], estimated_timestamp=pdf_data["estimated_timestamp"])

            for page in pages:
                # ページ文章をチャンク分割
                chunks = split_text_with_overlap(page["text"])

                for i, chunk in enumerate(chunks):
                    # チャンクをEmbedding
                    embedding = get_embedding(chunk)

                    # FAISSへ登録
                    add_vector(
                        embedding,
                        {
                            "doc_id": doc_id,
                            "page": page["page"],
                            "chunk_id": i,
                            "text": chunk,
                        },
                    )
        except Exception as e:
            print(f"[ERROR] analyzer: PDFの処理に失敗しました: {pdf_path} エラー: {e}")

        # 登録結果を表示
        print(f"FAISS登録済みベクトル数: {index.ntotal}")

