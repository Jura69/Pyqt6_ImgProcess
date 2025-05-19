from controllers.base_controller import BaseController
from models.processors.crop_model import CropModel
from views.processors.crop_view import CropView

class CropController(BaseController):
    def __init__(self):
        models = CropModel()
        views = CropView()
        super().__init__(models, views) 