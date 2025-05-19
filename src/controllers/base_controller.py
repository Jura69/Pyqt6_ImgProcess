from PyQt6.QtWidgets import QWidget

class BaseController:
    def __init__(self, processor, controls):
        self.processor = processor
        self.controls = controls
        self._connect_signals()

    def _connect_signals(self):
        if hasattr(self.controls, "parameters_changed"):
            self.controls.parameters_changed.connect(self.processor.set_parameters)

    def get_processor(self):
        return self.processor

    def get_controls(self):
        return self.controls 