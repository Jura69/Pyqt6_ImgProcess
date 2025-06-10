from typing import Dict, Any
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                            QSlider, QDoubleSpinBox, QComboBox, QCheckBox, QSpinBox)
from PyQt6.QtCore import Qt
from views.processors.base_processor_view import BaseProcessorView

class HighpassView(BaseProcessorView):
    """
    View for highpass filter processor controls.
    
    Provides UI controls for adjusting highpass filter parameters including
    filter type, strength, and algorithm-specific settings.
    """
    
    def __init__(self) -> None:
        """Initialize the highpass filter view."""
        super().__init__("Highpass Filter")
        self._setup_controls()
        
    def _setup_controls(self) -> None:
        """Set up all control widgets."""
        self._setup_filter_type_control()
        self._setup_strength_control()
        self._setup_gaussian_control()
        self._setup_boost_factor_control()
        self._setup_kernel_size_control()
        self._setup_options()
        
    def _setup_filter_type_control(self) -> None:
        """Set up filter type selection."""
        filter_types = [
            "Unsharp Mask",
            "Laplacian", 
            "High Boost",
            "Custom Kernel"
        ]
        
        self.filter_type_combo = self._create_combobox("Filter Type:", filter_types)
        self.filter_type_combo.setCurrentText("Unsharp Mask")
        self.filter_type_combo.currentTextChanged.connect(self._on_filter_type_changed)
        
    def _setup_strength_control(self) -> None:
        """Set up filter strength control."""
        strength_container = QWidget()
        strength_layout = QVBoxLayout(strength_container)
        
        strength_label = QLabel("Filter Strength:")
        strength_layout.addWidget(strength_label)
        
        strength_slider_layout = QHBoxLayout()
        
        self.strength_slider = QSlider(Qt.Orientation.Horizontal)
        self.strength_slider.setMinimum(0)
        self.strength_slider.setMaximum(500)  # 0.0 to 5.0 with 0.01 precision
        self.strength_slider.setValue(100)  # Default 1.0
        self.strength_slider.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.strength_slider.setTickInterval(100)
        
        self.strength_spinbox = QDoubleSpinBox()
        self.strength_spinbox.setMinimum(0.0)
        self.strength_spinbox.setMaximum(5.0)
        self.strength_spinbox.setValue(1.0)
        self.strength_spinbox.setSingleStep(0.1)
        self.strength_spinbox.setDecimals(2)
        self.strength_spinbox.setFixedWidth(80)
        
        strength_slider_layout.addWidget(self.strength_slider)
        strength_slider_layout.addWidget(self.strength_spinbox)
        strength_layout.addLayout(strength_slider_layout)
        
        self.layout.addWidget(strength_container)
        
        # Connect strength controls
        self.strength_slider.valueChanged.connect(self._on_strength_slider_changed)
        self.strength_spinbox.valueChanged.connect(self._on_strength_spinbox_changed)
        
    def _setup_gaussian_control(self) -> None:
        """Set up Gaussian sigma control for unsharp mask and high boost."""
        self.gaussian_container = QWidget()
        gaussian_layout = QVBoxLayout(self.gaussian_container)
        
        gaussian_label = QLabel("Gaussian Sigma (Blur Amount):")
        gaussian_layout.addWidget(gaussian_label)
        
        gaussian_slider_layout = QHBoxLayout()
        
        self.gaussian_slider = QSlider(Qt.Orientation.Horizontal)
        self.gaussian_slider.setMinimum(10)  # 0.1
        self.gaussian_slider.setMaximum(1000)  # 10.0
        self.gaussian_slider.setValue(100)  # Default 1.0
        self.gaussian_slider.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.gaussian_slider.setTickInterval(100)
        
        self.gaussian_spinbox = QDoubleSpinBox()
        self.gaussian_spinbox.setMinimum(0.1)
        self.gaussian_spinbox.setMaximum(10.0)
        self.gaussian_spinbox.setValue(1.0)
        self.gaussian_spinbox.setSingleStep(0.1)
        self.gaussian_spinbox.setDecimals(2)
        self.gaussian_spinbox.setFixedWidth(80)
        
        gaussian_slider_layout.addWidget(self.gaussian_slider)
        gaussian_slider_layout.addWidget(self.gaussian_spinbox)
        gaussian_layout.addLayout(gaussian_slider_layout)
        
        self.layout.addWidget(self.gaussian_container)
        
        # Connect gaussian controls
        self.gaussian_slider.valueChanged.connect(self._on_gaussian_slider_changed)
        self.gaussian_spinbox.valueChanged.connect(self._on_gaussian_spinbox_changed)
        
    def _setup_boost_factor_control(self) -> None:
        """Set up boost factor control for high boost filter."""
        self.boost_container = QWidget()
        boost_layout = QVBoxLayout(self.boost_container)
        
        boost_label = QLabel("Boost Factor:")
        boost_layout.addWidget(boost_label)
        
        boost_slider_layout = QHBoxLayout()
        
        self.boost_slider = QSlider(Qt.Orientation.Horizontal)
        self.boost_slider.setMinimum(100)  # 1.0
        self.boost_slider.setMaximum(500)  # 5.0
        self.boost_slider.setValue(150)  # Default 1.5
        self.boost_slider.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.boost_slider.setTickInterval(100)
        
        self.boost_spinbox = QDoubleSpinBox()
        self.boost_spinbox.setMinimum(1.0)
        self.boost_spinbox.setMaximum(5.0)
        self.boost_spinbox.setValue(1.5)
        self.boost_spinbox.setSingleStep(0.1)
        self.boost_spinbox.setDecimals(2)
        self.boost_spinbox.setFixedWidth(80)
        
        boost_slider_layout.addWidget(self.boost_slider)
        boost_slider_layout.addWidget(self.boost_spinbox)
        boost_layout.addLayout(boost_slider_layout)
        
        self.layout.addWidget(self.boost_container)
        
        # Connect boost controls
        self.boost_slider.valueChanged.connect(self._on_boost_slider_changed)
        self.boost_spinbox.valueChanged.connect(self._on_boost_spinbox_changed)
        
        # Initially hide boost factor (only shown for high boost filter)
        self.boost_container.setVisible(False)
        
    def _setup_kernel_size_control(self) -> None:
        """Set up kernel size control for custom kernels."""
        self.kernel_container = QWidget()
        kernel_layout = QVBoxLayout(self.kernel_container)
        
        kernel_label = QLabel("Kernel Size:")
        kernel_layout.addWidget(kernel_label)
        
        self.kernel_spinbox = QSpinBox()
        self.kernel_spinbox.setMinimum(3)
        self.kernel_spinbox.setMaximum(5)
        self.kernel_spinbox.setSingleStep(2)
        self.kernel_spinbox.setValue(3)
        self.kernel_spinbox.setSuffix(" x 3" if self.kernel_spinbox.value() == 3 else " x 5")
        
        kernel_layout.addWidget(self.kernel_spinbox)
        self.layout.addWidget(self.kernel_container)
        
        # Connect kernel control
        self.kernel_spinbox.valueChanged.connect(self._on_kernel_size_changed)
        
        # Initially hide kernel size (only shown for custom filter)
        self.kernel_container.setVisible(False)
        
    def _setup_options(self) -> None:
        """Set up additional options."""
        options_container = QWidget()
        options_layout = QVBoxLayout(options_container)
        
        options_label = QLabel("Options:")
        options_layout.addWidget(options_label)
        
        # Preserve brightness checkbox
        self.preserve_brightness_checkbox = QCheckBox("Preserve Original Brightness")
        self.preserve_brightness_checkbox.setChecked(True)
        options_layout.addWidget(self.preserve_brightness_checkbox)
        
        self.layout.addWidget(options_container)
        
        # Connect options
        self.preserve_brightness_checkbox.stateChanged.connect(self._on_parameters_changed)
        
    def _on_filter_type_changed(self, filter_type: str) -> None:
        """Handle filter type selection changes."""
        # Show/hide relevant controls based on filter type
        if filter_type in ["Unsharp Mask", "High Boost"]:
            self.gaussian_container.setVisible(True)
        else:
            self.gaussian_container.setVisible(False)
            
        if filter_type == "High Boost":
            self.boost_container.setVisible(True)
        else:
            self.boost_container.setVisible(False)
            
        if filter_type == "Custom Kernel":
            self.kernel_container.setVisible(True)
        else:
            self.kernel_container.setVisible(False)
            
        self._on_parameters_changed()
        
    def _on_strength_slider_changed(self, value: int) -> None:
        """Handle strength slider changes."""
        strength_value = value / 100.0  # Convert to 0.0-5.0 range
        self.strength_spinbox.setValue(strength_value)
        self._on_parameters_changed()
        
    def _on_strength_spinbox_changed(self, value: float) -> None:
        """Handle strength spinbox changes."""
        slider_value = int(value * 100)  # Convert to 0-500 range
        self.strength_slider.setValue(slider_value)
        self._on_parameters_changed()
        
    def _on_gaussian_slider_changed(self, value: int) -> None:
        """Handle gaussian slider changes."""
        gaussian_value = value / 100.0  # Convert to 0.1-10.0 range
        self.gaussian_spinbox.setValue(gaussian_value)
        self._on_parameters_changed()
        
    def _on_gaussian_spinbox_changed(self, value: float) -> None:
        """Handle gaussian spinbox changes."""
        slider_value = int(value * 100)  # Convert to 10-1000 range
        self.gaussian_slider.setValue(slider_value)
        self._on_parameters_changed()
        
    def _on_boost_slider_changed(self, value: int) -> None:
        """Handle boost factor slider changes."""
        boost_value = value / 100.0  # Convert to 1.0-5.0 range
        self.boost_spinbox.setValue(boost_value)
        self._on_parameters_changed()
        
    def _on_boost_spinbox_changed(self, value: float) -> None:
        """Handle boost factor spinbox changes."""
        slider_value = int(value * 100)  # Convert to 100-500 range
        self.boost_slider.setValue(slider_value)
        self._on_parameters_changed()
        
    def _on_kernel_size_changed(self, value: int) -> None:
        """Handle kernel size changes."""
        # Update suffix to show actual kernel dimensions
        self.kernel_spinbox.setSuffix(f" x {value}")
        self._on_parameters_changed()
        
    def _on_parameters_changed(self) -> None:
        """Handle any parameter change."""
        parameters = self.get_parameters()
        self._emit_parameters(parameters)
        
    def get_parameters(self) -> Dict[str, Any]:
        """
        Get current parameters from the view.
        
        Returns:
            Dict[str, Any]: Current parameter values
        """
        # Map display names to internal names
        filter_type_map = {
            "Unsharp Mask": "unsharp_mask",
            "Laplacian": "laplacian",
            "High Boost": "high_boost",
            "Custom Kernel": "custom"
        }
        
        return {
            "filter_type": filter_type_map[self.filter_type_combo.currentText()],
            "strength": self.strength_spinbox.value(),
            "gaussian_sigma": self.gaussian_spinbox.value(),
            "boost_factor": self.boost_spinbox.value(),
            "kernel_size": self.kernel_spinbox.value(),
            "preserve_brightness": self.preserve_brightness_checkbox.isChecked()
        }
        
    def reset(self) -> None:
        """Reset view to initial state."""
        # Reset to default values
        self.filter_type_combo.setCurrentText("Unsharp Mask")
        self.strength_slider.setValue(100)
        self.strength_spinbox.setValue(1.0)
        self.gaussian_slider.setValue(100)
        self.gaussian_spinbox.setValue(1.0)
        self.boost_slider.setValue(150)
        self.boost_spinbox.setValue(1.5)
        self.kernel_spinbox.setValue(3)
        self.preserve_brightness_checkbox.setChecked(True)
        
        # Update visibility
        self._on_filter_type_changed("Unsharp Mask")
        
        # Emit parameters after reset
        self._on_parameters_changed() 