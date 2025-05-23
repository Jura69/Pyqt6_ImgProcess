from PyQt6.QtWidgets import QLabel

class SucessMessage(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        # Hiển thị thông báo lỗi (màu đỏ)
        self.setStyleSheet("color: green; font-weight: bold;")
        self.setText("")
        self.hide()

    def show_message(self, message: str):
        # Hiện thông báo
        self.setText(message)
        self.show()

    def clear_message(self):
        # Ẩn thông báo
        self.setText("")
        self.hide() 