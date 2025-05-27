from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QSpinBox, QComboBox
from PyQt6.QtCore import Qt, pyqtSignal
from .base_processor_view import BaseProcessorView
from ..components.base_input import SpinBoxInput

class RotationView(BaseProcessorView):
    rotation_type_changed = pyqtSignal(str)  # Keep this signal for controller compatibility
    
    def __init__(self):
        super().__init__("Rotation")
        self._setup_rotation_ui()
        
    def _setup_rotation_ui(self):
        # Create horizontal layout for inputs
        input_layout = self._create_horizontal_layout()
        
        # Degree input
        degree_container = self._create_vertical_layout()
        degree_label = QLabel("Degree:")
        self.degree_input = QSpinBox()
        self.degree_input.setRange(-360, 360)  # Allow negative values for counter-clockwise
        self.degree_input.setValue(0)
        self.degree_input.valueChanged.connect(self._on_parameter_changed)
        degree_container.addWidget(degree_label)
        degree_container.addWidget(self.degree_input)
        input_layout.addWidget(degree_container.parent())
        
        # Rotation type selection
        self.rotation_type = self._create_combobox("Rotation Type:", ["Center", "Origin"])
        self.rotation_type.currentIndexChanged.connect(self._on_rotation_type_changed)
        
    def _on_rotation_type_changed(self, index: int):
        rotation_type = "center" if index == 0 else "origin"
        self.rotation_type_changed.emit(rotation_type)
        self._on_parameter_changed()
        
    def _on_parameter_changed(self):
        parameters = self.get_parameters()
        self._emit_parameters(parameters)
        
    def get_parameters(self) -> dict:
        return {
            "degree": self.degree_input.value(),
            "rotation_type": "center" if self.rotation_type.currentIndex() == 0 else "origin"
        }
        
    def reset(self):
        self.degree_input.setValue(0)
        self.rotation_type.setCurrentIndex(0)
        
    def cleanup(self):
        if hasattr(self, 'degree_input'):
            try:
                self.degree_input.valueChanged.disconnect()
            except:
                pass
        if hasattr(self, 'rotation_type'):
            try:
                self.rotation_type.currentIndexChanged.disconnect()
            except:
                pass
        try:
            self.rotation_type_changed.disconnect()
        except:
            pass
        super().cleanup() 