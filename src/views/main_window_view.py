"""
Main Window View - UI components for the main application window.

This view handles only the UI presentation layer without business logic,
following the MVC pattern for clear separation of concerns.
"""

from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                           QLabel, QPushButton, QFileDialog, QComboBox,
                           QFrame, QSizePolicy, QStackedWidget)
from PyQt6.QtGui import QPixmap, QImage
from PyQt6.QtCore import Qt, pyqtSignal
from typing import Dict, Any, Optional
import cv2
import numpy as np
from utils.imageScaling_ultil import image_scaling
from views.components.error_message import ErrorMessage
from views.components.success_message import SuccessMessage
from views.components.warning_message import WarningMessage

class MainWindowView(QMainWindow):
    """
    View component for main window UI.
    
    Handles only UI presentation and user interactions,
    emits signals for controller to handle business logic.
    """
    
    # Constants following CODE_STANDARDS.md
    DEFAULT_WINDOW_WIDTH = 1800
    DEFAULT_WINDOW_HEIGHT = 700
    MIN_WINDOW_WIDTH = 1200
    MIN_WINDOW_HEIGHT = 600
    CONTROL_PANEL_WIDTH = 400
    MESSAGE_CONTAINER_HEIGHT = 40
    IMAGE_FRAME_MIN_SIZE = 400
    
    # Add constant for default processor name
    DEFAULT_PROCESSOR_NAME = "Select Transformation"
    
    # Signals for user interactions
    upload_requested = pyqtSignal(str)  # Emitted when user selects file to upload
    processor_selection_changed = pyqtSignal(str)  # Emitted when processor is selected
    process_requested = pyqtSignal()  # Emitted when process button is clicked
    save_requested = pyqtSignal(str)  # Emitted when user chooses save location
    
    def __init__(self) -> None:
        """Initialize the main window view."""
        super().__init__()
        self._processor_views: Dict[str, QWidget] = {}
        self._setup_message_components()  # Create messages first
        self._setup_ui()
    
    def _setup_ui(self) -> None:
        """Set up the user interface."""
        self.setWindowTitle("Image Processor")
        self.setGeometry(100, 100, self.DEFAULT_WINDOW_WIDTH, self.DEFAULT_WINDOW_HEIGHT)
        self.setMinimumSize(self.MIN_WINDOW_WIDTH, self.MIN_WINDOW_HEIGHT)
        
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
    
    def _setup_message_components(self) -> None:
        """Setup message components for notifications."""
        self.success_message = SuccessMessage()
        self.error_message = ErrorMessage()
        self.warning_message = WarningMessage()
        
        # Create a fixed-height container for messages to prevent UI jumping
        self.message_container = QWidget()
        self.message_container.setFixedHeight(self.MESSAGE_CONTAINER_HEIGHT)  # Fixed height for up to 3 messages
        self.message_layout = QVBoxLayout(self.message_container)
        self.message_layout.setContentsMargins(0, 0, 0, 0)
        self.message_layout.setSpacing(5)
        
        # Add all message components to the container
        self.message_layout.addWidget(self.warning_message)
        self.message_layout.addWidget(self.success_message)
        self.message_layout.addWidget(self.error_message)
        
        # Add stretch to push messages to top of container
        self.message_layout.addStretch()
    
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
        frame.setMinimumSize(self.IMAGE_FRAME_MIN_SIZE, self.IMAGE_FRAME_MIN_SIZE)
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
        panel.setFixedWidth(self.CONTROL_PANEL_WIDTH)
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(10, 10, 10, 10)
        
        # Add fixed message container at the top
        layout.addWidget(self.message_container)
        
        # Upload button
        self.upload_button = QPushButton("Upload Image")
        self.upload_button.clicked.connect(self._on_upload_clicked)
        layout.addWidget(self.upload_button)
        
        # Processor selection
        self.processor_combo = QComboBox()
        self.processor_combo.currentTextChanged.connect(self._on_processor_changed)
        layout.addWidget(self.processor_combo)
        
        # Views stack for processor options
        self.views_stack = QStackedWidget()
        layout.addWidget(self.views_stack)
        
        # Process button
        self.process_button = QPushButton("Process Image")
        self.process_button.clicked.connect(self._on_process_clicked)
        layout.addWidget(self.process_button)
        
        # Save button
        self.save_button = QPushButton("Save Processed Image")
        self.save_button.clicked.connect(self._on_save_clicked)
        self.save_button.setEnabled(False)
        layout.addWidget(self.save_button)
        
        layout.addStretch()
        return panel
    
    def setup_processor_views(self, processor_views: Dict[str, QWidget]) -> None:
        """
        Setup processor views in the stack widget.
        
        Args:
            processor_views: Dictionary mapping processor names to view widgets
        """
        self._processor_views = processor_views
        
        # Clear existing views
        while self.views_stack.count() > 0:
            widget = self.views_stack.widget(0)
            self.views_stack.removeWidget(widget)
        
        # Add empty widget for default state
        empty_widget = QWidget()
        self.views_stack.addWidget(empty_widget)
        
        # Add processor views
        for name, view in processor_views.items():
            self.views_stack.addWidget(view)
    
    def set_processor_names(self, processor_names: list) -> None:
        """
        Set available processor names in combo box.
        
        Args:
            processor_names: List of processor names
        """
        self.processor_combo.clear()
        self.processor_combo.addItems(processor_names)
    
    def display_original_image(self, image: np.ndarray) -> None:
        """
        Display original image in the original image frame.
        
        Args:
            image: Image to display
        """
        # Validate input according to standards
        if image is None or not isinstance(image, np.ndarray):
            return
        
        frame_width = self.original_frame.width() - 20
        frame_height = self.original_frame.height() - 60
        
        display_img = image_scaling(image, max_width=frame_width, max_height=frame_height)
        self._display_image(display_img, self.original_image_label)
    
    def display_processed_image(self, image: np.ndarray) -> None:
        """
        Display processed image in the processed image frame.
        
        Args:
            image: Image to display
        """
        # Validate input according to standards
        if image is None or not isinstance(image, np.ndarray):
            return
        
        frame_width = self.processed_frame.width() - 20
        frame_height = self.processed_frame.height() - 60
        
        display_img = image_scaling(image, max_width=frame_width, max_height=frame_height)
        self._display_image(display_img, self.processed_image_label)
    
    def set_processor_selection(self, processor_name: str) -> None:
        """
        Set current processor selection in UI.
        
        Args:
            processor_name: Name of processor to select
        """
        if processor_name == "" or processor_name == self.DEFAULT_PROCESSOR_NAME:
            self.views_stack.setCurrentIndex(0)
            return
        
        # Find and set the correct view
        processor_names = [self.processor_combo.itemText(i) for i in range(self.processor_combo.count())]
        try:
            if processor_name in processor_names:
                index = processor_names.index(processor_name)
                if index > 0:  # Skip DEFAULT_PROCESSOR_NAME
                    self.views_stack.setCurrentIndex(index)
        except ValueError:
            # Processor not found, stay on empty view
            self.views_stack.setCurrentIndex(0)
    
    def set_save_button_enabled(self, enabled: bool) -> None:
        """
        Enable or disable the save button.
        
        Args:
            enabled: Whether to enable the save button
        """
        self.save_button.setEnabled(enabled)
    
    def set_processing_state(self, is_processing: bool) -> None:
        """
        Set UI state during processing.
        
        Args:
            is_processing: True to show processing state, False for normal state
        """
        # Disable controls during processing
        self.upload_button.setEnabled(not is_processing)
        self.processor_combo.setEnabled(not is_processing)
        self.process_button.setEnabled(not is_processing)
        
        # Update cursor
        if is_processing:
            self.setCursor(Qt.CursorShape.WaitCursor)
        else:
            self.setCursor(Qt.CursorShape.ArrowCursor)
        
        # Update button text
        if is_processing:
            self.process_button.setText("Processing...")
        else:
            self.process_button.setText("Process Image")
    
    def show_success_message(self, message: str) -> None:
        """Show success message."""
        self._clear_all_messages()
        self.success_message.show_message(message)
    
    def show_error_message(self, message: str) -> None:
        """Show error message."""
        self._clear_all_messages()
        self.error_message.show_message(message)
    
    def show_warning_message(self, message: str) -> None:
        """Show warning message."""
        self._clear_all_messages()
        self.warning_message.show_message(message)
    
    def clear_messages(self) -> None:
        """Clear all messages."""
        self._clear_all_messages()
    
    def _clear_all_messages(self) -> None:
        """Clear all message components."""
        self.success_message.clear_message()
        self.error_message.clear_message()
        self.warning_message.clear_message()
    
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
    
    # Event handlers that emit signals for controller
    
    def _on_upload_clicked(self) -> None:
        """Handle upload button click."""
        file_name, _ = QFileDialog.getOpenFileName(
            self, "Open Image File", "",
            "Image Files (*.png *.jpg *.jpeg *.bmp *.gif)")
            
        if file_name:
            self.upload_requested.emit(file_name)
    
    def _on_processor_changed(self, processor_name: str) -> None:
        """Handle processor selection change."""
        self.processor_selection_changed.emit(processor_name)
    
    def _on_process_clicked(self) -> None:
        """Handle process button click."""
        self.process_requested.emit()
    
    def _on_save_clicked(self) -> None:
        """Handle save button click."""
        file_name, _ = QFileDialog.getSaveFileName(
            self, "Save Processed Image", "",
            "PNG Image (*.png);;JPEG Image (*.jpg);;BMP Image (*.bmp)")
        
        if file_name:
            self.save_requested.emit(file_name)
    
    def resizeEvent(self, event) -> None:
        """Handle window resize event."""
        super().resizeEvent(event)
        # Note: Image updates should be handled by controller
        # This just calls the parent resize event
    
    def cleanup(self) -> None:
        """Clean up view resources."""
        # Clear processor views
        self._processor_views.clear()
        
        # Disconnect signals
        try:
            self.upload_requested.disconnect()
            self.processor_selection_changed.disconnect()
            self.process_requested.disconnect()
            self.save_requested.disconnect()
        except RuntimeError:
            # Signals already disconnected
            pass 