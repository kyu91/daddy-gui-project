from PyQt5.QtWidgets import QWidget, QVBoxLayout, QFormLayout, QLineEdit, QPushButton, QMessageBox, QHBoxLayout, QLabel, QDateEdit
from PyQt5.QtCore import Qt, QDate  # Qt 및 QDate 임포트 추가
import sqlite3
import os

class NewPatientPage(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        # 폼 레이아웃 설정
        form_layout = QFormLayout()

        # 입력 필드 생성
        self.name_input = QLineEdit()
        self.birthdate_input = QDateEdit()  # 생년월일 입력 필드를 QDateEdit으로 변경
        self.birthdate_input.setCalendarPopup(True)
        self.birthdate_input.setDisplayFormat("yyyy-MM-dd")
        self.birthdate_input.setDate(QDate.currentDate())  # 기본값을 현재 날짜로 설정

        # 전화번호 입력 필드 설정
        phone_layout = QHBoxLayout()
        self.phone_prefix = QLabel("010-")
        self.phone_middle_input = QLineEdit()
        self.phone_last_input = QLineEdit()
        self.phone_middle_input.setMaxLength(4)
        self.phone_last_input.setMaxLength(4)
        
        phone_layout.addWidget(self.phone_prefix)
        phone_layout.addWidget(self.phone_middle_input)
        phone_layout.addWidget(self.phone_last_input)

        # 폼 레이아웃에 필드 추가
        form_layout.addRow("이름", self.name_input)
        form_layout.addRow("생년월일", self.birthdate_input)  # QDateEdit 필드 추가
        form_layout.addRow("전화번호", phone_layout)

        # 등록 버튼 생성
        submit_button = QPushButton("환자 등록")
        submit_button.clicked.connect(self.save_patient)

        # 메인 레이아웃 설정
        main_layout = QVBoxLayout()
        main_layout.addLayout(form_layout)
        main_layout.addWidget(submit_button, alignment=Qt.AlignCenter)

        self.setLayout(main_layout)

    def save_patient(self):
        # 입력된 데이터 가져오기
        name = self.name_input.text()
        birthdate = self.birthdate_input.date().toString("yyyy-MM-dd")  # 날짜 형식으로 저장
        phone = f"010-{self.phone_middle_input.text()}-{self.phone_last_input.text()}"

        # 데이터 검증 (전화번호 입력이 올바른지 확인)
        if len(self.phone_middle_input.text()) != 4 or len(self.phone_last_input.text()) != 4:
            QMessageBox.warning(self, "오류", "전화번호를 올바르게 입력해 주세요.")
            return

        # 프로젝트 루트 디렉토리의 절대 경로를 가져오기
        base_dir = os.path.dirname(os.path.abspath(__file__))
        db_path = os.path.join(base_dir, "../db/clinic.db")

        # 데이터베이스 연결
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # 중복 확인
        cursor.execute("SELECT id FROM patients WHERE name=? AND phone=? AND birthdate=?", (name, phone, birthdate))
        patient = cursor.fetchone()

        if patient:
            QMessageBox.warning(self, "오류", "이미 등록된 환자입니다.")
        else:
            # 환자 데이터 삽입
            cursor.execute("INSERT INTO patients (name, phone, birthdate) VALUES (?, ?, ?)", (name, phone, birthdate))
            conn.commit()
            QMessageBox.information(self, "성공", "환자가 성공적으로 등록되었습니다.")
        
        conn.close()

        # 입력 필드 초기화
        self.name_input.clear()
        self.birthdate_input.setDate(QDate.currentDate())  # 초기화 시 현재 날짜로 설정
        self.phone_middle_input.clear()
        self.phone_last_input.clear()
