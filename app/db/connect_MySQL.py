'''
app.db.connect_MySQL

「アプリ全体で共有する DB エンジンを、1回だけ作るモジュール」

engineを一度だけ定義するためのもの 共有リソース定義モジュールのため、
ベタ打ちの内容が、import時に実行されます。
DB_NAME_DOCUMENTS と DB_NAME_CHUNKS の2つのDBに接続するエンジンを作成します。

'''


from sqlalchemy import create_engine
import os, tempfile

# データベース接続情報
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_NAME_DOCUMENTS = os.getenv('DB_NAME_DOCUMENTS')
DB_NAME_CHUNKS = os.getenv('DB_NAME_CHUNKS')

# ローカル実行用：CA証明書ファイルのパス（.env想定）
SSL_CA_PATH = os.getenv('SSL_CA_PATH')

# MySQLのURL構築
DATABASE_URL_DOCUMENTS = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME_DOCUMENTS}"
DATABASE_URL_CHUNKS = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME_CHUNKS}"

# ローカル実行時用の処理 SSL証明書ファイルのパスを絶対パスに変換
# current_dir = os.path.dirname(os.path.abspath(__file__))
# backend_dir = os.path.dirname(current_dir)  # db_controlの親ディレクトリ（backend）
# cert_path = os.path.join(backend_dir, "DigiCertGlobalRootG2.crt.pem")
 
# Azure用:
# PEMを環境変数から読み取り、クラウド側でtmpファイルに保存しパスを返す関数
def prepare_ca_file_from_env() -> str | None:
    pem = os.getenv("PEM_CONTENT")  # CA証明書本文/ Azure実行時用
    if not pem:
        return None
    pem = pem.replace("\\n", "\n")   # \n文字列を改行に置き替え
    ca_path = os.path.join(tempfile.gettempdir(), "mysql-ca.pem")
    with open(ca_path, "w") as f:
        f.write(pem)
    return ca_path

ca_path = prepare_ca_file_from_env() or SSL_CA_PATH


connect_args = {}
if ca_path:
    connect_args = {"ssl": {"ca": ca_path, "check_hostname": False}}

# エンジンの作成
engine_documents = create_engine(
    DATABASE_URL_DOCUMENTS,
    echo=True,
    pool_pre_ping=True,
    pool_recycle=3600,
    connect_args=connect_args,
)

engine_chunks = create_engine(
    DATABASE_URL_CHUNKS,
    echo=True,
    pool_pre_ping=True,
    pool_recycle=3600,
    connect_args=connect_args,
)



