from controllers.base_controller import BaseController
from models.processors.crop_model import CropModel
from views.processors.crop_view import CropView

class CropController(BaseController):
    """
    Controller for crop image processing.
    
    Coordinates between CropModel and CropView to handle
    image cropping operations.
    """
    
    def __init__(self) -> None:
        """Initialize crop controller with model and view."""
        model = CropModel()
        view = CropView()
        super().__init__(model, view)

    def _connect_signals(self) -> None:
        """Connect crop-specific signals between view and model."""
        super()._connect_signals()
        if hasattr(self.view, 'parameters_changed'):
            self.view.parameters_changed.connect(self.model.set_parameters)