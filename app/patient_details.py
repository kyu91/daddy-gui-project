# patient_details.py

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QFormLayout, QLineEdit, QPushButton, QLabel, QTableWidget, QTableWidgetItem, QMessageBox, QHBoxLayout
import sqlite3
import os

class PatientDetailsPage(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # 메인 레이아웃
        main_layout = QVBoxLayout()

        # 검색 레이아웃 설정
        search_layout = QFormLayout()
        self.search_input = QLineEdit()
        search_layout.addRow("환자 이름 또는 전화번호", self.search_input)
        
        search_button = QPushButton("검색")
        search_button.clicked.connect(self.search_patients)
        search_layout.addWidget(search_button)

        # 검색 결과 테이블 생성
        self.result_table = QTableWidget()
        self.result_table.setColumnCount(5)  # 선택 버튼을 위한 열 추가
        self.result_table.setHorizontalHeaderLabels(["고유 번호", "이름", "생년월일", "전화번호", "선택"])

        # 환자 정보 라벨 및 예약 내역 테이블
        self.patient_info_label = QLabel("")

        # 선택된 환자의 정보를 표시하는 레이아웃
        detail_layout = QFormLayout()
        self.name_label = QLineEdit()
        self.name_label.setReadOnly(True)
        self.birthdate_label = QLineEdit()
        self.birthdate_label.setReadOnly(True)
        self.phone_label = QLineEdit()
        self.phone_label.setReadOnly(True)

        detail_layout.addRow("이름", self.name_label)
        detail_layout.addRow("생년월일", self.birthdate_label)
        detail_layout.addRow("전화번호", self.phone_label)

        # 예약 내역 테이블 생성
        self.reservation_table = QTableWidget()
        self.reservation_table.setColumnCount(3)
        self.reservation_table.setHorizontalHeaderLabels(["예약 번호", "예약 날짜", "예약 시간"])

        # 메인 레이아웃 구성
        main_layout.addLayout(search_layout)
        main_layout.addWidget(QLabel("검색 결과 화면"))
        main_layout.addWidget(self.result_table)
        main_layout.addWidget(self.patient_info_label)
        main_layout.addLayout(detail_layout)
        main_layout.addWidget(QLabel("예약 내역 (이 환자만의 예약 내역)"))
        main_layout.addWidget(self.reservation_table)

        self.setLayout(main_layout)

    def search_patients(self):
        search_term = self.search_input.text()

        # 프로젝트 루트 디렉토리의 절대 경로를 가져오기
        base_dir = os.path.dirname(os.path.abspath(__file__))
        db_path = os.path.join(base_dir, "../db/clinic.db")

        # 데이터베이스 연결
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # 검색 쿼리 실행 (이름 또는 전화번호로 검색)
        cursor.execute("SELECT id, name, birthdate, phone FROM patients WHERE name LIKE ? OR phone LIKE ?", ('%' + search_term + '%', '%' + search_term + '%'))
        rows = cursor.fetchall()

        # 검색 결과 테이블에 데이터 추가
        self.result_table.setRowCount(len(rows))
        for i, row in enumerate(rows):
            for j, value in enumerate(row):
                self.result_table.setItem(i, j, QTableWidgetItem(str(value)))
            # 선택 버튼 추가
            select_button = QPushButton("선택")
            select_button.clicked.connect(lambda _, r=row: self.fill_form(r))
            self.result_table.setCellWidget(i, 4, select_button)  # 마지막 열에 버튼 추가

        conn.close()

    def fill_form(self, patient):
        patient_id, name, birthdate, phone = patient
        self.name_label.setText(name)
        self.birthdate_label.setText(birthdate)
        self.phone_label.setText(phone)

        # 예약 내역 불러오기
        self.load_reservations(patient_id)

    def load_reservations(self, patient_id):
        # 프로젝트 루트 디렉토리의 절대 경로를 가져오기
        base_dir = os.path.dirname(os.path.abspath(__file__))
        db_path = os.path.join(base_dir, "../db/clinic.db")

        # 데이터베이스 연결
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # 선택된 환자의 예약 내역 가져오기
        cursor.execute("SELECT id, reservation_date, reservation_time FROM reservations WHERE patient_id=?", (patient_id,))
        rows = cursor.fetchall()

        # 예약 내역 테이블에 데이터 추가
        self.reservation_table.setRowCount(len(rows))
        for i, row in enumerate(rows):
            for j, value in enumerate(row):
                self.reservation_table.setItem(i, j, QTableWidgetItem(str(value)))

        conn.close()
