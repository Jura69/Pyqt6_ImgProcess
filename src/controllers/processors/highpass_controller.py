from controllers.base_controller import BaseController
from models.processors.highpass_model import HighpassModel
from views.processors.highpass_view import HighpassView

class HighpassController(BaseController):
    """
    Controller for highpass filter processor.
    
    Coordinates between HighpassModel and HighpassView,
    handling parameter changes and processing requests.
    """
    
    def __init__(self) -> None:
        """Initialize highpass filter controller with model and view."""
        model = HighpassModel()
        view = HighpassView()
        super().__init__(model, view) 