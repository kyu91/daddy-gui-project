# patient_details.py

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QFormLayout, QLineEdit, QPushButton, QLabel, QTableWidget, QTableWidgetItem, QMessageBox
)
import sqlite3
import os

class PatientDetailsPage(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # 폼 레이아웃 설정
        form_layout = QFormLayout()

        # 입력 필드 생성
        self.name_input = QLineEdit()
        self.birthdate_input = QLineEdit()

        # 폼 레이아웃에 필드 추가
        form_layout.addRow("환자 이름", self.name_input)
        form_layout.addRow("생년월일", self.birthdate_input)

        # 조회 버튼 생성
        search_button = QPushButton("조회")
        search_button.clicked.connect(self.search_patient)

        # 환자 정보 라벨
        self.patient_info_label = QLabel("")

        # 테이블 위젯 생성 (예약 내역 표시)
        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["예약 날짜", "예약 시간", "전화번호"])

        # 메인 레이아웃 설정
        main_layout = QVBoxLayout()
        main_layout.addLayout(form_layout)
        main_layout.addWidget(search_button)
        main_layout.addWidget(self.patient_info_label)
        main_layout.addWidget(self.table)

        self.setLayout(main_layout)

    def search_patient(self):
        name = self.name_input.text()
        birthdate = self.birthdate_input.text()

        # 프로젝트 루트 디렉토리의 절대 경로를 가져오기
        base_dir = os.path.dirname(os.path.abspath(__file__))
        db_path = os.path.join(base_dir, "../db/clinic.db")

        # 데이터베이스 연결
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # 환자 정보 조회
        cursor.execute("SELECT name, phone, birthdate FROM reservations WHERE name=? AND birthdate=?", (name, birthdate))
        patient_info = cursor.fetchone()

        if patient_info:
            self.patient_info_label.setText(f"이름: {patient_info[0]}, 전화번호: {patient_info[1]}, 생년월일: {patient_info[2]}")

            # 환자 예약 내역 조회
            cursor.execute("SELECT reservation_date, reservation_time, phone FROM reservations WHERE name=? AND birthdate=?", (name, birthdate))
            rows = cursor.fetchall()

            # 테이블 초기화 후 데이터 추가
            self.table.setRowCount(len(rows))
            for i, row in enumerate(rows):
                for j, value in enumerate(row):
                    self.table.setItem(i, j, QTableWidgetItem(str(value)))
        else:
            self.patient_info_label.setText("")
            self.table.setRowCount(0)
            QMessageBox.warning(self, "오류", "해당 환자를 찾을 수 없습니다.")

        conn.close()
