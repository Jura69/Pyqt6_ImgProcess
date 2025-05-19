from controllers.base_controller import BaseController
from models.processors.crop_model import CropModel
from views.crop_view import CropView

class CropController(BaseController):
    def __init__(self):
        processor = CropModel()
        controls = CropView()
        super().__init__(processor, controls) 