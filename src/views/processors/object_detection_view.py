from typing import Dict, Any
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                            QSlider, QSpinBox, QCheckBox, QDoubleSpinBox)
from PyQt6.QtCore import Qt
from views.processors.base_processor_view import BaseProcessorView

class ObjectDetectionView(BaseProcessorView):
    """
    View for object detection processor controls.
    
    Provides UI controls for adjusting Canny edge detection parameters,
    display options, and filtering settings.
    """
    
    def __init__(self) -> None:
        """Initialize the object detection view."""
        super().__init__("Object Detection")
        self._setup_controls()
        
    def _setup_controls(self) -> None:
        """Set up all control widgets."""
        self._setup_threshold_controls()
        self._setup_gaussian_control()
        self._setup_area_control()
        self._setup_display_options()
        
    def _setup_threshold_controls(self) -> None:
        """Set up Canny threshold controls."""
        # Threshold 1 control
        threshold1_container = QWidget()
        threshold1_layout = QVBoxLayout(threshold1_container)
        
        threshold1_label = QLabel("Canny Threshold 1:")
        threshold1_layout.addWidget(threshold1_label)
        
        threshold1_slider_layout = QHBoxLayout()
        
        self.threshold1_slider = QSlider(Qt.Orientation.Horizontal)
        self.threshold1_slider.setMinimum(1)
        self.threshold1_slider.setMaximum(255)
        self.threshold1_slider.setValue(30)
        self.threshold1_slider.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.threshold1_slider.setTickInterval(50)
        
        self.threshold1_spinbox = QSpinBox()
        self.threshold1_spinbox.setMinimum(1)
        self.threshold1_spinbox.setMaximum(255)
        self.threshold1_spinbox.setValue(30)
        self.threshold1_spinbox.setFixedWidth(60)
        
        threshold1_slider_layout.addWidget(self.threshold1_slider)
        threshold1_slider_layout.addWidget(self.threshold1_spinbox)
        threshold1_layout.addLayout(threshold1_slider_layout)
        
        self.layout.addWidget(threshold1_container)
        
        # Threshold 2 control
        threshold2_container = QWidget()
        threshold2_layout = QVBoxLayout(threshold2_container)
        
        threshold2_label = QLabel("Canny Threshold 2:")
        threshold2_layout.addWidget(threshold2_label)
        
        threshold2_slider_layout = QHBoxLayout()
        
        self.threshold2_slider = QSlider(Qt.Orientation.Horizontal)
        self.threshold2_slider.setMinimum(1)
        self.threshold2_slider.setMaximum(255)
        self.threshold2_slider.setValue(150)
        self.threshold2_slider.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.threshold2_slider.setTickInterval(50)
        
        self.threshold2_spinbox = QSpinBox()
        self.threshold2_spinbox.setMinimum(1)
        self.threshold2_spinbox.setMaximum(255)
        self.threshold2_spinbox.setValue(150)
        self.threshold2_spinbox.setFixedWidth(60)
        
        threshold2_slider_layout.addWidget(self.threshold2_slider)
        threshold2_slider_layout.addWidget(self.threshold2_spinbox)
        threshold2_layout.addLayout(threshold2_slider_layout)
        
        self.layout.addWidget(threshold2_container)
        
        # Connect threshold controls
        self.threshold1_slider.valueChanged.connect(self._on_threshold1_changed)
        self.threshold1_spinbox.valueChanged.connect(self._on_threshold1_changed)
        self.threshold2_slider.valueChanged.connect(self._on_threshold2_changed)
        self.threshold2_spinbox.valueChanged.connect(self._on_threshold2_changed)
        
    def _setup_gaussian_control(self) -> None:
        """Set up Gaussian kernel size control."""
        gaussian_container = QWidget()
        gaussian_layout = QVBoxLayout(gaussian_container)
        
        gaussian_label = QLabel("Gaussian Kernel Size:")
        gaussian_layout.addWidget(gaussian_label)
        
        gaussian_slider_layout = QHBoxLayout()
        
        self.gaussian_slider = QSlider(Qt.Orientation.Horizontal)
        self.gaussian_slider.setMinimum(1)
        self.gaussian_slider.setMaximum(15)
        self.gaussian_slider.setValue(5)
        self.gaussian_slider.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.gaussian_slider.setTickInterval(2)
        
        self.gaussian_spinbox = QSpinBox()
        self.gaussian_spinbox.setMinimum(1)
        self.gaussian_spinbox.setMaximum(15)
        self.gaussian_spinbox.setSingleStep(2)
        self.gaussian_spinbox.setValue(5)
        self.gaussian_spinbox.setFixedWidth(60)
        
        gaussian_slider_layout.addWidget(self.gaussian_slider)
        gaussian_slider_layout.addWidget(self.gaussian_spinbox)
        gaussian_layout.addLayout(gaussian_slider_layout)
        
        self.layout.addWidget(gaussian_container)
        
        # Connect gaussian control
        self.gaussian_slider.valueChanged.connect(self._on_gaussian_changed)
        self.gaussian_spinbox.valueChanged.connect(self._on_gaussian_changed)
        
    def _setup_area_control(self) -> None:
        """Set up minimum contour area control."""
        area_container = QWidget()
        area_layout = QVBoxLayout(area_container)
        
        area_label = QLabel("Minimum Contour Area:")
        area_layout.addWidget(area_label)
        
        area_input_layout = QHBoxLayout()
        
        self.area_spinbox = QDoubleSpinBox()
        self.area_spinbox.setMinimum(0.0)
        self.area_spinbox.setMaximum(10000.0)
        self.area_spinbox.setValue(100.0)
        self.area_spinbox.setSuffix(" px²")
        self.area_spinbox.setDecimals(1)
        
        area_input_layout.addWidget(self.area_spinbox)
        area_input_layout.addStretch()
        area_layout.addLayout(area_input_layout)
        
        self.layout.addWidget(area_container)
        
        # Connect area control
        self.area_spinbox.valueChanged.connect(self._on_parameters_changed)
        
    def _setup_display_options(self) -> None:
        """Set up display option checkboxes."""
        options_container = QWidget()
        options_layout = QVBoxLayout(options_container)
        
        options_label = QLabel("Display Options:")
        options_layout.addWidget(options_label)
        
        # Show numbering checkbox
        self.show_numbering_checkbox = QCheckBox("Show Object Numbering")
        self.show_numbering_checkbox.setChecked(True)
        options_layout.addWidget(self.show_numbering_checkbox)
        
        # Show area checkbox
        self.show_area_checkbox = QCheckBox("Show Object Areas")
        self.show_area_checkbox.setChecked(True)
        options_layout.addWidget(self.show_area_checkbox)
        
        self.layout.addWidget(options_container)
        
        # Connect display option controls
        self.show_numbering_checkbox.stateChanged.connect(self._on_parameters_changed)
        self.show_area_checkbox.stateChanged.connect(self._on_parameters_changed)
        
    def _on_threshold1_changed(self, value: int) -> None:
        """Handle threshold1 value changes."""
        # Ensure odd values for kernel size
        if hasattr(self, 'gaussian_slider') and value % 2 == 0:
            value = value + 1 if value < 255 else value - 1
            
        # Sync slider and spinbox
        if self.sender() == self.threshold1_slider:
            self.threshold1_spinbox.setValue(value)
        else:
            self.threshold1_slider.setValue(value)
            
        self._on_parameters_changed()
        
    def _on_threshold2_changed(self, value: int) -> None:
        """Handle threshold2 value changes."""
        # Sync slider and spinbox
        if self.sender() == self.threshold2_slider:
            self.threshold2_spinbox.setValue(value)
        else:
            self.threshold2_slider.setValue(value)
            
        self._on_parameters_changed()
        
    def _on_gaussian_changed(self, value: int) -> None:
        """Handle Gaussian kernel size changes."""
        # Ensure odd values for kernel size
        if value % 2 == 0:
            value = value + 1 if value < 15 else value - 1
            
        # Sync slider and spinbox
        if self.sender() == self.gaussian_slider:
            self.gaussian_spinbox.setValue(value)
        else:
            self.gaussian_slider.setValue(value)
            
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
        return {
            "threshold1": self.threshold1_spinbox.value(),
            "threshold2": self.threshold2_spinbox.value(),
            "gaussian_kernel": self.gaussian_spinbox.value(),
            "min_contour_area": self.area_spinbox.value(),
            "show_numbering": self.show_numbering_checkbox.isChecked(),
            "show_area": self.show_area_checkbox.isChecked()
        }
        
    def reset(self) -> None:
        """Reset view to initial state."""
        # Reset to default values
        self.threshold1_slider.setValue(30)
        self.threshold1_spinbox.setValue(30)
        self.threshold2_slider.setValue(150)
        self.threshold2_spinbox.setValue(150)
        self.gaussian_slider.setValue(5)
        self.gaussian_spinbox.setValue(5)
        self.area_spinbox.setValue(100.0)
        self.show_numbering_checkbox.setChecked(True)
        self.show_area_checkbox.setChecked(True)
        
        # Emit parameters after reset
        self._on_parameters_changed() 