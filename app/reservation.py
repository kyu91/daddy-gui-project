# reservation.py

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QFormLayout, QLineEdit, QPushButton, QMessageBox, QDateEdit, QTimeEdit
from PyQt5.QtCore import Qt, QDate, QTime
import sqlite3
import os

class ReservationPage(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        # 폼 레이아웃 설정
        form_layout = QFormLayout()

        # 입력 필드 생성
        self.name_input = QLineEdit()
        self.phone_input = QLineEdit()
        self.birthdate_input = QDateEdit()
        self.birthdate_input.setCalendarPopup(True)
        self.birthdate_input.setDisplayFormat("yyyy-MM-dd")
        
        # 예약 날짜와 시간 분리
        self.reservation_date_input = QDateEdit(QDate.currentDate())
        self.reservation_date_input.setCalendarPopup(True)
        self.reservation_date_input.setDisplayFormat("yyyy-MM-dd")
        self.reservation_time_input = QTimeEdit(QTime.currentTime())
        self.reservation_time_input.setDisplayFormat("HH:mm:ss")

        # 폼 레이아웃에 필드 추가
        form_layout.addRow("이름", self.name_input)
        form_layout.addRow("전화번호", self.phone_input)
        form_layout.addRow("생년월일", self.birthdate_input)
        form_layout.addRow("예약 날짜", self.reservation_date_input)
        form_layout.addRow("예약 시간", self.reservation_time_input)

        # 예약 완료 버튼 생성
        submit_button = QPushButton("예약 완료")
        submit_button.clicked.connect(self.save_reservation)

        # 메인 레이아웃 설정
        main_layout = QVBoxLayout()
        main_layout.addLayout(form_layout)
        main_layout.addWidget(submit_button, alignment=Qt.AlignCenter)

        self.setLayout(main_layout)

    def save_reservation(self):
        # 입력된 데이터 가져오기
        name = self.name_input.text()
        phone = self.phone_input.text()
        birthdate = self.birthdate_input.date().toString("yyyy-MM-dd")
        reservation_date = self.reservation_date_input.date().toString("yyyy-MM-dd")
        reservation_time = self.reservation_time_input.time().toString("HH:mm:ss")

        # 프로젝트 루트 디렉토리의 절대 경로를 가져오기
        base_dir = os.path.dirname(os.path.abspath(__file__))
        db_path = os.path.join(base_dir, "../db/clinic.db")

        # 데이터베이스 연결
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # 테이블이 존재하지 않으면 생성 (예약 날짜와 시간 칼럼 분리)
        cursor.execute('''CREATE TABLE IF NOT EXISTS reservations (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            name TEXT,
                            phone TEXT,
                            birthdate TEXT,
                            reservation_date TEXT,
                            reservation_time TEXT
                          )''')

        # 데이터 삽입
        cursor.execute('''INSERT INTO reservations (name, phone, birthdate, reservation_date, reservation_time)
                          VALUES (?, ?, ?, ?, ?)''', (name, phone, birthdate, reservation_date, reservation_time))

        conn.commit()
        conn.close()

        # 성공 메시지 출력
        QMessageBox.information(self, "성공", "예약이 완료되었습니다!")

        # 입력 필드 초기화
        self.name_input.clear()
        self.phone_input.clear()
        self.birthdate_input.setDate(QDate.currentDate())
        self.reservation_date_input.setDate(QDate.currentDate())
        self.reservation_time_input.setTime(QTime.currentTime())
