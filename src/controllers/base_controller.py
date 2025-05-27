# type: ignore
from abc import ABC, abstractmethod
from typing import Any
from PyQt6.QtWidgets import QWidget
from models.base_model import BaseModel

class BaseController(ABC):
    """
    Abstract base class for all processor controllers.
    
    This class coordinates between the model and view components,
    handling communication and data flow between them.
    """
    
    def __init__(self, model: BaseModel, view: QWidget) -> None:
        """
        Initialize the controller with model and view.
        
        Args:
            model (BaseModel): The processor model instance
            view (QWidget): The processor view instance
        """
        self.model = model
        self.view = view
        self._connect_signals()

    def _connect_signals(self) -> None:
        """
        Connect signals between view and model.
        
        This method should be overridden by subclasses to establish
        specific signal-slot connections for their processor.
        """
        if hasattr(self.view, "parameters_changed"):
            self.view.parameters_changed.connect(self.model.set_parameters)

    def get_model(self) -> BaseModel:
        """
        Get the controller's model instance.
        
        Returns:
            BaseModel: The processor model
        """
        return self.model

    def get_view(self) -> QWidget:
        """
        Get the controller's view instance.
        
        Returns:
            QWidget: The processor view
        """
        return self.view
        
    def cleanup(self) -> None:
        """
        Clean up resources when controller is destroyed.
        
        This method should be called before the controller is destroyed
        to properly disconnect signals and free resources.
        """
        try:
            if hasattr(self.view, "parameters_changed"):
                self.view.parameters_changed.disconnect()
        except RuntimeError:
            # Signal already disconnected
            pass 