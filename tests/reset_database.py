import sqlite3
import os

def reset_database():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(base_dir, "../db/clinic.db")

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # 기존 테이블 삭제
    cursor.execute("DROP TABLE IF EXISTS patients")
    cursor.execute("DROP TABLE IF EXISTS reservations")

    # 새로운 테이블 생성
    cursor.execute('''
        CREATE TABLE patients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            phone TEXT NOT NULL,
            birthdate DATE NOT NULL  -- 생년월일을 DATE 타입으로 변경
        )
    ''')

    cursor.execute('''
        CREATE TABLE reservations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id INTEGER NOT NULL,
            reservation_date TEXT NOT NULL,
            reservation_time TEXT NOT NULL,
            remarks TEXT,
            FOREIGN KEY (patient_id) REFERENCES patients(id)
        )
    ''')

    conn.commit()
    conn.close()

if __name__ == "__main__":
    reset_database()
