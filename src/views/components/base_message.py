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
        """Get background color based on message type."""
        color_map = {
            "success": "#4CAF50",  # Green
            "error": "#f44336",    # Red
            "warning": "#FFD700"   # Yellow
        }
        return color_map.get(self.message_type, "#2196F3")  # Default blue
        
    def show_message(self, message: str):
        self.setText(message)
        self.show()
        
    def clear_message(self):
        self.setText("")
        self.hide() 