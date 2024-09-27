# view_reservations.py

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem
import sqlite3
import os

class ViewReservationsPage(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # 메인 레이아웃 설정
        main_layout = QVBoxLayout()

        # 테이블 위젯 생성
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["예약번호", "환자 이름", "예약 날짜", "예약 시간", "전화번호"])

        # 메인 레이아웃에 테이블 위젯 추가
        main_layout.addWidget(self.table)

        self.setLayout(main_layout)

    def showEvent(self, event):
        self.load_reservations()
        super().showEvent(event)

    def load_reservations(self):
        # 프로젝트 루트 디렉토리의 절대 경로를 가져오기
        base_dir = os.path.dirname(os.path.abspath(__file__))
        db_path = os.path.join(base_dir, "../db/clinic.db")

        # 데이터베이스 연결
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # 모든 예약 내역 조회 (patients 테이블과 조인하여 환자 정보 가져오기)
        cursor.execute('''
            SELECT reservations.id, patients.name, reservations.reservation_date, reservations.reservation_time, patients.phone
            FROM reservations
            JOIN patients ON reservations.patient_id = patients.id
        ''')
        rows = cursor.fetchall()

        # 테이블 위젯에 데이터 추가
        self.table.setRowCount(len(rows))
        for i, row in enumerate(rows):
            for j, value in enumerate(row):
                self.table.setItem(i, j, QTableWidgetItem(str(value)))

        conn.close()
