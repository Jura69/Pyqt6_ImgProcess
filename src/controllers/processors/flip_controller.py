from controllers.base_controller import BaseController
from models.processors.flip_model import FlipModel
from views.processors.flip_view import FlipView

class FlipController(BaseController):
    """
    Controller for flip image processing.
    
    Coordinates between FlipModel and FlipView to handle
    image flipping operations.
    """
    
    def __init__(self) -> None:
        """Initialize flip controller with model and view."""
        model = FlipModel()
        view = FlipView()
        super().__init__(model, view)

    def _connect_signals(self) -> None:
        """Connect flip-specific signals between view and model."""
        super()._connect_signals()
        if hasattr(self.view, 'parameters_changed'):
            self.view.parameters_changed.connect(self.model.set_parameters)