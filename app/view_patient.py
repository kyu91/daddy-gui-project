# view_patient.py

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, QCheckBox, QMessageBox
import sqlite3
import os

class ViewPatientsPage(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # 메인 레이아웃 설정
        main_layout = QVBoxLayout()

        # '선택 항목 삭제' 버튼 생성
        delete_button = QPushButton("선택 항목 삭제")
        delete_button.clicked.connect(self.delete_selected_patients)

        # 테이블 위젯 생성
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["선택", "고유 번호", "이름", "생년월일", "전화번호"])

        # 메인 레이아웃에 위젯 추가
        main_layout.addWidget(delete_button)
        main_layout.addWidget(self.table)

        self.setLayout(main_layout)

    def showEvent(self, event):
        self.load_patients()
        super().showEvent(event)

    def load_patients(self):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        db_path = os.path.join(base_dir, "../db/clinic.db")

        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        cursor.execute("SELECT id, name, birthdate, phone FROM patients")
        rows = cursor.fetchall()

        self.table.setRowCount(len(rows))
        for i, row in enumerate(rows):
            checkbox_item = QTableWidgetItem()
            checkbox_item.setCheckState(False)
            self.table.setItem(i, 0, checkbox_item)  # 체크박스 추가
            for j, value in enumerate(row):
                self.table.setItem(i, j + 1, QTableWidgetItem(str(value)))

        conn.close()

    def delete_selected_patients(self):
        selected_ids = []
        for i in range(self.table.rowCount()):
            if self.table.item(i, 0).checkState() == 2:  # 체크박스 체크 상태 확인
                patient_id = self.table.item(i, 1).text()
                selected_ids.append(patient_id)

        if not selected_ids:
            QMessageBox.warning(self, "오류", "삭제할 항목을 선택해 주세요.")
            return

        confirmation = QMessageBox.question(
            self, "삭제 확인", "선택한 환자를 삭제하시겠습니까? 이 작업은 취소할 수 없습니다.",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )

        if confirmation == QMessageBox.Yes:
            base_dir = os.path.dirname(os.path.abspath(__file__))
            db_path = os.path.join(base_dir, "../db/clinic.db")

            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()

            # 환자 삭제 (예약 정보도 함께 삭제해야 할 수 있음)
            cursor.executemany("DELETE FROM patients WHERE id = ?", [(id,) for id in selected_ids])

            conn.commit()
            conn.close()

            QMessageBox.information(self, "성공", "선택한 환자가 삭제되었습니다.")

            # 테이블 갱신
            self.load_patients()