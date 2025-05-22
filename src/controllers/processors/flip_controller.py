from PyQt6.QtWidgets import QWidget
from models.processors.flip_model import FlipModel
from views.processors.flip_view import FlipView
from controllers.base_controller import BaseController

class FlipController(BaseController):
    def __init__(self):
        models = FlipModel()
        views = FlipView()
        super().__init__(models, views)

    def _connect_signals(self):
        self.views.flip_type_changed.connect(self.models.set_flip_type)
        super()._connect_signals()