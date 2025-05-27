# type: ignore
from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                           QLabel, QPushButton, QFileDialog, QComboBox,
                           QFrame, QSizePolicy, QStackedWidget)
from PyQt6.QtGui import QPixmap, QImage
from PyQt6.QtCore import Qt, QSize
from typing import Dict, Any
import cv2
import numpy as np
from utils.imageScaling_ultil import image_scaling
from views.components.error_message import ErrorMessage
from views.components.success_message import SuccessMessage

class MainWindow(QMainWindow):
    """
    Main application window for the Image Processor.
    
    Provides the main user interface for loading images, selecting processors,
    and displaying results.
    """
    
    def __init__(self, processor_controllers: Dict[str, Any]) -> None:
        """
        Initialize the main window.
        
        Args:
            processor_controllers: Dictionary of processor controllers
        """
        super().__init__()
        self.processor_controllers = processor_controllers
        self.original_image: np.ndarray = None
        self.processed_image: np.ndarray = None
        self.current_processor = None
        self.processor_views: Dict[str, QWidget] = {}
        self._setup_ui()

    def _setup_ui(self) -> None:
        """Set up the user interface."""
        self.setWindowTitle("Image Processor")
        self.setGeometry(100, 100, 1800, 700)
        self.setMinimumSize(1200, 600)
        
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QHBoxLayout(main_widget)
        main_layout.setSpacing(20)
        
        # Create image display frames
        self.original_frame, self.original_image_label = self._create_image_frame("Original Image")
        self.processed_frame, self.processed_image_label = self._create_image_frame("Processed Image")
        
        # Create control panel
        control_panel = self._create_control_panel()
        
        main_layout.addWidget(self.original_frame, 1)
        main_layout.addWidget(control_panel)
        main_layout.addWidget(self.processed_frame, 1)

    def _create_image_frame(self, title: str) -> tuple:
        """
        Create an image display frame.
        
        Args:
            title: Title for the frame
            
        Returns:
            tuple: (frame, image_label) widgets
        """
        frame = QFrame()
        frame.setFrameStyle(QFrame.Shape.StyledPanel)
        frame.setMinimumSize(400, 400)
        frame.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        layout = QVBoxLayout(frame)
        layout.setContentsMargins(10, 10, 10, 10)
        
        title_label = QLabel(title)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("font-weight: bold; font-size: 14px;")
        layout.addWidget(title_label)

        # Create container for image
        image_container = QWidget()
        image_container.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        image_layout = QVBoxLayout(image_container)
        image_layout.setContentsMargins(0, 0, 0, 0)
        
        image_label = QLabel()
        image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        image_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        image_layout.addWidget(image_label)
        
        layout.addWidget(image_container)

        return frame, image_label

    def _create_control_panel(self) -> QWidget:
        """
        Create the control panel widget.
        
        Returns:
            QWidget: Control panel widget
        """
        panel = QWidget()
        panel.setFixedWidth(400)
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(10, 10, 10, 10)
        
        self.upload_button = QPushButton("Upload Image")
        self.upload_button.clicked.connect(self._on_upload_clicked)
        layout.addWidget(self.upload_button)
        
        self.processor_combo = QComboBox()
        self.processor_combo.addItems(["Select Transformation"] + list(self.processor_controllers.keys()))
        self.processor_combo.currentTextChanged.connect(self._on_processor_changed)
        layout.addWidget(self.processor_combo)
        
        self.views_stack = QStackedWidget()
        layout.addWidget(self.views_stack)
        
        self._create_processor_views()
        
        self.process_button = QPushButton("Process Image")
        self.process_button.clicked.connect(self._on_process_clicked)
        layout.addWidget(self.process_button)
        
        self.save_button = QPushButton("Save Processed Image")
        self.save_button.clicked.connect(self._on_save_clicked)
        self.save_button.setEnabled(False)
        layout.addWidget(self.save_button)
        
        layout.addStretch()
        return panel

    def _create_processor_views(self) -> None:
        """Create all processor views at startup."""
        empty_widget = QWidget()
        self.views_stack.addWidget(empty_widget)
        
        for name, controller in self.processor_controllers.items():
            view = controller.get_view()  # Updated method name
            self.processor_views[name] = view
            self.views_stack.addWidget(view)

    def _on_upload_clicked(self) -> None:
        """Handle upload button click."""
        file_name, _ = QFileDialog.getOpenFileName(
            self, "Open Image File", "",
            "Image Files (*.png *.jpg *.jpeg *.bmp *.gif)")
            
        if file_name:
            self.original_image = cv2.imread(file_name)
            if self.original_image is None:
                return
                
            self.image_height, self.image_width = self.original_image.shape[:2]
            
            # Calculate frame size for scaling
            frame_width = self.original_frame.width() - 20
            frame_height = self.original_frame.height() - 60
            
            # Scale image to fit frame while maintaining aspect ratio
            display_img = image_scaling(self.original_image, max_width=frame_width, max_height=frame_height)
            self._display_image(display_img, self.original_image_label)
            
            if self.current_processor is not None:
                current_view = self.processor_views.get(self.processor_combo.currentText())
                if current_view and hasattr(current_view, 'set_image_dimensions'):
                    current_view.set_image_dimensions(self.image_width, self.image_height)
            
            self.save_button.setEnabled(False)

    def _on_processor_changed(self, name: str) -> None:
        """Handle processor selection change."""
        if name == "Select Transformation":
            self.views_stack.setCurrentIndex(0)
            self.current_processor = None
            return
            
        try:
            view_index = list(self.processor_controllers.keys()).index(name) + 1
            self.views_stack.setCurrentIndex(view_index)
            self.current_processor = self.processor_controllers[name].get_model()  # Updated method name
            
            if hasattr(self, 'image_width') and hasattr(self, 'image_height'):
                current_view = self.processor_views.get(name)
                if current_view and hasattr(current_view, 'set_image_dimensions'):
                    current_view.set_image_dimensions(self.image_width, self.image_height)
        except (KeyError, ValueError):
            pass

    def _on_process_clicked(self) -> None:
        """Handle process button click."""
        if self.original_image is None or self.current_processor is None:
            return
            
        self.processed_image = self.current_processor.process(self.original_image)
        
        # Calculate frame size for scaling
        frame_width = self.processed_frame.width() - 20
        frame_height = self.processed_frame.height() - 60
        
        # Scale processed image to match original image size
        display_img = image_scaling(self.processed_image, max_width=frame_width, max_height=frame_height)
        self._display_image(display_img, self.processed_image_label)
        self.save_button.setEnabled(True)

    def _on_save_clicked(self) -> None:
        """Handle save button click."""
        if self.processed_image is None:
            return
        
        file_name, _ = QFileDialog.getSaveFileName(
            self, "Save Processed Image", "",
            "PNG Image (*.png);;JPEG Image (*.jpg);;BMP Image (*.bmp)")
        
        if file_name:
            cv2.imwrite(file_name, self.processed_image)

    def _display_image(self, image: np.ndarray, image_label: QLabel) -> None:
        """
        Display an image in the specified label.
        
        Args:
            image: Image to display
            image_label: Label widget to display image in
        """
        if image is None:
            return
            
        height, width = image.shape[:2]
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        qt_image = QImage(rgb_image.tobytes(), width, height, 3 * width, QImage.Format.Format_RGB888)
        pixmap = QPixmap.fromImage(qt_image)
        
        # Scale pixmap to fit label while maintaining aspect ratio
        scaled_pixmap = pixmap.scaled(
            image_label.size(),
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        )
        
        image_label.setPixmap(scaled_pixmap)

    def resizeEvent(self, event) -> None:
        """Handle window resize event."""
        super().resizeEvent(event)
        
        # Update image displays if images exist
        if self.original_image is not None:
            frame_width = self.original_frame.width() - 20
            frame_height = self.original_frame.height() - 60
            display_img = image_scaling(self.original_image, max_width=frame_width, max_height=frame_height)
            self._display_image(display_img, self.original_image_label)
            
        if self.processed_image is not None:
            frame_width = self.processed_frame.width() - 20
            frame_height = self.processed_frame.height() - 60
            display_img = image_scaling(self.processed_image, max_width=frame_width, max_height=frame_height)
            self._display_image(display_img, self.processed_image_label)

    def closeEvent(self, event) -> None:
        """Handle application close event."""
        # Clean up controllers
        for controller in self.processor_controllers.values():
            if hasattr(controller, 'cleanup'):
                controller.cleanup()
        super().closeEvent(event)
