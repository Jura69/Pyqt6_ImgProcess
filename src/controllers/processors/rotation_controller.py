from controllers.base_controller import BaseController
from models.processors.rotation_model import RotationModel
from views.processors.rotation_view import RotationView

class RotationController(BaseController):
    """
    Controller for rotation image processing.
    
    Coordinates between RotationModel and RotationView to handle
    image rotation operations.
    """
    
    def __init__(self) -> None:
        """Initialize rotation controller with model and view."""
        model = RotationModel()
        view = RotationView()
        super().__init__(model, view)

    def _connect_signals(self) -> None:
        """Connect rotation-specific signals between view and model."""
        super()._connect_signals()
        
        # Connect rotation type changes
        if hasattr(self.view, 'rotation_type_changed'):
            self.view.rotation_type_changed.connect(self.model.set_rotation_type)
            
        # Connect parameter changes
        if hasattr(self.view, 'parameters_changed'):
            self.view.parameters_changed.connect(self.model.set_parameters) 