import sqlite3
import os

def alter_table():
    # 프로젝트 루트 디렉토리의 절대 경로를 가져오기
    base_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(base_dir, "../db/clinic.db")

    # 데이터베이스 연결
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # 새로운 칼럼 추가
    try:
        cursor.execute("ALTER TABLE reservations ADD COLUMN reservation_date TEXT")
        cursor.execute("ALTER TABLE reservations ADD COLUMN reservation_time TEXT")
    except sqlite3.OperationalError:
        # 칼럼이 이미 존재할 경우 무시
        pass

    conn.commit()
    conn.close()

if __name__ == "__main__":
    alter_table()
