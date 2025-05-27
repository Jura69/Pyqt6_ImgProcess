from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton
from PyQt6.QtCore import pyqtSignal
from views.components.base_input import TextInput
from views.components.error_message import ErrorMessage

class CropView(QWidget):
    parameters_changed = pyqtSignal(dict)
    
    def __init__(self):
        super().__init__()
        self._setup_ui()
        
    def _setup_ui(self):
        layout = QVBoxLayout(self)
        
        # Title
        title = QLabel("Crop Image")
        title.setStyleSheet("font-size: 16px; font-weight: bold;")
        layout.addWidget(title)
        
        # Coordinate inputs
        coord_layout = QVBoxLayout()
        
        # X coordinates
        x_layout = QHBoxLayout()
        self.x1_input = TextInput("X1")
        self.x2_input = TextInput("X2")
        x_layout.addWidget(self.x1_input)
        x_layout.addWidget(self.x2_input)
        coord_layout.addLayout(x_layout)
        
        # Y coordinates
        y_layout = QHBoxLayout()
        self.y1_input = TextInput("Y1")
        self.y2_input = TextInput("Y2")
        y_layout.addWidget(self.y1_input)
        y_layout.addWidget(self.y2_input)
        coord_layout.addLayout(y_layout)
        
        layout.addLayout(coord_layout)
        
        # Validation message
        self.error_message = ErrorMessage()
        layout.addWidget(self.error_message)
        
        # Connect signals
        self.x1_input.textChanged.connect(self._on_parameter_changed)
        self.x2_input.textChanged.connect(self._on_parameter_changed)
        self.y1_input.textChanged.connect(self._on_parameter_changed)
        self.y2_input.textChanged.connect(self._on_parameter_changed)
        
    def _validate_coordinates(self) -> bool:
        try:
            x1 = int(self.x1_input.get_value())
            x2 = int(self.x2_input.get_value())
            y1 = int(self.y1_input.get_value())
            y2 = int(self.y2_input.get_value())
            
            # Check if coordinates are positive
            if any(coord < 0 for coord in [x1, x2, y1, y2]):
                self.error_message.show_message("Coordinates must be positive numbers")
                return False
                
            # Check if coordinates form a valid rectangle
            if x1 >= x2:
                self.error_message.show_message("X1 must be less than X2")
                return False
                
            if y1 >= y2:
                self.error_message.show_message("Y1 must be less than Y2")
                return False
                
            self.error_message.clear_message()
            return True
            
        except ValueError:
            self.error_message.show_message("Please enter valid numbers")
            return False
            
    def _on_parameter_changed(self):
        if self._validate_coordinates():
            self._emit_parameters()
            
    def _emit_parameters(self):
        parameters = self.get_parameters()
        self.parameters_changed.emit(parameters)
        
    def get_parameters(self) -> dict:
        try:
            return {
                "x1": int(self.x1_input.get_value()),
                "x2": int(self.x2_input.get_value()),
                "y1": int(self.y1_input.get_value()),
                "y2": int(self.y2_input.get_value())
            }
        except ValueError:
            return {
                "x1": 0,
                "x2": 0,
                "y1": 0,
                "y2": 0
            }
            
    def reset(self):
        self.x1_input.set_value("0")
        self.x2_input.set_value("0")
        self.y1_input.set_value("0")
        self.y2_input.set_value("0")
        self.error_message.clear_message() 