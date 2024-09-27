# main.py

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QHBoxLayout, QWidget, QStackedWidget, QLabel
from new_patient import NewPatientPage
from make_reservation import MakeReservationPage
from view_reservations import ViewReservationsPage
from patient_details import PatientDetailsPage
from view_patient import ViewPatientsPage  # 전체 환자 보기 페이지 임포트

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Massage Clinic Management System")
        self.setGeometry(100, 100, 800, 600)

        # 상단 메뉴바 레이아웃 생성
        menu_bar_layout = QHBoxLayout()

        # 버튼 생성
        home_button = QPushButton("Home")
        new_patient_button = QPushButton("신규 환자 등록")
        make_reservation_button = QPushButton("예약하기")
        view_reservations_button = QPushButton("예약 내역 보기")  # 예약 내역 보기 버튼을 먼저 추가
        view_patients_button = QPushButton("전체 환자 보기")  # 전체 환자 보기 버튼을 그 다음에 추가
        patient_details_button = QPushButton("환자별 상세 정보")

        # 버튼들을 상단 메뉴바에 추가
        menu_bar_layout.addWidget(home_button)
        menu_bar_layout.addWidget(new_patient_button)
        menu_bar_layout.addWidget(make_reservation_button)
        menu_bar_layout.addWidget(view_reservations_button)  # 순서 변경
        menu_bar_layout.addWidget(view_patients_button)  # 순서 변경
        menu_bar_layout.addWidget(patient_details_button)

        # 중앙 위젯 및 레이아웃 설정
        central_widget = QWidget()
        central_layout = QVBoxLayout(central_widget)
        
        # 상단 메뉴바 추가
        central_layout.addLayout(menu_bar_layout)

        # 스택 위젯 생성 (여러 페이지를 관리하기 위해)
        self.stack = QStackedWidget()
        
        # 각 페이지 위젯 생성
        self.home_page = QLabel("안녕?")  # Home 페이지
        self.new_patient_page = NewPatientPage()  # 신규 환자 등록 페이지
        self.make_reservation_page = MakeReservationPage()  # 예약하기 페이지
        self.view_patients_page = ViewPatientsPage()  # 전체 환자 보기 페이지
        self.view_reservations_page = ViewReservationsPage()  # 예약 내역 보기 페이지
        self.patient_details_page = PatientDetailsPage()  # 환자별 상세 정보 페이지

        # 스택 위젯에 페이지 추가
        self.stack.addWidget(self.home_page)
        self.stack.addWidget(self.new_patient_page)
        self.stack.addWidget(self.make_reservation_page)
        self.stack.addWidget(self.view_reservations_page)  # 순서 변경
        self.stack.addWidget(self.view_patients_page)  # 순서 변경
        self.stack.addWidget(self.patient_details_page)

        # 스택 위젯을 중앙 레이아웃에 추가
        central_layout.addWidget(self.stack)

        self.setCentralWidget(central_widget)

        # 버튼 클릭 시 페이지 변경
        home_button.clicked.connect(lambda: self.stack.setCurrentWidget(self.home_page))
        new_patient_button.clicked.connect(lambda: self.stack.setCurrentWidget(self.new_patient_page))
        make_reservation_button.clicked.connect(lambda: self.stack.setCurrentWidget(self.make_reservation_page))
        view_reservations_button.clicked.connect(lambda: self.stack.setCurrentWidget(self.view_reservations_page))  # 예약 내역 보기 버튼 연결
        view_patients_button.clicked.connect(lambda: self.stack.setCurrentWidget(self.view_patients_page))  # 전체 환자 보기 버튼 연결
        patient_details_button.clicked.connect(lambda: self.stack.setCurrentWidget(self.patient_details_page))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())