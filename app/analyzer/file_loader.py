"""
ファイルを読み込み、文章データとして返すモジュール
（現時点ではPDFのみ対応）

履歴：
2026.1.3 エラーが出た場合の例外処理を追加
"""

from pypdf import PdfReader
import logging


def load_pdf(path: str) -> list[dict]:
    try:
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

    except Exception as e:
        logging.error(f"PDFの読み込みに失敗しました: {path} エラー: {e}")
        return []

    return pages
    
