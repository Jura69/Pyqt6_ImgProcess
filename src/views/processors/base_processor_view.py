from typing import Dict, Any
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QComboBox, QHBoxLayout
from PyQt6.QtCore import pyqtSignal
import logging

class BaseProcessorView(QWidget):
    """
    Base class for all processor view widgets.
    
    This class provides common functionality for processor UI components
    including parameter management and signal handling.
    """
    
    parameters_changed = pyqtSignal(dict)
    
    def __init__(self, title: str) -> None:
        """
        Initialize the base processor view.
        
        Args:
            title (str): Display title for this processor
        """
        super().__init__()
        self.title = title
        self._setup_ui()
        
    def _setup_ui(self) -> None:
        """Set up the basic UI structure."""
        self.layout = QVBoxLayout(self)
        self.title_label = QLabel(self.title)
        self.title_label.setStyleSheet("font-weight: bold; font-size: 14px;")
        self.layout.addWidget(self.title_label)
        
    def _create_combobox(self, label: str, options: list) -> QComboBox:
        """
        Create a labeled combobox widget.
        
        Args:
            label (str): Label text for the combobox
            options (list): List of options for the combobox
            
        Returns:
            QComboBox: Configured combobox widget
        """
        container = QWidget()
        layout = QVBoxLayout(container)
        
        label_widget = QLabel(label)
        layout.addWidget(label_widget)
        
        combobox = QComboBox()
        combobox.addItems(options)
        layout.addWidget(combobox)
        
        self.layout.addWidget(container)
        return combobox
        
    def _create_horizontal_layout(self) -> QHBoxLayout:
        """
        Create a horizontal layout container.
        
        Returns:
            QHBoxLayout: Horizontal layout added to main layout
        """
        container = QWidget()
        layout = QHBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        self.layout.addWidget(container)
        return layout
        
    def _create_vertical_layout(self) -> QVBoxLayout:
        """
        Create a vertical layout container.
        
        Returns:
            QVBoxLayout: Vertical layout added to main layout
        """
        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        self.layout.addWidget(container)
        return layout
        
    def _emit_parameters(self, parameters: Dict[str, Any]) -> None:
        """
        Emit parameters with validation.
        
        Args:
            parameters (Dict[str, Any]): Parameters to emit
        """
        if not isinstance(parameters, dict):
            logging.error("Parameters must be a dictionary")
            return
        self.parameters_changed.emit(parameters)
        
    def get_parameters(self) -> Dict[str, Any]:
        """
        Get current parameters from the view.
        
        Returns:
            Dict[str, Any]: Current parameter values
        """
        raise NotImplementedError("Subclasses must implement get_parameters method")
        
    def reset(self) -> None:
        """Reset view to initial state."""
        raise NotImplementedError("Subclasses must implement reset method")
        
    def cleanup(self) -> None:
        """
        Clean up resources before deletion.
        
        This method should be called before the view is destroyed
        to properly disconnect signals and free resources.
        """
        # Disconnect all signals
        try:
            self.parameters_changed.disconnect()
        except Exception as e:
            logging.debug(f"Error disconnecting signals: {e}")
            
        # Clear layout
        while self.layout.count():
            item = self.layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
                
    def __del__(self) -> None:
        """Destructor to ensure cleanup."""
        self.cleanup() 
        