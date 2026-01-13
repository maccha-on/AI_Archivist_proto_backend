# app/db/create_tables.py
"""
一回だけ実行してテーブルを作るスクリプト
例: python -m app.db.create_tables
"""
from app.db.connect_MySQL import engine
from app.db.mymodels_MySQL import Base

def main():
    Base.metadata.create_all(bind=engine)
    print("✅ tables created")

if __name__ == "__main__":
    main()
