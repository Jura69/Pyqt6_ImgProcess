from PyQt6.QtWidgets import QWidget
from models.processors.rotation_model import RotationModel
from views.processors.rotation_view import RotationView
from controllers.base_controller import BaseController

class RotationController(BaseController):
    def __init__(self):
        models = RotationModel()
        views = RotationView()
        super().__init__(models, views)

    def _connect_signals(self):
        # Kết nối signal rotation_type_changed từ views tới models
        self.views.rotation_type_changed.connect(self.models.set_rotation_type)
        super()._connect_signals() 