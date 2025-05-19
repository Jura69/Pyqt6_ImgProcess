from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLineEdit, QVBoxLayout, QLabel
from PyQt6.QtCore import pyqtSignal

class CropView(QWidget):
    parameters_changed = pyqtSignal(dict)
    
    def __init__(self):
        super().__init__()
        self._setup_ui()
        
    def _setup_ui(self):
        main_layout = QVBoxLayout(self)
        input_layout = QHBoxLayout()
        
        # Tạo các trường input
        self.start_y_input = QLineEdit()
        self.start_y_input.setPlaceholderText("Start Y")
        self.end_y_input = QLineEdit()
        self.end_y_input.setPlaceholderText("End Y")
        self.start_x_input = QLineEdit()
        self.start_x_input.setPlaceholderText("Start X")
        self.end_x_input = QLineEdit()
        self.end_x_input.setPlaceholderText("End X")
        
        for input_field in [self.start_y_input, self.end_y_input, 
                          self.start_x_input, self.end_x_input]:
            input_field.textChanged.connect(self._on_parameter_changed)
        
        # Add to layout
        input_layout.addWidget(self.start_y_input)
        input_layout.addWidget(self.end_y_input)
        input_layout.addWidget(self.start_x_input)
        input_layout.addWidget(self.end_x_input)
        main_layout.addLayout(input_layout)
        
        # Label thông báo lỗi
        self.warning_label = QLabel()
        self.warning_label.setStyleSheet("color: red;")
        main_layout.addWidget(self.warning_label)
        
    def _on_parameter_changed(self):
        try:
            start_y = int(self.start_y_input.text())
            end_y = int(self.end_y_input.text())
            start_x = int(self.start_x_input.text())
            end_x = int(self.end_x_input.text())
            # Kiểm tra hợp lệ
            if start_y < 0 or end_y < 0 or start_x < 0 or end_x < 0:
                self.warning_label.setText("Tọa độ phải >= 0.")
                return
            if end_y <= start_y or end_x <= start_x:
                self.warning_label.setText("End phải lớn hơn Start.")
                return
            self.warning_label.setText("")
            parameters = {
                "start_y": start_y,
                "end_y": end_y,
                "start_x": start_x,
                "end_x": end_x
            }
            self.parameters_changed.emit(parameters)
        except ValueError:
            self.warning_label.setText("Vui lòng nhập số nguyên hợp lệ.")
            return
        
    def set_parameters(self, parameters: dict):
        self.start_y_input.setText(str(parameters.get("start_y", 0)))
        self.end_y_input.setText(str(parameters.get("end_y", 0)))
        self.start_x_input.setText(str(parameters.get("start_x", 0)))
        self.end_x_input.setText(str(parameters.get("end_x", 0))) 