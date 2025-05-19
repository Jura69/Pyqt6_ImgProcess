from controllers.base_controller import BaseController
from models.processors.rotation_model import RotationModel
from views.rotation_view import RotationView

class RotationController(BaseController):
    def __init__(self):
        processor = RotationModel()
        controls = RotationView()
        super().__init__(processor, controls)

    def _connect_signals(self):
        self.controls.rotation_type_changed.connect(self.processor.set_rotation_type)
        self.controls.parameters_changed.connect(self.processor.set_parameters) 