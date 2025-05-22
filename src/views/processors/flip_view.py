from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QRadioButton, 
                           QButtonGroup, QLabel)
from PyQt6.QtCore import pyqtSignal

class FlipView(QWidget):
    flip_type_changed = pyqtSignal(int)
    
    def __init__(self):
        super().__init__()
        self._setup_ui()
        
    def _setup_ui(self):
        main_layout = QVBoxLayout(self)
        
        # Create radio buttons
        self.vertical_radio = QRadioButton("Vertical Flip")
        self.horizontal_radio = QRadioButton("Horizontal Flip")
        
        # Create button group
        self.flip_group = QButtonGroup(self)
        self.flip_group.addButton(self.vertical_radio, 0)  # 0 for vertical flip
        self.flip_group.addButton(self.horizontal_radio, 1)  # 1 for horizontal flip
        
        # Connect signal
        self.flip_group.buttonClicked.connect(self._on_flip_type_changed)
        
        # Add to layout
        main_layout.addWidget(QLabel("Select Flip Type:"))
        main_layout.addWidget(self.vertical_radio)
        main_layout.addWidget(self.horizontal_radio)
        

        self.vertical_radio.setChecked(True)
        
    def _on_flip_type_changed(self, button):
        flip_type = self.flip_group.id(button)
        self.flip_type_changed.emit(flip_type)
        
    def set_flip_type(self, flip_type: int):
        if flip_type == 0:
            self.vertical_radio.setChecked(True)
        elif flip_type == 1:
            self.horizontal_radio.setChecked(True) 