"""
Main Window Model - Business logic and state management for the main application window.

This model handles image loading, processing coordination, and state management
while being independent of the UI components.
"""

from typing import Dict, Any, Optional, Tuple
import cv2
import numpy as np
import logging
from PyQt6.QtCore import QObject, pyqtSignal

class MainWindowModel(QObject):
    """
    Model for main window managing application state and business logic.
    
    Handles image data, processor coordination, and state management
    without direct UI dependencies.
    """
    
    # Constants following CODE_STANDARDS.md
    SUPPORTED_FORMATS = ['.png', '.jpg', '.jpeg', '.bmp', '.gif']
    DEFAULT_PROCESSOR_NAME = "Select Transformation"
    
    # Signals for notifying view of state changes
    image_loaded = pyqtSignal(np.ndarray)  # Emitted when original image is loaded
    image_processed = pyqtSignal(np.ndarray)  # Emitted when processing completes
    processor_changed = pyqtSignal(str)  # Emitted when processor selection changes
    processing_started = pyqtSignal()  # Emitted when processing begins
    processing_finished = pyqtSignal()  # Emitted when processing ends
    error_occurred = pyqtSignal(str)  # Emitted when error occurs
    
    def __init__(self, processor_controllers: Dict[str, Any]) -> None:
        """
        Initialize main window model.
        
        Args:
            processor_controllers: Dictionary of processor controllers
        """
        super().__init__()
        self.processor_controllers = processor_controllers
        self._original_image: Optional[np.ndarray] = None
        self._processed_image: Optional[np.ndarray] = None
        self._current_processor_name: Optional[str] = None
        self._current_processor = None
        self._image_dimensions: Optional[Tuple[int, int]] = None
        
        self.logger = logging.getLogger(__name__)
    
    @property
    def original_image(self) -> Optional[np.ndarray]:
        """Get the original image."""
        return self._original_image
    
    @property
    def processed_image(self) -> Optional[np.ndarray]:
        """Get the processed image."""
        return self._processed_image
    
    @property
    def current_processor_name(self) -> Optional[str]:
        """Get the current processor name."""
        return self._current_processor_name
    
    @property
    def image_dimensions(self) -> Optional[Tuple[int, int]]:
        """Get image dimensions as (width, height)."""
        return self._image_dimensions
    
    @property
    def has_original_image(self) -> bool:
        """Check if original image is loaded."""
        return self._original_image is not None
    
    @property
    def has_processed_image(self) -> bool:
        """Check if processed image exists."""
        return self._processed_image is not None
    
    @property
    def can_process(self) -> bool:
        """Check if processing is possible."""
        return self.has_original_image and self._current_processor is not None
    
    def validate_image(self, image: np.ndarray) -> bool:
        """
        Validate input image according to standards.
        
        Args:
            image: Image to validate
            
        Returns:
            bool: True if image is valid, False otherwise
        """
        if image is None:
            return False
        if not isinstance(image, np.ndarray):
            return False
        if image.size == 0:
            return False
        if len(image.shape) < 2:
            return False
        return True
    
    def load_image(self, file_path: str) -> bool:
        """
        Load image from file path.
        
        Args:
            file_path: Path to image file
            
        Returns:
            bool: True if image loaded successfully, False otherwise
        """
        # Validate input parameter
        if not isinstance(file_path, str) or not file_path.strip():
            self.error_occurred.emit("Invalid file path provided")
            return False
        
        try:
            image = cv2.imread(file_path)
            if image is None:
                self.error_occurred.emit(f"Failed to load image: {file_path}")
                return False
            
            # Validate image according to standards
            if not self.validate_image(image):
                self.error_occurred.emit(f"Invalid image format: {file_path}")
                return False
            
            self._original_image = image
            self._processed_image = None  # Clear processed image
            
            # Store image dimensions
            height, width = image.shape[:2]
            self._image_dimensions = (width, height)
            
            self.logger.info(f"Image loaded: {file_path} ({width}x{height})")
            self.image_loaded.emit(image)
            
            # Update current processor view with dimensions if available
            self._update_processor_dimensions()
            
            return True
            
        except Exception as e:
            error_msg = f"Error loading image: {str(e)}"
            self.logger.error(error_msg)
            self.error_occurred.emit(error_msg)
            return False
    
    def set_processor(self, processor_name: str) -> bool:
        """
        Set current processor by name.
        
        Args:
            processor_name: Name of processor to set
            
        Returns:
            bool: True if processor set successfully, False otherwise
        """
        try:
            # Validate input parameter
            if not isinstance(processor_name, str):
                self.error_occurred.emit("Processor name must be a string")
                return False
            
            if processor_name == self.DEFAULT_PROCESSOR_NAME or processor_name == "":
                self._current_processor_name = None
                self._current_processor = None
                self.processor_changed.emit("")
                return True
            
            if processor_name not in self.processor_controllers:
                self.error_occurred.emit(f"Unknown processor: {processor_name}")
                return False
            
            self._current_processor_name = processor_name
            self._current_processor = self.processor_controllers[processor_name].get_model()
            
            self.logger.info(f"Processor changed to: {processor_name}")
            self.processor_changed.emit(processor_name)
            
            # Update processor view with current image dimensions
            self._update_processor_dimensions()
            
            return True
            
        except Exception as e:
            error_msg = f"Error setting processor: {str(e)}"
            self.logger.error(error_msg)
            self.error_occurred.emit(error_msg)
            return False
    
    def process_image(self) -> bool:
        """
        Process the current image with selected processor.
        
        Returns:
            bool: True if processing successful, False otherwise
        """
        if not self.can_process:
            self.error_occurred.emit("Cannot process: missing image or processor")
            return False
        
        try:
            self.processing_started.emit()
            self.logger.info(f"Processing image with {self._current_processor_name}")
            
            # Process the image
            self._processed_image = self._current_processor.process(self._original_image)
            
            self.logger.info("Image processing completed successfully")
            self.image_processed.emit(self._processed_image)
            self.processing_finished.emit()
            
            return True
            
        except Exception as e:
            error_msg = f"Processing failed: {str(e)}"
            self.logger.error(error_msg)
            self.error_occurred.emit(error_msg)
            self.processing_finished.emit()
            return False
    
    def save_processed_image(self, file_path: str) -> bool:
        """
        Save processed image to file.
        
        Args:
            file_path: Path to save image
            
        Returns:
            bool: True if saved successfully, False otherwise
        """
        # Validate input parameter
        if not isinstance(file_path, str) or not file_path.strip():
            self.error_occurred.emit("Invalid file path provided")
            return False
        
        if not self.has_processed_image:
            self.error_occurred.emit("No processed image to save")
            return False
        
        try:
            success = cv2.imwrite(file_path, self._processed_image)
            if success:
                self.logger.info(f"Image saved: {file_path}")
                return True
            else:
                self.error_occurred.emit(f"Failed to save image: {file_path}")
                return False
                
        except Exception as e:
            error_msg = f"Error saving image: {str(e)}"
            self.logger.error(error_msg)
            self.error_occurred.emit(error_msg)
            return False
    
    def get_processor_names(self) -> list:
        """
        Get list of available processor names.
        
        Returns:
            list: List of processor names
        """
        return [self.DEFAULT_PROCESSOR_NAME] + list(self.processor_controllers.keys())
    
    def get_processor_view(self, processor_name: str) -> Optional[Any]:
        """
        Get view for specified processor.
        
        Args:
            processor_name: Name of processor
            
        Returns:
            View widget or None if not found
        """
        if processor_name in self.processor_controllers:
            return self.processor_controllers[processor_name].get_view()
        return None
    
    def _update_processor_dimensions(self) -> None:
        """Update current processor view with image dimensions."""
        if (self._current_processor_name and 
            self._image_dimensions and 
            self._current_processor_name in self.processor_controllers):
            
            view = self.processor_controllers[self._current_processor_name].get_view()
            if view and hasattr(view, 'set_image_dimensions'):
                width, height = self._image_dimensions
                view.set_image_dimensions(width, height)
    
    def cleanup(self) -> None:
        """Clean up model resources."""
        self.logger.info("Cleaning up main window model")
        
        # Clear image data
        self._original_image = None
        self._processed_image = None
        self._current_processor = None
        self._current_processor_name = None
        self._image_dimensions = None
        
        # Disconnect all signals
        try:
            self.image_loaded.disconnect()
            self.image_processed.disconnect()
            self.processor_changed.disconnect()
            self.processing_started.disconnect()
            self.processing_finished.disconnect()
            self.error_occurred.disconnect()
        except RuntimeError:
            # Signals already disconnected
            pass 