# view_reservations.py

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, QHBoxLayout, QCheckBox, QMessageBox
import sqlite3
import os

class ViewReservationsPage(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        main_layout = QVBoxLayout()

        delete_button = QPushButton("선택 항목 삭제")
        delete_button.clicked.connect(self.delete_selected_reservations)

        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["선택", "예약번호", "환자 이름", "예약 날짜", "예약 시간"])

        main_layout.addWidget(delete_button)
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
        for i, row in enumerate(rows):
            checkbox_item = QTableWidgetItem()
            checkbox_item.setCheckState(False)
            self.table.setItem(i, 0, checkbox_item)  # 체크박스 추가
            for j, value in enumerate(row):
                self.table.setItem(i, j + 1, QTableWidgetItem(str(value)))

        conn.close()

    def delete_selected_reservations(self):
        selected_ids = []
        for i in range(self.table.rowCount()):
            if self.table.item(i, 0).checkState() == 2:  # 체크박스 체크 상태 확인
                reservation_id = self.table.item(i, 1).text()
                selected_ids.append(reservation_id)

        # 디버그: 선택된 예약 ID 출력
        print("Selected IDs for deletion:", selected_ids)

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

            # 디버그: 실행할 삭제 쿼리 출력
            print("Executing deletion for IDs:", selected_ids)

            cursor.executemany("DELETE FROM reservations WHERE id = ?", [(id,) for id in selected_ids])

            conn.commit()
            conn.close()

            QMessageBox.information(self, "성공", "선택한 예약이 삭제되었습니다.")

            # 테이블 갱신
            self.load_reservations()