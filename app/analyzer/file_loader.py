"""
ファイルを読み込み、文章データとして返すモジュール
（現時点ではPDFのみ対応）

履歴：
2026.1.3 エラーが出た場合の例外処理を追加
"""

from pypdf import PdfReader
from openai import OpenAI
import logging, json
from app.core.clients import get_openai_client


def load_pdf(path: str) -> list[dict]:
    try:
        # PDFを開く
        reader = PdfReader(path)

        pages = []
        page_text_list = []

        # ページ単位で処理
        for i, page in enumerate(reader.pages):
            text = page.extract_text()

            # 文字が取得できたページのみ追加
            if text:
                pages.append({
                    "page": i + 1,
                    "text": text,
                })
                page_text_list.append(text)
        full_text = "\n".join(page_text_list)

        print(f"full_text: {full_text[:200]}")
        # =====================
        # OpenAI API による要約・更新日推定
        # =====================
        prompt = f"""
以下はPDF文書の全文です。

次の条件を厳守して回答してください。

- 出力は JSON形式のテキストのみ。マークダウン形式にはしないこと。
- 文章や説明文は一切含めない。 
- フィールドは次の2つだけ
  - summary : 文書全体の要約（200文字以内、日本語）
  - estimated_timestamp : 本文から推定される最終更新日
    - ISO形式（YYYY-MM-DD）
    - 推定できない場合は "unknown"

---- PDF本文 ----
{full_text}
"""
        client = get_openai_client()
        response = client.chat.completions.create(
            model="gpt-4o-mini",  # 軽量・安価モデル想定
            messages=[
                {"role": "system", "content": "あなたは文書解析アシスタントです。"},
                {"role": "user", "content": prompt},
            ],
            temperature=0.1,  # JSON安定化
        )
        raw_content = response.choices[0].message.content

        # =====================
        # JSONとして安全にパース
        # =====================
        print("AI raw response repr:", (raw_content))
        ai_result = json.loads(raw_content)

        return {
            "pages": pages,
            "summary": ai_result.get("summary", ""),
            "estimated_timestamp": ai_result.get("estimated_timestamp", "unknown"),
        }

    except json.JSONDecodeError as e:
        logging.error(f"AIのJSONパースに失敗しました: {e}")
    except Exception as e:
        logging.error(f"PDFの読み込みに失敗しました: {path} エラー: {e}")

    return {
        "pages": [],
        "summary": "",
        "estimated_timestamp": "unknown",
    }