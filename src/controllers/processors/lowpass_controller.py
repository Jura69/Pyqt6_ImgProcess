from controllers.base_controller import BaseController
from models.processors.lowpass_model import LowpassModel
from views.processors.lowpass_view import LowpassView

class LowpassController(BaseController):
    """
    Controller for lowpass filter image processing.
    
    Coordinates between LowpassModel and LowpassView to handle
    lowpass filtering operations with various filter types.
    """
    
    def __init__(self) -> None:
        """Initialize lowpass controller with model and view."""
        model = LowpassModel()
        view = LowpassView()
        super().__init__(model, view)

    def _connect_signals(self) -> None:
        """Connect lowpass-specific signals between view and model."""
        super()._connect_signals()
        
        # Connect parameter changes from view to model
        if hasattr(self.view, 'parameters_changed'):
            self.view.parameters_changed.connect(self.model.set_parameters)
            
        # Connect filter type changes specifically
        if hasattr(self.view, 'filter_combo'):
            self.view.filter_combo.currentTextChanged.connect(self._on_filter_type_changed)
            
    def _on_filter_type_changed(self, filter_type: str) -> None:
        """
        Handle filter type change from view.
        
        Args:
            filter_type (str): Selected filter type
        """
        try:
            self.model.set_filter_type(filter_type)
        except ValueError as e:
            # Log error but don't crash
            import logging
            logging.warning(f"Invalid filter type selected: {e}")
            
    def set_filter_parameters(self, filter_type: str, kernel_size: int) -> None:
        """
        Set filter parameters programmatically.
        
        Args:
            filter_type (str): Type of filter to use
            kernel_size (int): Size of the kernel
        """
        try:
            # Update model
            parameters = {
                "filter_type": filter_type,
                "kernel_size": kernel_size
            }
            self.model.set_parameters(parameters)
            
            # Update view
            if hasattr(self.view, 'set_filter_type'):
                self.view.set_filter_type(filter_type)
            if hasattr(self.view, 'set_kernel_size'):
                self.view.set_kernel_size(kernel_size)
                
        except ValueError as e:
            import logging
            logging.error(f"Failed to set filter parameters: {e}")
            
    def get_available_filters(self) -> list:
        """
        Get list of available filter types.
        
        Returns:
            list: Available filter types
        """
        return ["gaussian", "average", "median", "min", "max"] 