from controllers.base_controller import BaseController
from models.processors.fourier_model import FourierModel
from views.processors.fourier_view import FourierView

class FourierController(BaseController):
    """
    Controller for Fourier Transform processor.
    
    Coordinates between FourierModel and FourierView,
    handling parameter changes and frequency domain processing requests.
    """
    
    def __init__(self) -> None:
        """Initialize Fourier transform controller with model and view."""
        model = FourierModel()
        view = FourierView()
        super().__init__(model, view) 