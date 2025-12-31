# --- ライブラリ ---
import os
import numpy as np
import faiss
from pypdf import PdfReader
from google import genai
from openai import OpenAI  # 最新SDK v1.0+
from dotenv import load_dotenv
 
# --- APIキー設定 ---
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if not OPENAI_API_KEY or not GOOGLE_API_KEY:
    raise RuntimeError("API_KEY is not set")

client_gemini = genai.Client()
openai_client = OpenAI(api_key=OPENAI_API_KEY)
 
# --- PDF読み込み関数 ---
def load_pdf(path):
    reader = PdfReader(path)
    pages = []
    for i, page in enumerate(reader.pages):
        text = page.extract_text()
        if text:
            pages.append({"page": i+1, "text": text})
    return pages
 
# --- チャンク分割 ---
def split_text_with_overlap(text, chunk_size=400, overlap=80):
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start = end - overlap
    return chunks
 
# --- Embedding取得（Gemini） ---
def get_embedding(text):
    res = client_gemini.models.embed_content(
        model="gemini-embedding-001",
        contents=text
    )
    return np.array(res.embeddings[0].values, dtype="float32")
 
# --- FAISS初期化 ---
dummy_emb = get_embedding("dummy")
EMBEDDING_DIM = len(dummy_emb)
index = faiss.IndexFlatIP(EMBEDDING_DIM)
meta_data = []
 
# --- PDFフォルダ内のPDFを一括登録 ---
pdf_folder = "./test/import_documents"
pdf_paths = [
    os.path.join(pdf_folder, f)
    for f in os.listdir(pdf_folder)
    if f.lower().endswith(".pdf")
]
 
for pdf_path in pdf_paths:
    doc_id = os.path.basename(pdf_path).split(".")[0]
    pages = load_pdf(pdf_path)
    for page in pages:
        chunks = split_text_with_overlap(page["text"])
        for i, chunk in enumerate(chunks):
            emb = get_embedding(chunk)
            faiss.normalize_L2(emb.reshape(1, -1))
            index.add(emb.reshape(1, -1))
            meta_data.append({
                "doc_id": doc_id,
                "page": page["page"],
                "chunk_id": i,
                "text": chunk
            })
 
print(f"FAISS登録済みベクトル数: {index.ntotal}")
 
# --- 類似検索 ---
def search_chunks(query, top_k=3):
    q_emb = get_embedding(query)
    faiss.normalize_L2(q_emb.reshape(1, -1))
    D, I = index.search(q_emb.reshape(1, -1), top_k)
    return [meta_data[i] for i in I[0]]
 
# --- RAGプロンプト作成 ---
def build_rag_prompt(question, contexts):
    context_text = "\n\n".join(
        f"[p{c['page']}] {c['text']}" for c in contexts
    )
    return f"""
あなたは社内規定に詳しいアシスタントです。
以下の資料を参考に質問に答えてください。

### 資料
{context_text}

### 質問
{question}
"""
 
# --- GPT4で回答生成（OpenAI最新SDK v1.0+） ---
def generate_answer(prompt):
    response = openai_client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "あなたは社内規定に詳しいアシスタントです。"},
            {"role": "user", "content": prompt}
        ],
        temperature=0.2,
        max_tokens=1024
    )
    return response.choices[0].message.content
 
# --- RAG回答 ---
def rag_answer(question, top_k=3):
    contexts = search_chunks(question, top_k)
    prompt = build_rag_prompt(question, contexts)
    answer = generate_answer(prompt)
    return {"answer": answer, "contexts": contexts}

# --- 質問例 ---
#quesiton ="新規採用者の試用期間は？"    
quesiton ="社員の労働時間を教えてください"
#quesiton ="適用範囲を教えてください"    

# --- 実行例 ---
result = rag_answer(quesiton)

print(quesiton)
 
print("=== 回答 ===")
print(result["answer"])
 
print("\n=== 参照チャンク ===")
for c in result["contexts"]:
    print(f"page {c['page']}: {c['text'][:80]}...")
