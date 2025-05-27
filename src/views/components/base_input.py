from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QSpinBox
from PyQt6.QtCore import pyqtSignal

class BaseInput(QWidget):
    def __init__(self, label: str):
        super().__init__()
        self.label = label
        self._setup_ui()
        
    def _setup_ui(self):
        self.layout = QVBoxLayout(self)
        self.label_widget = QLabel(self.label)
        self.layout.addWidget(self.label_widget)
        
    def get_value(self):
        raise NotImplementedError("Subclasses must implement get_value()")
        
    def set_value(self, value):
        raise NotImplementedError("Subclasses must implement set_value()")

class TextInput(BaseInput):
    def __init__(self, label: str, placeholder: str = ""):
        super().__init__(label)
        self.input = QLineEdit()
        self.input.setPlaceholderText(placeholder)
        self.layout.addWidget(self.input)
        
    def get_value(self) -> str:
        return self.input.text()
        
    def set_value(self, value: str):
        self.input.setText(str(value))
        
    @property
    def textChanged(self):
        return self.input.textChanged

class SpinBoxInput(BaseInput):
    def __init__(self, label: str, min_val: int, max_val: int, default_val: int = 0):
        super().__init__(label)
        self.input = QSpinBox()
        self.input.setRange(min_val, max_val)
        self.input.setValue(default_val)
        self.layout.addWidget(self.input)
        
    def get_value(self) -> int:
        return self.input.value()
        
    def set_value(self, value: int):
        self.input.setValue(value) 