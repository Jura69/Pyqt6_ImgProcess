"""
Main Window Controller - Coordinates between MainWindowModel and MainWindowView.

This controller handles the communication between the model and view,
implementing the MVC pattern for the main application window.
"""

from typing import Dict, Any
import logging
from PyQt6.QtCore import QTimer
from models.main_window_model import MainWindowModel
from views.main_window_view import MainWindowView

class MainWindowController:
    """
    Controller for the main window coordinating model and view.
    
    Handles user interactions from the view and updates the model accordingly,
    while updating the view based on model state changes.
    """
    
    def __init__(self, processor_controllers: Dict[str, Any]) -> None:
        """
        Initialize main window controller.
        
        Args:
            processor_controllers: Dictionary of processor controllers
        """
        self.logger = logging.getLogger(__name__)
        
        # Initialize model and view
        self.model = MainWindowModel(processor_controllers)
        self.view = MainWindowView()
        
        # Setup initial state
        self._setup_initial_state()
        self._connect_signals()
        
        self.logger.info("Main window controller initialized")
    
    def get_view(self) -> MainWindowView:
        """
        Get the view instance.
        
        Returns:
            MainWindowView: The main window view
        """
        return self.view
    
    def get_model(self) -> MainWindowModel:
        """
        Get the model instance.
        
        Returns:
            MainWindowModel: The main window model
        """
        return self.model
    
    def show(self) -> None:
        """Show the main window."""
        self.view.show()
    
    def _setup_initial_state(self) -> None:
        """Setup initial state of the application."""
        # Setup processor names in combo box
        processor_names = self.model.get_processor_names()
        self.view.set_processor_names(processor_names)
        
        # Setup processor views
        processor_views = {}
        for name in self.model.processor_controllers.keys():
            processor_views[name] = self.model.get_processor_view(name)
        
        self.view.setup_processor_views(processor_views)
        
        # Initial button states
        self.view.set_save_button_enabled(False)
    
    def _connect_signals(self) -> None:
        """Connect signals between model and view."""
        # Connect view signals to controller methods
        self.view.upload_requested.connect(self._on_upload_requested)
        self.view.processor_selection_changed.connect(self._on_processor_selection_changed)
        self.view.process_requested.connect(self._on_process_requested)
        self.view.save_requested.connect(self._on_save_requested)
        
        # Connect model signals to view updates
        self.model.image_loaded.connect(self._on_image_loaded)
        self.model.image_processed.connect(self._on_image_processed)
        self.model.processor_changed.connect(self._on_processor_changed)
        self.model.processing_started.connect(self._on_processing_started)
        self.model.processing_finished.connect(self._on_processing_finished)
        self.model.error_occurred.connect(self._on_error_occurred)
        
        # Connect window resize to image refresh
        self.view.resizeEvent = self._on_window_resized
    
    # View event handlers
    
    def _on_upload_requested(self, file_path: str) -> None:
        """
        Handle upload request from view.
        
        Args:
            file_path: Path to file to upload
        """
        self.logger.info(f"Upload requested: {file_path}")
        success = self.model.load_image(file_path)
        
        if success:
            self.view.show_success_message("Image loaded successfully!")
            # Auto-clear success message after 3 seconds
            QTimer.singleShot(3000, self.view.clear_messages)
            
            # Reset save button state
            self.view.set_save_button_enabled(False)
    
    def _on_processor_selection_changed(self, processor_name: str) -> None:
        """
        Handle processor selection change from view.
        
        Args:
            processor_name: Name of selected processor
        """
        self.logger.info(f"Processor selection changed: {processor_name}")
        self.model.set_processor(processor_name)
    
    def _on_process_requested(self) -> None:
        """Handle process request from view."""
        self.logger.info("Processing requested")
        
        if not self.model.can_process:
            self.view.show_warning_message("Please load an image and select a processor first.")
            QTimer.singleShot(3000, self.view.clear_messages)
            return
        
        success = self.model.process_image()
        if success:
            self.view.show_success_message("Image processed successfully!")
            # Auto-clear success message after 3 seconds
            QTimer.singleShot(3000, self.view.clear_messages)
    
    def _on_save_requested(self, file_path: str) -> None:
        """
        Handle save request from view.
        
        Args:
            file_path: Path to save file
        """
        self.logger.info(f"Save requested: {file_path}")
        
        if not self.model.has_processed_image:
            self.view.show_warning_message("No processed image to save.")
            QTimer.singleShot(3000, self.view.clear_messages)
            return
        
        success = self.model.save_processed_image(file_path)
        if success:
            self.view.show_success_message("Image saved successfully!")
            # Auto-clear success message after 3 seconds
            QTimer.singleShot(3000, self.view.clear_messages)
    
    # Model event handlers
    
    def _on_image_loaded(self, image) -> None:
        """
        Handle image loaded event from model.
        
        Args:
            image: Loaded image array
        """
        self.view.display_original_image(image)
        self.view.clear_messages()  # Clear any previous messages
    
    def _on_image_processed(self, image) -> None:
        """
        Handle image processed event from model.
        
        Args:
            image: Processed image array
        """
        self.view.display_processed_image(image)
        self.view.set_save_button_enabled(True)
    
    def _on_processor_changed(self, processor_name: str) -> None:
        """
        Handle processor changed event from model.
        
        Args:
            processor_name: Name of new processor
        """
        self.view.set_processor_selection(processor_name)
        
        # Clear processed image when processor changes
        if processor_name and self.model.has_original_image:
            # Only clear if we have an original image to potentially reprocess
            self.view.set_save_button_enabled(False)
    
    def _on_processing_started(self) -> None:
        """Handle processing started event from model."""
        self.view.set_processing_state(True)
        self.view.show_warning_message("Processing image...")
    
    def _on_processing_finished(self) -> None:
        """Handle processing finished event from model."""
        self.view.set_processing_state(False)
    
    def _on_error_occurred(self, error_message: str) -> None:
        """
        Handle error event from model.
        
        Args:
            error_message: Error message to display
        """
        self.logger.error(f"Error occurred: {error_message}")
        self.view.show_error_message(error_message)
        # Auto-clear error message after 5 seconds
        QTimer.singleShot(5000, self.view.clear_messages)
    
    def _on_window_resized(self, event) -> None:
        """
        Handle window resize event.
        
        Args:
            event: Resize event
        """
        # Call the original resize event handler
        MainWindowView.resizeEvent(self.view, event)
        
        # Update image displays if images exist
        if self.model.has_original_image:
            self.view.display_original_image(self.model.original_image)
            
        if self.model.has_processed_image:
            self.view.display_processed_image(self.model.processed_image)
    
    def cleanup(self) -> None:
        """Clean up controller resources."""
        self.logger.info("Cleaning up main window controller")
        
        # Clean up model
        self.model.cleanup()
        
        # Clean up view
        self.view.cleanup()
        
        # Clean up processor controllers
        for controller in self.model.processor_controllers.values():
            if hasattr(controller, 'cleanup'):
                controller.cleanup()
        
        # Disconnect signals
        try:
            # Disconnect view signals
            self.view.upload_requested.disconnect()
            self.view.processor_selection_changed.disconnect()
            self.view.process_requested.disconnect()
            self.view.save_requested.disconnect()
            
            # Disconnect model signals
            self.model.image_loaded.disconnect()
            self.model.image_processed.disconnect()
            self.model.processor_changed.disconnect()
            self.model.processing_started.disconnect()
            self.model.processing_finished.disconnect()
            self.model.error_occurred.disconnect()
            
        except RuntimeError:
            # Signals already disconnected
            pass 