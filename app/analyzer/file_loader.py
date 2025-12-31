"""
ファイルを読み込み、文章データとして返すモジュール
（現時点ではPDFのみ対応）
"""

from pypdf import PdfReader


def load_pdf(path: str) -> list[dict]:
    # PDFを開く
    reader = PdfReader(path)

    pages = []

    # ページ単位で処理
    for i, page in enumerate(reader.pages):
        text = page.extract_text()

        # 文字が取得できたページのみ追加
        if text:
            pages.append({
                "page": i + 1,
                "text": text,
            })

    return pages
