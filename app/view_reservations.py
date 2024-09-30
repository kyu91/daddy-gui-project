# view_reservations.py

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, QCalendarWidget, QCheckBox, QMessageBox, QHBoxLayout, QDialog, QLabel
from PyQt5.QtGui import QTextCharFormat, QFont, QColor
from PyQt5.QtCore import QDate
import sqlite3
import os

class ViewReservationsPage(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        main_layout = QVBoxLayout()

        # 달력으로 보기 / 표로 보기 버튼 생성
        self.calendar_button = QPushButton("달력으로 보기")
        self.table_button = QPushButton("표로 보기")
        self.calendar_button.clicked.connect(self.show_calendar_view)
        self.table_button.clicked.connect(self.show_table_view)

        # '선택 항목 삭제' 버튼 생성
        self.delete_button = QPushButton("선택 항목 삭제")
        self.delete_button.clicked.connect(self.delete_selected_reservations)

        # 버튼 레이아웃 추가
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.calendar_button)
        button_layout.addWidget(self.table_button)
        button_layout.addWidget(self.delete_button)

        # 테이블 위젯 생성 (초기 상태는 표로 보기)
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["선택", "예약번호", "환자 이름", "예약 날짜", "예약 시간"])

        # 달력 위젯 생성 (기본적으로 숨김)
        self.calendar = QCalendarWidget()
        self.calendar.setVisible(False)
        self.calendar.clicked.connect(self.show_reservation_popup)  # 날짜 클릭 시 팝업 표시

        # 달력 좌측의 넘버링(주 번호) 제거
        self.calendar.setVerticalHeaderFormat(QCalendarWidget.NoVerticalHeader)

        # 메인 레이아웃에 위젯 추가
        main_layout.addLayout(button_layout)
        main_layout.addWidget(self.calendar)
        main_layout.addWidget(self.table)

        self.setLayout(main_layout)

    def showEvent(self, event):
        self.load_reservations()
        super().showEvent(event)

    def load_reservations(self):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        db_path = os.path.join(base_dir, "../db/clinic.db")

        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        cursor.execute('''
            SELECT reservations.id, patients.name, reservations.reservation_date, reservations.reservation_time
            FROM reservations
            JOIN patients ON reservations.patient_id = patients.id
        ''')
        rows = cursor.fetchall()

        self.table.setRowCount(len(rows))
        self.reservations = {}  # 날짜별 예약 정보를 저장할 딕셔너리

        for i, row in enumerate(rows):
            checkbox_item = QTableWidgetItem()
            checkbox_item.setCheckState(False)
            self.table.setItem(i, 0, checkbox_item)  # 체크박스 추가
            for j, value in enumerate(row):
                self.table.setItem(i, j + 1, QTableWidgetItem(str(value)))

            # 예약 날짜를 기준으로 딕셔너리에 저장
            reservation_date = row[2]
            if reservation_date not in self.reservations:
                self.reservations[reservation_date] = []
            self.reservations[reservation_date].append(f"{row[1]}: {row[3]}")  # 이름과 시간 추가

        conn.close()

        # 달력에 예약 정보 표시
        self.update_calendar_reservations()

    def update_calendar_reservations(self):
        """예약이 있는 날짜의 글씨를 기본 크기로 돌리기"""
        for reservation_date, details in self.reservations.items():
            # 날짜를 QDate 객체로 변환
            date_parts = list(map(int, reservation_date.split("-")))
            qdate = QDate(date_parts[0], date_parts[1], date_parts[2])

            # 예약이 있는 날짜의 텍스트 포맷 설정 (기본 크기로 설정)
            format = QTextCharFormat()
            format.setFont(QFont())  # 기본 폰트 설정 (사이즈나 스타일 변경하지 않음)
            format.setForeground(QColor("red"))  # 텍스트 색상만 설정
            self.calendar.setDateTextFormat(qdate, format)

    def show_calendar_view(self):
        self.table.setVisible(False)  # 테이블 숨기기
        self.calendar.setVisible(True)  # 달력 표시

    def show_table_view(self):
        self.calendar.setVisible(False)  # 달력 숨기기
        self.table.setVisible(True)  # 테이블 표시

    def show_reservation_popup(self, date):
        """클릭한 날짜의 예약 정보를 팝업으로 표시하는 함수"""
        selected_date = date.toString("yyyy-MM-dd")
        if selected_date in self.reservations:
            reservations_for_date = "\n".join(self.reservations[selected_date])
            self.show_popup(f"{selected_date} 예약자", reservations_for_date)
        else:
            self.show_popup(f"{selected_date}", "예약이 없습니다.")

    def show_popup(self, title, message):
        """예약 정보를 팝업으로 표시하는 함수"""
        dialog = QDialog(self)
        dialog.setWindowTitle(title)
        layout = QVBoxLayout()
        label = QLabel(message)
        layout.addWidget(label)
        dialog.setLayout(layout)
        dialog.exec_()

    def delete_selected_reservations(self):
        selected_ids = []
        for i in range(self.table.rowCount()):
            if self.table.item(i, 0).checkState() == 2:  # 체크박스 체크 상태 확인
                reservation_id = self.table.item(i, 1).text()
                selected_ids.append(reservation_id)

        if not selected_ids:
            QMessageBox.warning(self, "오류", "삭제할 항목을 선택해 주세요.")
            return

        confirmation = QMessageBox.question(
            self, "삭제 확인", "선택한 예약을 삭제하시겠습니까?",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )

        if confirmation == QMessageBox.Yes:
            base_dir = os.path.dirname(os.path.abspath(__file__))
            db_path = os.path.join(base_dir, "../db/clinic.db")

            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()

            cursor.executemany("DELETE FROM reservations WHERE id = ?", [(id,) for id in selected_ids])

            conn.commit()
            conn.close()

            QMessageBox.information(self, "성공", "선택한 예약이 삭제되었습니다.")

            # 테이블 갱신
            self.load_reservations()
