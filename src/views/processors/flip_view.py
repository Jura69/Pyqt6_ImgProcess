from PyQt6.QtWidgets import QLabel, QRadioButton, QButtonGroup
from PyQt6.QtCore import Qt, pyqtSignal
from .base_processor_view import BaseProcessorView

class FlipView(BaseProcessorView):
    flip_type_changed = pyqtSignal(int)  # Keep this signal for controller compatibility
    
    def __init__(self):
        super().__init__("Flip")
        self._setup_flip_ui()
        
    def _setup_flip_ui(self):
        # Create vertical layout for radio buttons
        radio_layout = self._create_vertical_layout()
        
        # Add label
        label = QLabel("Flip Direction:")
        radio_layout.addWidget(label)
        
        # Create radio buttons
        self.vertical_radio = QRadioButton("Vertical")
        self.horizontal_radio = QRadioButton("Horizontal")
        self.vertical_radio.setChecked(True)
        
        # Create button group
        self.button_group = QButtonGroup(self)  # Set parent to self
        self.button_group.addButton(self.vertical_radio)
        self.button_group.addButton(self.horizontal_radio)
        self.button_group.buttonClicked.connect(self._on_flip_type_changed)
        
        # Add radio buttons to layout
        radio_layout.addWidget(self.vertical_radio)
        radio_layout.addWidget(self.horizontal_radio)
        
    def _on_flip_type_changed(self, button):
        flip_type = 0 if button == self.vertical_radio else 1
        self.flip_type_changed.emit(flip_type)
        self._on_parameter_changed()
        
    def _on_parameter_changed(self):
        parameters = self.get_parameters()
        self._emit_parameters(parameters)
        
    def get_parameters(self) -> dict:
        return {
            "flip_type": 0 if self.vertical_radio.isChecked() else 1
        }
        
    def reset(self):
        self.vertical_radio.setChecked(True)
        
    def cleanup(self):
        if hasattr(self, 'button_group'):
            try:
                self.button_group.buttonClicked.disconnect()
            except:
                pass
        try:
            self.flip_type_changed.disconnect()
        except:
            pass
        super().cleanup() 