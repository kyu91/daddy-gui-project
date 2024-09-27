# make_reservation.py

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QFormLayout, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem, QDateEdit, QTimeEdit, QMessageBox, QHBoxLayout, QLabel
from PyQt5.QtCore import Qt, QDate, QTime
import sqlite3
import os

class MakeReservationPage(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        # 폼 레이아웃 설정
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

        # 예약 폼 레이아웃
        form_layout = QFormLayout()

        self.name_label = QLineEdit()
        self.name_label.setReadOnly(True)
        self.birthdate_label = QLineEdit()
        self.birthdate_label.setReadOnly(True)

        # 전화번호 입력 필드 설정
        phone_layout = QHBoxLayout()
        self.phone_prefix = QLabel("010-")
        self.phone_middle_label = QLineEdit()
        self.phone_last_label = QLineEdit()
        self.phone_middle_label.setReadOnly(True)
        self.phone_last_label.setReadOnly(True)
        
        phone_layout.addWidget(self.phone_prefix)
        phone_layout.addWidget(self.phone_middle_label)
        phone_layout.addWidget(self.phone_last_label)

        self.reservation_date_input = QDateEdit(QDate.currentDate())
        self.reservation_date_input.setCalendarPopup(True)
        self.reservation_time_input = QTimeEdit(QTime.currentTime())
        self.remarks_input = QLineEdit()

        form_layout.addRow("이름", self.name_label)
        form_layout.addRow("생년월일", self.birthdate_label)
        form_layout.addRow("전화번호", phone_layout)
        form_layout.addRow("예약 날짜", self.reservation_date_input)
        form_layout.addRow("예약 시간", self.reservation_time_input)
        form_layout.addRow("비고", self.remarks_input)

        # 예약 버튼
        reserve_button = QPushButton("예약 완료")
        reserve_button.clicked.connect(self.save_reservation)

        # 메인 레이아웃 설정
        main_layout = QVBoxLayout()
        main_layout.addLayout(search_layout)
        main_layout.addWidget(self.result_table)
        main_layout.addLayout(form_layout)
        main_layout.addWidget(reserve_button, alignment=Qt.AlignCenter)

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
        self.patient_id = patient_id  # 예약 시 사용하기 위해 환자 ID 저장
        self.name_label.setText(name)
        self.birthdate_label.setText(birthdate)
        phone_parts = phone.split('-')
        self.phone_middle_label.setText(phone_parts[1])
        self.phone_last_label.setText(phone_parts[2])

    def save_reservation(self):
        # 입력된 데이터 가져오기
        reservation_date = self.reservation_date_input.date().toString("yyyy-MM-dd")
        reservation_time = self.reservation_time_input.time().toString("HH:mm:ss")
        remarks = self.remarks_input.text()

        if not hasattr(self, 'patient_id'):
            QMessageBox.warning(self, "오류", "환자를 선택해 주세요.")
            return

        # 프로젝트 루트 디렉토리의 절대 경로를 가져오기
        base_dir = os.path.dirname(os.path.abspath(__file__))
        db_path = os.path.join(base_dir, "../db/clinic.db")

        # 데이터베이스 연결
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # 예약 데이터 삽입
        cursor.execute('''INSERT INTO reservations (patient_id, reservation_date, reservation_time, remarks) 
                          VALUES (?, ?, ?, ?)''', (self.patient_id, reservation_date, reservation_time, remarks))

        conn.commit()
        conn.close()

        # 성공 메시지 출력
        QMessageBox.information(self, "성공", "예약이 완료되었습니다!")

        # 입력 필드 초기화
        self.reservation_date_input.setDate(QDate.currentDate())
        self.reservation_time_input.setTime(QTime.currentTime())
        self.remarks_input.clear()
        self.name_label.clear()
        self.birthdate_label.clear()
        self.phone_middle_label.clear()
        self.phone_last_label.clear()
