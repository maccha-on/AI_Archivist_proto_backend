

sequenceDiagram
autonumber
actor User as ユーザー
participant API as FastAPI(API層)
participant RDB as RDB（文書台帳）
participant Search as Azure AI Search
participant AI as AI（任意：説明生成）

User->>API: POST /search (query, filters, top_k, return_answer)
API->>RDB: フィルタ補助情報取得（任意）/ 文書状態確認（任意）
RDB-->>API: フィルタ条件/制御情報

API->>Search: ハイブリッド検索（全文＋ベクトル） + 属性フィルタ
Search-->>API: chunk結果（doc_id, score, page, snippet, attributes...）

API->>API: doc_id単位で集計（スコア合算/件数など）
API->>RDB: doc_id→family_key, is_latest取得（最新版制御）
RDB-->>API: family_key, is_latest 等

API->>API: family_key単位で最新版のみ残す（is_latest=true）
API->>API: 文書ランキング生成（上位N、根拠チャンク添付）

alt return_answer=true
  API->>AI: 上位文書＋根拠から説明文生成
  AI-->>API: answer（説明文）
end

API-->>User: 200 OK（文書名/ID、根拠、任意でanswer）
