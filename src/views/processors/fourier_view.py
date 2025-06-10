from typing import Dict, Any
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                            QSlider, QDoubleSpinBox, QComboBox, QCheckBox, QSpinBox, QGroupBox)
from PyQt6.QtCore import Qt
from views.processors.base_processor_view import BaseProcessorView

class FourierView(BaseProcessorView):
    """
    View for Fourier Transform processor controls.
    
    Provides UI controls for frequency domain analysis and filtering including
    operation mode, filter types, cutoff frequencies, and visualization options.
    """
    
    def __init__(self) -> None:
        """Initialize the Fourier transform view."""
        super().__init__("Fourier Transform")
        self._setup_controls()
        
    def _setup_controls(self) -> None:
        """Set up all control widgets."""
        self._setup_operation_control()
        self._setup_filter_controls()
        self._setup_frequency_controls()
        self._setup_filter_shape_controls()
        self._setup_visualization_options()
        
    def _setup_operation_control(self) -> None:
        """Set up operation type selection."""
        operation_group = QGroupBox("Operation Type")
        operation_layout = QVBoxLayout(operation_group)
        
        operations = [
            "Frequency Filter",
            "Magnitude Spectrum", 
            "Phase Spectrum",
            "Inverse FFT"
        ]
        
        self.operation_combo = self._create_combobox("Mode:", operations)
        self.operation_combo.setCurrentText("Frequency Filter")
        self.operation_combo.currentTextChanged.connect(self._on_operation_changed)
        
        operation_layout.addWidget(self.operation_combo)
        self.layout.addWidget(operation_group)
        
    def _setup_filter_controls(self) -> None:
        """Set up filter type and shape controls."""
        self.filter_group = QGroupBox("Filter Settings")
        filter_layout = QVBoxLayout(self.filter_group)
        
        # Filter type selection
        filter_types = [
            "Lowpass",
            "Highpass", 
            "Bandpass",
            "Notch"
        ]
        
        self.filter_type_combo = self._create_combobox("Filter Type:", filter_types)
        self.filter_type_combo.setCurrentText("Lowpass")
        self.filter_type_combo.currentTextChanged.connect(self._on_filter_type_changed)
        filter_layout.addWidget(self.filter_type_combo)
        
        self.layout.addWidget(self.filter_group)
        
    def _setup_frequency_controls(self) -> None:
        """Set up cutoff frequency controls."""
        self.frequency_group = QGroupBox("Frequency Controls")
        frequency_layout = QVBoxLayout(self.frequency_group)
        
        # Primary cutoff frequency
        cutoff_container = QWidget()
        cutoff_layout = QVBoxLayout(cutoff_container)
        
        cutoff_label = QLabel("Cutoff Frequency (% of max):")
        cutoff_layout.addWidget(cutoff_label)
        
        cutoff_slider_layout = QHBoxLayout()
        
        self.cutoff_slider = QSlider(Qt.Orientation.Horizontal)
        self.cutoff_slider.setMinimum(1)
        self.cutoff_slider.setMaximum(100)
        self.cutoff_slider.setValue(50)
        self.cutoff_slider.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.cutoff_slider.setTickInterval(10)
        
        self.cutoff_spinbox = QDoubleSpinBox()
        self.cutoff_spinbox.setMinimum(0.1)
        self.cutoff_spinbox.setMaximum(100.0)
        self.cutoff_spinbox.setValue(50.0)
        self.cutoff_spinbox.setSingleStep(1.0)
        self.cutoff_spinbox.setDecimals(1)
        self.cutoff_spinbox.setSuffix(" %")
        self.cutoff_spinbox.setFixedWidth(100)
        
        cutoff_slider_layout.addWidget(self.cutoff_slider)
        cutoff_slider_layout.addWidget(self.cutoff_spinbox)
        cutoff_layout.addLayout(cutoff_slider_layout)
        
        frequency_layout.addWidget(cutoff_container)
        
        # High cutoff frequency (for bandpass/notch)
        self.cutoff_high_container = QWidget()
        cutoff_high_layout = QVBoxLayout(self.cutoff_high_container)
        
        cutoff_high_label = QLabel("High Cutoff Frequency (% of max):")
        cutoff_high_layout.addWidget(cutoff_high_label)
        
        cutoff_high_slider_layout = QHBoxLayout()
        
        self.cutoff_high_slider = QSlider(Qt.Orientation.Horizontal)
        self.cutoff_high_slider.setMinimum(1)
        self.cutoff_high_slider.setMaximum(100)
        self.cutoff_high_slider.setValue(80)
        self.cutoff_high_slider.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.cutoff_high_slider.setTickInterval(10)
        
        self.cutoff_high_spinbox = QDoubleSpinBox()
        self.cutoff_high_spinbox.setMinimum(0.1)
        self.cutoff_high_spinbox.setMaximum(100.0)
        self.cutoff_high_spinbox.setValue(80.0)
        self.cutoff_high_spinbox.setSingleStep(1.0)
        self.cutoff_high_spinbox.setDecimals(1)
        self.cutoff_high_spinbox.setSuffix(" %")
        self.cutoff_high_spinbox.setFixedWidth(100)
        
        cutoff_high_slider_layout.addWidget(self.cutoff_high_slider)
        cutoff_high_slider_layout.addWidget(self.cutoff_high_spinbox)
        cutoff_high_layout.addLayout(cutoff_high_slider_layout)
        
        frequency_layout.addWidget(self.cutoff_high_container)
        
        # Connect frequency controls
        self.cutoff_slider.valueChanged.connect(self._on_cutoff_slider_changed)
        self.cutoff_spinbox.valueChanged.connect(self._on_cutoff_spinbox_changed)
        self.cutoff_high_slider.valueChanged.connect(self._on_cutoff_high_slider_changed)
        self.cutoff_high_spinbox.valueChanged.connect(self._on_cutoff_high_spinbox_changed)
        
        # Initially hide high cutoff (only for bandpass/notch)
        self.cutoff_high_container.setVisible(False)
        
        self.layout.addWidget(self.frequency_group)
        
    def _setup_filter_shape_controls(self) -> None:
        """Set up filter shape and parameters."""
        self.shape_group = QGroupBox("Filter Shape")
        shape_layout = QVBoxLayout(self.shape_group)
        
        # Filter shape selection
        filter_shapes = [
            "Gaussian",
            "Ideal",
            "Butterworth"
        ]
        
        self.filter_shape_combo = self._create_combobox("Shape:", filter_shapes)
        self.filter_shape_combo.setCurrentText("Gaussian")
        self.filter_shape_combo.currentTextChanged.connect(self._on_filter_shape_changed)
        shape_layout.addWidget(self.filter_shape_combo)
        
        # Butterworth order control
        self.butterworth_container = QWidget()
        butterworth_layout = QVBoxLayout(self.butterworth_container)
        
        butterworth_label = QLabel("Butterworth Order:")
        butterworth_layout.addWidget(butterworth_label)
        
        self.butterworth_spinbox = QSpinBox()
        self.butterworth_spinbox.setMinimum(1)
        self.butterworth_spinbox.setMaximum(10)
        self.butterworth_spinbox.setValue(2)
        self.butterworth_spinbox.setSuffix(" (steepness)")
        
        butterworth_layout.addWidget(self.butterworth_spinbox)
        shape_layout.addWidget(self.butterworth_container)
        
        # Gaussian sigma control
        self.gaussian_container = QWidget()
        gaussian_layout = QVBoxLayout(self.gaussian_container)
        
        gaussian_label = QLabel("Gaussian Sigma:")
        gaussian_layout.addWidget(gaussian_label)
        
        gaussian_slider_layout = QHBoxLayout()
        
        self.gaussian_slider = QSlider(Qt.Orientation.Horizontal)
        self.gaussian_slider.setMinimum(10)  # 1.0
        self.gaussian_slider.setMaximum(1000)  # 100.0
        self.gaussian_slider.setValue(200)  # Default 20.0
        self.gaussian_slider.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.gaussian_slider.setTickInterval(100)
        
        self.gaussian_spinbox = QDoubleSpinBox()
        self.gaussian_spinbox.setMinimum(1.0)
        self.gaussian_spinbox.setMaximum(100.0)
        self.gaussian_spinbox.setValue(20.0)
        self.gaussian_spinbox.setSingleStep(1.0)
        self.gaussian_spinbox.setDecimals(1)
        self.gaussian_spinbox.setFixedWidth(80)
        
        gaussian_slider_layout.addWidget(self.gaussian_slider)
        gaussian_slider_layout.addWidget(self.gaussian_spinbox)
        gaussian_layout.addLayout(gaussian_slider_layout)
        
        shape_layout.addWidget(self.gaussian_container)
        
        # Connect shape controls
        self.butterworth_spinbox.valueChanged.connect(self._on_parameters_changed)
        self.gaussian_slider.valueChanged.connect(self._on_gaussian_slider_changed)
        self.gaussian_spinbox.valueChanged.connect(self._on_gaussian_spinbox_changed)
        
        # Initially show only Gaussian controls
        self.butterworth_container.setVisible(False)
        
        self.layout.addWidget(self.shape_group)
        
    def _setup_visualization_options(self) -> None:
        """Set up visualization and display options."""
        viz_group = QGroupBox("Visualization Options")
        viz_layout = QVBoxLayout(viz_group)
        
        # Show spectrum overlay
        self.show_spectrum_checkbox = QCheckBox("Show Frequency Spectrum Overlay")
        self.show_spectrum_checkbox.setChecked(True)
        viz_layout.addWidget(self.show_spectrum_checkbox)
        
        # Log transform for spectrum display
        self.log_transform_checkbox = QCheckBox("Use Log Transform for Spectrum")
        self.log_transform_checkbox.setChecked(True)
        viz_layout.addWidget(self.log_transform_checkbox)
        
        # Connect visualization controls
        self.show_spectrum_checkbox.stateChanged.connect(self._on_parameters_changed)
        self.log_transform_checkbox.stateChanged.connect(self._on_parameters_changed)
        
        self.layout.addWidget(viz_group)
        
    def _on_operation_changed(self, operation: str) -> None:
        """Handle operation type selection changes."""
        # Show/hide filter controls based on operation type
        is_filter_mode = (operation == "Frequency Filter")
        
        self.filter_group.setVisible(is_filter_mode)
        self.frequency_group.setVisible(is_filter_mode)
        self.shape_group.setVisible(is_filter_mode)
        
        self._on_parameters_changed()
        
    def _on_filter_type_changed(self, filter_type: str) -> None:
        """Handle filter type selection changes."""
        # Show/hide high cutoff for bandpass/notch filters
        needs_high_cutoff = filter_type in ["Bandpass", "Notch"]
        self.cutoff_high_container.setVisible(needs_high_cutoff)
        
        self._on_parameters_changed()
        
    def _on_filter_shape_changed(self, shape: str) -> None:
        """Handle filter shape selection changes."""
        # Show/hide shape-specific controls
        self.butterworth_container.setVisible(shape == "Butterworth")
        self.gaussian_container.setVisible(shape == "Gaussian")
        
        self._on_parameters_changed()
        
    def _on_cutoff_slider_changed(self, value: int) -> None:
        """Handle cutoff frequency slider changes."""
        cutoff_value = float(value)
        self.cutoff_spinbox.setValue(cutoff_value)
        self._on_parameters_changed()
        
    def _on_cutoff_spinbox_changed(self, value: float) -> None:
        """Handle cutoff frequency spinbox changes."""
        slider_value = int(value)
        self.cutoff_slider.setValue(slider_value)
        self._on_parameters_changed()
        
    def _on_cutoff_high_slider_changed(self, value: int) -> None:
        """Handle high cutoff frequency slider changes."""
        cutoff_high_value = float(value)
        self.cutoff_high_spinbox.setValue(cutoff_high_value)
        self._on_parameters_changed()
        
    def _on_cutoff_high_spinbox_changed(self, value: float) -> None:
        """Handle high cutoff frequency spinbox changes."""
        slider_value = int(value)
        self.cutoff_high_slider.setValue(slider_value)
        self._on_parameters_changed()
        
    def _on_gaussian_slider_changed(self, value: int) -> None:
        """Handle Gaussian sigma slider changes."""
        gaussian_value = value / 10.0  # Convert to 1.0-100.0 range
        self.gaussian_spinbox.setValue(gaussian_value)
        self._on_parameters_changed()
        
    def _on_gaussian_spinbox_changed(self, value: float) -> None:
        """Handle Gaussian sigma spinbox changes."""
        slider_value = int(value * 10)  # Convert to 10-1000 range
        self.gaussian_slider.setValue(slider_value)
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
        operation_map = {
            "Frequency Filter": "filter",
            "Magnitude Spectrum": "magnitude", 
            "Phase Spectrum": "phase",
            "Inverse FFT": "inverse"
        }
        
        filter_type_map = {
            "Lowpass": "lowpass",
            "Highpass": "highpass",
            "Bandpass": "bandpass", 
            "Notch": "notch"
        }
        
        filter_shape_map = {
            "Gaussian": "gaussian",
            "Ideal": "ideal",
            "Butterworth": "butterworth"
        }
        
        return {
            "operation_type": operation_map[self.operation_combo.currentText()],
            "filter_type": filter_type_map[self.filter_type_combo.currentText()],
            "filter_shape": filter_shape_map[self.filter_shape_combo.currentText()],
            "cutoff_frequency": self.cutoff_spinbox.value(),
            "cutoff_high": self.cutoff_high_spinbox.value(),
            "butterworth_order": self.butterworth_spinbox.value(),
            "gaussian_sigma": self.gaussian_spinbox.value(),
            "show_spectrum": self.show_spectrum_checkbox.isChecked(),
            "log_transform": self.log_transform_checkbox.isChecked()
        }
        
    def reset(self) -> None:
        """Reset view to initial state."""
        # Reset to default values
        self.operation_combo.setCurrentText("Frequency Filter")
        self.filter_type_combo.setCurrentText("Lowpass")
        self.filter_shape_combo.setCurrentText("Gaussian")
        
        self.cutoff_slider.setValue(50)
        self.cutoff_spinbox.setValue(50.0)
        self.cutoff_high_slider.setValue(80)
        self.cutoff_high_spinbox.setValue(80.0)
        
        self.butterworth_spinbox.setValue(2)
        self.gaussian_slider.setValue(200)
        self.gaussian_spinbox.setValue(20.0)
        
        self.show_spectrum_checkbox.setChecked(True)
        self.log_transform_checkbox.setChecked(True)
        
        # Update visibility
        self._on_operation_changed("Frequency Filter")
        self._on_filter_type_changed("Lowpass")
        self._on_filter_shape_changed("Gaussian")
        
        # Emit parameters after reset
        self._on_parameters_changed() 