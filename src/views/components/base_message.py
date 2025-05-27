from PyQt6.QtWidgets import QLabel
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor

class BaseMessage(QLabel):
    def __init__(self, message_type: str):
        super().__init__()
        self.message_type = message_type
        self._setup_ui()
        
    def _setup_ui(self):
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setStyleSheet(f"""
            QLabel {{
                padding: 10px;
                border-radius: 5px;
                color: white;
                background-color: {self._get_background_color()};
            }}
        """)
        self.hide()
        
    def _get_background_color(self) -> str:
        return "#4CAF50" if self.message_type == "success" else "#f44336"
        
    def show_message(self, message: str):
        self.setText(message)
        self.show()
        
    def clear_message(self):
        self.setText("")
        self.hide() 