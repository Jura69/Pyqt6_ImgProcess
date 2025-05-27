from typing import Dict, Any
from PyQt6.QtWidgets import QComboBox, QSlider, QLabel, QWidget, QVBoxLayout
from PyQt6.QtCore import Qt
from views.processors.base_processor_view import BaseProcessorView

class LowpassView(BaseProcessorView):
    """
    View for lowpass filter processor controls.
    
    Provides UI controls for selecting filter type and kernel size
    for lowpass filtering operations.
    """
    
    def __init__(self) -> None:
        """Initialize lowpass filter view."""
        super().__init__("Lowpass Filter")
        self._setup_lowpass_controls()
        
    def _setup_lowpass_controls(self) -> None:
        """Set up lowpass filter specific controls."""
        # Filter type selection
        self.filter_combo = self._create_combobox(
            "Filter Type:",
            ["gaussian", "average", "median", "min", "max"]
        )
        self.filter_combo.currentTextChanged.connect(self._on_filter_type_changed)
        
        # Kernel size selection
        self._create_kernel_size_controls()
        
    def _create_kernel_size_controls(self) -> None:
        """Create kernel size slider controls."""
        container = QWidget()
        layout = QVBoxLayout(container)
        
        # Label
        self.kernel_label = QLabel("Kernel Size: 3")
        layout.addWidget(self.kernel_label)
        
        # Slider
        self.kernel_slider = QSlider(Qt.Orientation.Horizontal)
        self.kernel_slider.setMinimum(3)
        self.kernel_slider.setMaximum(15)
        self.kernel_slider.setValue(3)
        self.kernel_slider.setSingleStep(2)  # Ensure odd values
        self.kernel_slider.valueChanged.connect(self._on_kernel_size_changed)
        layout.addWidget(self.kernel_slider)
        
        self.layout.addWidget(container)
        
    def _on_filter_type_changed(self, filter_type: str) -> None:
        """
        Handle filter type selection change.
        
        Args:
            filter_type (str): Selected filter type
        """
        parameters = self.get_parameters()
        self._emit_parameters(parameters)
        
    def _on_kernel_size_changed(self, value: int) -> None:
        """
        Handle kernel size slider change.
        
        Args:
            value (int): New kernel size value
        """
        # Ensure odd values only
        if value % 2 == 0:
            value += 1
            self.kernel_slider.setValue(value)
            
        self.kernel_label.setText(f"Kernel Size: {value}")
        parameters = self.get_parameters()
        self._emit_parameters(parameters)
        
    def get_parameters(self) -> Dict[str, Any]:
        """
        Get current parameters from the view.
        
        Returns:
            Dict[str, Any]: Current parameter values
        """
        kernel_size = self.kernel_slider.value()
        # Ensure odd value
        if kernel_size % 2 == 0:
            kernel_size += 1
            
        return {
            "filter_type": self.filter_combo.currentText(),
            "kernel_size": kernel_size
        }
        
    def reset(self) -> None:
        """Reset view to initial state."""
        self.filter_combo.setCurrentIndex(0)  # Reset to "gaussian"
        self.kernel_slider.setValue(3)
        self.kernel_label.setText("Kernel Size: 3")
        
    def set_filter_type(self, filter_type: str) -> None:
        """
        Set the filter type programmatically.
        
        Args:
            filter_type (str): Filter type to set
        """
        index = self.filter_combo.findText(filter_type)
        if index >= 0:
            self.filter_combo.setCurrentIndex(index)
            
    def set_kernel_size(self, kernel_size: int) -> None:
        """
        Set the kernel size programmatically.
        
        Args:
            kernel_size (int): Kernel size to set
        """
        # Ensure odd value and within range
        kernel_size = max(3, min(15, kernel_size))
        if kernel_size % 2 == 0:
            kernel_size += 1
            
        self.kernel_slider.setValue(kernel_size)
        self.kernel_label.setText(f"Kernel Size: {kernel_size}") 