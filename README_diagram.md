::: mermaid


flowchart TD
    %% Entry Point
    MAIN[main.py<br/>アプリ起点]

    %% Analyzer
    subgraph ANALYZER[analyzer / データ解析]
        A1[analyzer.py<br/>全体制御]
        A2[file_loader.py<br/>PDF → 文章]
        A3[text_splitter.py<br/>文章 → チャンク]
        A4[embedder.py<br/>文章 → Embedding]
        A5[index_manager.py<br/>FAISS登録]
    end

    %% Finder
    subgraph FINDER[finder / 検索・回答]
        F1[finder.py<br/>質問処理入口]
        F2[search.py<br/>類似検索]
        F3[rag.py<br/>プロンプト生成・回答]
    end

    %% External
    FAISS[(FAISS Index)]
    GEMINI[Gemini API<br/>Embedding]
    OPENAI[OpenAI API<br/>回答生成]

    %% Flow
    MAIN --> A1
    A1 --> A2
    A2 --> A3
    A3 --> A4
    A4 --> A5
    A5 --> FAISS
    A4 --> GEMINI

    MAIN --> F1
    F1 --> F2
    F2 --> FAISS
    F1 --> F3
    F3 --> OPENAI
