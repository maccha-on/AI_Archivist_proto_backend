sequenceDiagram
autonumber
actor User as ユーザー
participant API as FastAPI(API層)
participant Blob as Blob Storage
participant RDB as RDB（文書台帳）
participant Queue as Queue/Job
participant Worker as 解析Worker
participant PDF as PDF抽出/分割
participant AI as AI（属性推定/Embedding）
participant Search as Azure AI Search

User->>API: POST /documents/upload (PDF, author等)
API->>Blob: PDF保存
Blob-->>API: blob_uri
API->>RDB: documents作成(status=processing, blob_uri等)
RDB-->>API: document_id
API->>Queue: 解析ジョブ投入(document_id)
API-->>User: 202 Accepted (document_id, status=processing)

Queue-->>Worker: ジョブ取得(document_id)
Worker->>RDB: documents取得(blob_uri等)
Worker->>Blob: PDF取得(blob_uri)
Worker->>PDF: テキスト抽出
PDF-->>Worker: 抽出テキスト(ページ単位)
Worker->>PDF: チャンク分割(page/chunk_id)
PDF-->>Worker: chunks[{chunk_id,page,text}]

Worker->>AI: 文書属性推定(先頭/末尾など)
AI-->>Worker: attributes(doc_type,tags,summary,confidence,...)
Worker->>RDB: attributes保存(document_attributes)

loop for each chunk
  Worker->>AI: Embedding生成(text)
  AI-->>Worker: embedding(vector)
  Worker->>Search: chunk登録(doc_id, page, text, embedding, 属性複製)
end

Worker->>RDB: documents更新(status=completed, is_latest判定用情報)
RDB-->>Worker: OK