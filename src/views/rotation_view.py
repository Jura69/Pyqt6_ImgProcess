from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QSpinBox, QComboBox
from PyQt6.QtCore import pyqtSignal

class RotationView(QWidget):
    """Controls for rotation processor"""
    
    # Signals
    parameters_changed = pyqtSignal(dict)
    rotation_type_changed = pyqtSignal(str)
    
    def __init__(self):
        super().__init__()
        self._init_ui()
        
    def _init_ui(self):
        layout = QVBoxLayout()
        
        # Rotation type selection
        type_layout = QHBoxLayout()
        type_label = QLabel("Rotation Type:")
        self.type_combo = QComboBox()
        self.type_combo.addItems(["Center", "Origin"])
        self.type_combo.currentTextChanged.connect(self._on_type_changed)
        
        type_layout.addWidget(type_label)
        type_layout.addWidget(self.type_combo)
        layout.addLayout(type_layout)
        
        # Degree selection
        degree_layout = QHBoxLayout()
        degree_label = QLabel("Degree:")
        self.degree_spin = QSpinBox()
        self.degree_spin.setRange(-360, 360)
        self.degree_spin.setValue(0)
        self.degree_spin.valueChanged.connect(self._on_parameters_changed)
        
        degree_layout.addWidget(degree_label)
        degree_layout.addWidget(self.degree_spin)
        layout.addLayout(degree_layout)
        
        self.setLayout(layout)
        
    def _on_type_changed(self, rotation_type: str):
        """Handle rotation type change"""
        self.rotation_type_changed.emit(rotation_type.lower())
        self._on_parameters_changed()
        
    def _on_parameters_changed(self):
        """Handle parameter changes"""
        params = {
            "degree": self.degree_spin.value()
        }
        self.parameters_changed.emit(params) 