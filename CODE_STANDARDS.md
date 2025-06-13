# Code Standards for PyQt6 Image Processor

## Project Overview
A PyQt6-based image processing application using MVC (Model-View-Controller) architecture for extensible image manipulation tools.

## Architecture Pattern

### Current Project Structure
```
src/
├── models/
│   ├── base_model.py              # Abstract base for all models
│   ├── main_window_model.py       # Main window business logic & state
│   └── processors/                # Processor implementations
│       ├── crop_model.py          # Crop transformation
│       ├── flip_model.py          # Flip transformation
│       ├── lowpass_model.py       # Lowpass filter with multiple algorithms
│       ├── rotation_model.py      # Rotation transformation
│       └── lowpass_filter/        # Filter implementation modules
├── views/
│   ├── main_window_view.py        # Main application UI (pure presentation)
│   ├── components/                # Reusable UI widgets
│   │   ├── base_message.py        # Message component base
│   │   ├── success_message.py     # Success notifications
│   │   ├── error_message.py       # Error notifications
│   │   ├── warning_message.py     # Warning notifications
│   │   └── base_input.py          # Input component base
│   └── processors/                # Processor-specific UI
│       ├── base_processor_view.py # Base class for processor views
│       ├── crop_view.py           # Crop controls
│       ├── flip_view.py           # Flip controls
│       ├── lowpass_view.py        # Lowpass filter controls
│       └── rotation_view.py       # Rotation controls
├── controllers/
│   ├── base_controller.py         # Abstract controller base
│   ├── main_window_controller.py  # Main application coordinator
│   └── processors/                # Processor coordinators
│       ├── crop_controller.py     # Crop MVC coordination
│       ├── flip_controller.py     # Flip MVC coordination
│       ├── lowpass_controller.py  # Lowpass MVC coordination
│       └── rotation_controller.py # Rotation MVC coordination
├── utils/
│   └── imageScaling_ultil.py      # Image scaling utilities
└── main.py                        # Application entry point
```

### MVC Pattern Implementation

#### Models Layer (`src/models/`)
- **Purpose**: Business logic, data processing, and state management
- **Key Files**:
  - `base_model.py`: Abstract interface defining processor contracts
  - `main_window_model.py`: Application state and image management
  - `processors/`: Individual transformation algorithms
  - `lowpass_filter/`: Modular filter implementations

#### Views Layer (`src/views/`)
- **Purpose**: UI components and user interaction handling
- **Key Files**:
  - `main_window_view.py`: Main application interface
  - `components/`: Reusable UI widgets (messages, inputs)
  - `processors/`: Processor-specific parameter controls

#### Controllers Layer (`src/controllers/`)
- **Purpose**: Coordinate between models and views, handle events
- **Key Files**:
  - `main_window_controller.py`: Application flow orchestration
  - `processors/`: Individual processor coordinators
  - Signal-slot connections and event handling

## Event System Design

### Current Implementation Overview
The application uses a simplified event system focused on the main window level, rather than individual processor events. The actual implementation differs from the original design in the following ways:

#### 1. Main Window Event Flow (Actually Implemented)
```python
# MainWindowModel signals (actually used)
class MainWindowModel(QObject):
    image_loaded = pyqtSignal(np.ndarray)
    image_processed = pyqtSignal(np.ndarray)    # Emitted when processing completes or image is reset
    processor_changed = pyqtSignal(str)
    processing_started = pyqtSignal()     # Emitted when processing begins
    processing_finished = pyqtSignal()    # Emitted when processing ends
    error_occurred = pyqtSignal(str)      # Emitted when errors occur

# MainWindowView message methods (actually implemented)
class MainWindowView(QMainWindow):
    def show_success_message(self, message: str) -> None:
        """Show success message using built-in message components."""
        self.success_message.show_message(message)
    
    def show_error_message(self, message: str) -> None:
        """Show error message using built-in message components."""
        self.error_message.show_message(message)
    
    def clear_messages(self) -> None:
        """Clear all active messages."""
        self.success_message.clear_message()
        self.error_message.clear_message()
        self.warning_message.clear_message()

    # MainWindowView signals for controller coordination:
    # upload_requested = pyqtSignal(str)
    # processor_selection_changed = pyqtSignal(str)
    # process_requested = pyqtSignal()
    # save_requested = pyqtSignal(str)
    # reset_requested = pyqtSignal() # Emitted when reset button is clicked
```

#### 2. Processor-Level Events (Actually Implemented)
```python
# BaseProcessorView - Simple parameter signaling
class BaseProcessorView(QWidget):
    parameters_changed = pyqtSignal(dict)  # Only signal actually used
    
    def _emit_parameters(self, parameters: Dict[str, Any]) -> None:
        """Emit parameters when UI controls change."""
        if not isinstance(parameters, dict):
            logging.error("Parameters must be a dictionary")
            return
        self.parameters_changed.emit(parameters)

# BaseController - Simple parameter handling
class BaseController(ABC):
    def _connect_signals(self) -> None:
        """Connect basic parameter signals."""
        if hasattr(self.view, "parameters_changed"):
            self.view.parameters_changed.connect(self.model.set_parameters)

# Business logic methods
def load_image(self, file_path: str) -> bool
def set_processor(self, processor_name: str) -> bool
def process_image(self) -> bool                 # Applies current processor to the current image (original or last processed state)
def save_processed_image(self, file_path: str) -> bool
def reset_to_original_image(self) -> bool      # Resets the processed image back to the originally loaded image
```

#### 3. Message Component Integration (Actually Implemented)
Only the main window has integrated message components:

```python
class MainWindowView(QMainWindow):
    def _setup_message_components(self) -> None:
        """Setup message components in main window only."""
        from views.components import WarningMessage, SuccessMessage, ErrorMessage
        
        # Create message container (fixed height to prevent UI jumping)
        self.message_container = QWidget()
        self.message_container.setFixedHeight(120)
        message_layout = QVBoxLayout(self.message_container)
        
        # Create message components
        self.warning_message = WarningMessage()
        self.success_message = SuccessMessage()
        self.error_message = ErrorMessage()
        
        # Add to container
        message_layout.addWidget(self.warning_message)
        message_layout.addWidget(self.success_message)
        message_layout.addWidget(self.error_message)
        message_layout.addStretch()  # Push messages to top
```

#### 4. Controller Event Handling (Actually Implemented)
```python
class MainWindowController:
    def _connect_signals(self) -> None:
        """Connect main window events."""
        # Processing events
        self.model.processing_started.connect(self._on_processing_started)
        self.model.processing_finished.connect(self._on_processing_finished)
        
        # Image events
        self.model.image_loaded.connect(self._on_image_loaded)
        self.model.image_processed.connect(self._on_image_processed)
        
        # Error handling
        self.model.error_occurred.connect(self._on_error_occurred)
    
    def _on_processing_started(self) -> None:
        """Handle processing start."""
        self.view.set_processing_state(True)
    
    def _on_processing_finished(self) -> None:
        """Handle processing completion."""
        self.view.set_processing_state(False)
    
    def _on_image_loaded(self, image: np.ndarray) -> None:
        """Handle successful image loading."""
        self.view.display_original_image(image)
        self.view.show_success_message("Image loaded successfully!")
        QTimer.singleShot(3000, self.view.clear_messages)

    def _on_reset_requested(self) -> None:
        """Handle reset button click."""
        self.model.reset_to_original_image()
        self.view.show_success_message("Image reset to original successfully!")
```

### What's NOT Implemented (Theoretical Patterns)

The following patterns were described in the standards but are NOT actually implemented:

❌ **Individual processor event signals**: `processing_started`, `processing_finished`, `processing_failed` on processor views  
❌ **Message signals on processor views**: `show_pending_message`, `show_success_message`, etc.  
❌ **process_image_async method**: Not implemented in controllers  
❌ **Message component setup in processor views**: Only main window has this  
❌ **Event-driven processing in individual processors**: They use simple parameter changes  

### Actual Event Patterns Used

#### 1. Parameter-Based Processing
```python
# Real implementation in processor views
class LowpassView(BaseProcessorView):
    def _on_filter_type_changed(self, filter_type: str) -> None:
        """Handle filter type change."""
        parameters = self.get_parameters()
        self._emit_parameters(parameters)  # Simple parameter emission
        
# Real controller handling
class LowpassController(BaseController):
    def _connect_signals(self) -> None:
        """Simple parameter connection."""
        super()._connect_signals()
        if hasattr(self.view, 'parameters_changed'):
            self.view.parameters_changed.connect(self.model.set_parameters)
```

#### 2. Main Window Coordination
```python
# All processing coordination happens at main window level
class MainWindowController:
    def _on_process_requested(self) -> None:
        """Handle process button click from main window."""
        if self.model.process_image():
            self.view.show_success_message("Image processed successfully!")
        else:
            self.view.show_error_message("Processing failed")
```

### Recommended Patterns (Based on Actual Implementation)

For consistency with the current codebase:

1. **Use simple parameter emission** for processor views
2. **Handle all user feedback at main window level**
3. **Keep processor views focused on UI controls only**
4. **Use the existing message components in main window**
5. **Coordinate processing through main window controller**

## Coding Standards

### 1. Type Hints (MANDATORY)
```python
# All functions must have complete type hints
def process_image(image: np.ndarray, parameters: Dict[str, Any]) -> np.ndarray:
    """Process image with given parameters."""
    pass

# Class attributes must be type-hinted
class ImageProcessor:
    def __init__(self) -> None:
        self._image: Optional[np.ndarray] = None
        self._parameters: Dict[str, Any] = {}
```

### 2. Documentation Standards
```python
class ExampleProcessor(BaseModel):
    """
    Brief description of the processor.
    
    Longer description explaining functionality, use cases,
    and important implementation details.
    """
    
    def process(self, image: np.ndarray) -> np.ndarray:
        """
        Process the input image.
        
        Args:
            image (np.ndarray): Input image as numpy array
            
        Returns:
            np.ndarray: Processed image
            
        Raises:
            ValueError: If input image is invalid
            TypeError: If image is not numpy array
        """
        pass
```

### 3. Abstract Base Classes
```python
# Models must inherit from BaseModel
class CustomProcessor(BaseModel):
    def process(self, image: np.ndarray) -> np.ndarray:
        # Implementation required
        
    def get_name(self) -> str:
        # Implementation required
        
    def get_parameters(self) -> Dict[str, Any]:
        # Implementation required
        
    def set_parameters(self, parameters: Dict[str, Any]) -> None:
        # Implementation required

# Controllers must inherit from BaseController
class CustomController(BaseController):
    def __init__(self) -> None:
        model = CustomModel()
        view = CustomView()
        super().__init__(model, view)

# Views should inherit from BaseProcessorView
class CustomView(BaseProcessorView):
    def __init__(self) -> None:
        super().__init__("Custom Processor")
        
    def get_parameters(self) -> Dict[str, Any]:
        # Implementation required
        
    def reset(self) -> None:
        # Implementation required
```

### 4. Error Handling Patterns
```python
# Input validation
def validate_image(self, image: np.ndarray) -> bool:
    """Validate input image."""
    if image is None:
        return False
    if not isinstance(image, np.ndarray):
        return False
    if image.size == 0:
        return False
    if len(image.shape) < 2:
        return False
    return True

# Parameter validation
def set_parameters(self, parameters: Dict[str, Any]) -> None:
    """Set parameters with validation."""
    try:
        self._value = int(parameters.get("value", 0))
        if self._value < 0:
            raise ValueError("Value must be non-negative")
    except (ValueError, TypeError) as e:
        raise ValueError(f"Invalid parameters: {e}")

# Resource cleanup
def cleanup(self) -> None:
    """Clean up resources."""
    try:
        if hasattr(self.view, "parameters_changed"):
            self.view.parameters_changed.disconnect()
    except RuntimeError:
        # Signal already disconnected
        pass
```

### 5. Signal-Slot Communication
```python
# View signals
class ProcessorView(BaseProcessorView):
    parameters_changed = pyqtSignal(dict)
    
    def _on_parameter_change(self) -> None:
        """Handle parameter change."""
        params = self.get_parameters()
        self._emit_parameters(params)

# Controller signal connection
class ProcessorController(BaseController):
    def _connect_signals(self) -> None:
        """Connect view signals to model."""
        super()._connect_signals()
        if hasattr(self.view, 'parameters_changed'):
            self.view.parameters_changed.connect(self.model.set_parameters)
```

### 6. Method Naming Conventions
```python
# Public methods: descriptive verbs
def process_image(self) -> np.ndarray:
def get_parameters(self) -> Dict[str, Any]:
def set_parameters(self, params: Dict[str, Any]) -> None:

# Private methods: underscore prefix
def _validate_input(self, data: Any) -> bool:
def _apply_transformation(self, image: np.ndarray) -> np.ndarray:
def _connect_signals(self) -> None:

# Event handlers: _on_ prefix
def _on_button_clicked(self) -> None:
def _on_parameter_changed(self, value: Any) -> None:
def _on_image_loaded(self, image: np.ndarray) -> None:
```

### 7. Constants and Configuration
```python
# Constants in UPPER_CASE
DEFAULT_IMAGE_WIDTH = 800
DEFAULT_IMAGE_HEIGHT = 600
SUPPORTED_FORMATS = ['.png', '.jpg', '.jpeg', '.bmp']

# Configuration as class attributes
class ImageProcessor:
    MAX_IMAGE_SIZE = 2048
    DEFAULT_QUALITY = 95
    CACHE_SIZE = 100
```

## Memory Management

### 1. Image Handling
```python
# Always validate images before processing
def process(self, image: np.ndarray) -> np.ndarray:
    if not self.validate_image(image):
        return image.copy() if image is not None else image
    
    # Create copy for processing to avoid modifying original
    working_image = image.copy()
    return self._apply_processing(working_image)

# Use image scaling utility for display
from utils.imageScaling_ultil import image_scaling

display_image = image_scaling(
    original_image, 
    max_width=frame_width, 
    max_height=frame_height
)
```

### 2. Resource Cleanup
```python
# Controllers must implement cleanup
def cleanup(self) -> None:
    """Clean up controller resources."""
    try:
        if hasattr(self.view, "parameters_changed"):
            self.view.parameters_changed.disconnect()
    except RuntimeError:
        pass

# Views must implement cleanup
def cleanup(self) -> None:
    """Clean up view resources."""
    try:
        self.parameters_changed.disconnect()
    except Exception as e:
        logging.debug(f"Error disconnecting signals: {e}")
    
    # Clear layout
    while self.layout.count():
        item = self.layout.takeAt(0)
        if item.widget():
            item.widget().deleteLater()
```

### 3. Signal Disconnection
```python
# Always disconnect signals in cleanup
def closeEvent(self, event) -> None:
    """Handle application close."""
    for controller in self.processor_controllers.values():
        if hasattr(controller, 'cleanup'):
            controller.cleanup()
    super().closeEvent(event)
```

## Extension Guidelines

### Adding New Processors

1. **Create Model** (inherit from `BaseModel`)
```python
class NewProcessor(BaseModel):
    def __init__(self) -> None:
        self._parameter: float = 0.0
    
    def process(self, image: np.ndarray) -> np.ndarray:
        # Implementation
        
    def get_name(self) -> str:
        return "New Processor"
        
    def get_parameters(self) -> Dict[str, Any]:
        return {"parameter": self._parameter}
        
    def set_parameters(self, parameters: Dict[str, Any]) -> None:
        self._parameter = float(parameters.get("parameter", 0.0))
```

2. **Create View** (inherit from `BaseProcessorView`)
```python
class NewProcessorView(BaseProcessorView):
    def __init__(self) -> None:
        super().__init__("New Processor")
        self._setup_controls()
    
    def _setup_controls(self) -> None:
        # Add UI controls
        
    def get_parameters(self) -> Dict[str, Any]:
        # Return current UI values
        
    def reset(self) -> None:
        # Reset UI to defaults
```

3. **Create Controller** (inherit from `BaseController`)
```python
class NewProcessorController(BaseController):
    def __init__(self) -> None:
        model = NewProcessor()
        view = NewProcessorView()
        super().__init__(model, view)
```

4. **Register in main.py**
```python
# Add to processor_controllers dictionary
processor_controllers = {
    "Rotation": RotationController(),
    "Crop": CropController(), 
    "Flip": FlipController(),
    "Lowpass Filter": LowpassController(),
    "New Processor": NewProcessorController(),  # Add here
}
```

## Performance Considerations

1. **Image Scaling**: Always use `image_scaling` utility for display
2. **Memory**: Create image copies only when necessary
3. **UI Updates**: Use signals for asynchronous updates
4. **Resource Cleanup**: Always implement and call cleanup methods

## Testing Guidelines

### Unit Test Structure
```python
import unittest
import numpy as np
from models.processors.rotation_model import RotationModel

class TestRotationProcessor(unittest.TestCase):
    def setUp(self) -> None:
        self.processor = RotationModel()
        self.test_image = np.zeros((100, 100, 3), dtype=np.uint8)
    
    def test_process_valid_image(self) -> None:
        # Set valid rotation angle
        self.processor.set_parameters({"angle": 90})
        result = self.processor.process(self.test_image)
        self.assertIsInstance(result, np.ndarray)
        
    def test_invalid_parameters(self) -> None:
        with self.assertRaises(ValueError):
            self.processor.set_parameters({"invalid": "value"})
    
    def test_rotation_angles(self) -> None:
        # Test common rotation angles
        for angle in [0, 90, 180, 270]:
            self.processor.set_parameters({"angle": angle})
            result = self.processor.process(self.test_image)
            self.assertIsNotNone(result)
```

## Dependencies

### Required Packages
```txt
PyQt6>=6.0.0
opencv-python>=4.5.0
numpy>=1.20.0
```

### Import Standards
```python
# Standard library imports first
import sys
import logging
from typing import Dict, Any, Optional, Tuple

# Third-party imports
import cv2
import numpy as np
from PyQt6.QtWidgets import QWidget, QVBoxLayout
from PyQt6.QtCore import pyqtSignal

# Local imports last
from models.base_model import BaseModel
from utils.imageScaling_ultil import image_scaling
```

## File Organization Rules

1. **One class per file** (except small helper classes)
2. **Descriptive file names** matching class names
3. **Consistent directory structure** following MVC pattern
4. **Utils for shared functionality** only

## Logging Standards

```python
import logging

# Use module-level logger
logger = logging.getLogger(__name__)

# Log levels:
# DEBUG: Detailed diagnostic info
# INFO: General operational messages
# WARNING: Something unexpected happened
# ERROR: Error occurred but program continues
# CRITICAL: Serious error, program may abort

# Example usage
logger.debug("Processing started")
logger.info("Image loaded successfully")
logger.warning("Parameter out of range, using default")
logger.error("Failed to process image")
```

## Shared Components and Reusability

### 1. Process Button Strategy
The application uses a **shared processing approach** to avoid code duplication:

**Default Pattern (Recommended)**: Use the main window's shared "Process Image" button
```python
# Processor views should NOT include individual process buttons by default
class CustomProcessorView(BaseProcessorView):
    def __init__(self) -> None:
        super().__init__("Custom Processor")  # No process button
        self._setup_controls()
```

### 2. Component Reusability Guidelines
- **Message Components**: Always use shared `SuccessMessage`, `ErrorMessage`, `WarningMessage`
- **Input Controls**: Create reusable slider, combobox components when patterns emerge  
- **Layout Patterns**: Extract common layout patterns into base methods
- **Parameter Emission**: Use consistent `_emit_parameters()` pattern for all processor views

### 3. Shared vs Individual Controls Decision Matrix
| Scenario | Use Shared Button | Individual Implementation |
|----------|------------------|----------------------|
| Standard processing | ✅ Main window button | ❌ Avoid duplication |
| Real-time preview | ❌ Too frequent updates | ✅ Parameter-based updates |
| Batch operations | ✅ Main window button | ❌ Standard workflow |
| Interactive effects | ❌ Main controls | ✅ Live parameter changes |

## Main Window Refactoring Guide

### Overview

The application has been successfully refactored from a monolithic structure to MVC (Model-View-Controller) pattern to clearly separate UI and business logic for better maintainability and extensibility.

### Architecture Before Refactoring

```
src/views/main_window.py (269 lines)
├── UI setup methods
├── Business logic methods  
├── Event handlers
└── Image processing logic
```

**Issues with the old structure:**
- ❌ Mixed UI and business logic
- ❌ Difficult to test and maintain
- ❌ Hard to extend with new features
- ❌ Violated Single Responsibility Principle

### Architecture After Refactoring

#### 1. MainWindowModel (`src/models/main_window_model.py`)
**Purpose:** State management and business logic
```python
class MainWindowModel(QObject):
    # Signals for state changes
    image_loaded = pyqtSignal(np.ndarray)
    image_processed = pyqtSignal(np.ndarray)
    processor_changed = pyqtSignal(str)
    
    # Business logic methods
    def load_image(self, file_path: str) -> bool
    def set_processor(self, processor_name: str) -> bool
    def process_image(self) -> bool                 # Applies current processor to the current image (original or last processed state)
    def save_processed_image(self, file_path: str) -> bool
    def reset_to_original_image(self) -> bool      # Resets the processed image back to the originally loaded image
```

**Benefits:**
- ✅ Completely separated from UI
- ✅ Easily unit testable
- ✅ Centralized state management
- ✅ Reusable with different UIs

#### 2. MainWindowView (`src/views/main_window_view.py`)
**Purpose:** Only UI components and presentation logic
```python
class MainWindowView(QMainWindow):
    # User interaction signals
    upload_requested = pyqtSignal(str)
    processor_selection_changed = pyqtSignal(str)
    process_requested = pyqtSignal()
    save_requested = pyqtSignal(str)
    reset_requested = pyqtSignal()                 # Emitted when user clicks the 'Reset Image' button
    
    # UI-only methods
    def display_original_image(self, image: np.ndarray)
    def display_processed_image(self, image: np.ndarray)
    def set_processing_state(self, is_processing: bool)
    def show_success_message(self, message: str)
    # UI elements include: 
    # - Buttons: "Upload Image", "Process Image", "Save Processed Image", "Reset Image"
    # - Dropdown: Processor selection (QComboBox)
    # - Image display areas for original and processed images.
```

**Benefits:**
- ✅ Focused on presentation layer
- ✅ No business logic
- ✅ Easy to change UI
- ✅ Clear separation of concerns

#### 3. MainWindowController (`src/controllers/main_window_controller.py`)
**Purpose:** Coordinates between Model and View
```python
class MainWindowController:
    def __init__(self, processor_controllers: Dict[str, Any]):
        self.model = MainWindowModel(processor_controllers)
        self.view = MainWindowView()
        self._connect_signals()
    
    # Event handlers
    def _on_upload_requested(self, file_path: str)
    def _on_process_requested(self)
    def _on_image_loaded(self, image)
    def _on_save_requested(self, file_path: str)     # Handles view's save_requested signal
    def _on_reset_requested(self)                    # Handles view's reset_requested signal. Calls model.reset_to_original_image(), shows success message, and updates UI state (e.g., disables save button).
```

**Benefits:**
- ✅ Separates Model and View
- ✅ Handles event-driven communication
- ✅ Easy to debug and maintain
- ✅ Follows proper MVC pattern

### Migration Path

#### Current Implementation:
The project now uses pure MVC architecture:

```python
# Standard way (current implementation)
from controllers.main_window_controller import MainWindowController
controller = MainWindowController(processor_controllers)
controller.show()
```

#### Architecture Benefits:
1. **Pure MVC:** No compatibility layers, clean architecture
2. **Direct Usage:** Import and use controllers directly
3. **Type Safety:** Full type hints and IDE support
4. **Standards Compliant:** Follows all CODE_STANDARDS.md requirements

### File Structure

```
src/
├── models/
│   └── main_window_model.py       # Business logic & state
├── views/
│   └── main_window_view.py        # Pure UI components
├── controllers/
│   └── main_window_controller.py  # MVC coordinator
└── main.py                       # Uses MainWindowController directly
```

### Benefits of New Architecture

#### 1. **Separation of Concerns**
- Model: Only handles data and business logic
- View: Only handles UI and user interactions  
- Controller: Coordinates between Model and View

#### 2. **Testability**
```python
# Test business logic separately
def test_image_loading():
    model = MainWindowModel({})
    assert model.load_image("test.jpg") == True
    assert model.has_original_image == True

# Test UI separately
def test_ui_state():
    view = MainWindowView()
    view.set_processing_state(True)
    assert not view.upload_button.isEnabled()
```

#### 3. **Extensibility**
- Easy to add new features
- Can create UI alternatives (web, mobile)
- Plugin architecture easily implementable

#### 4. **Maintainability**
- Clear, readable code
- Bugs easier to locate and fix
- Safer refactoring

### Code Standards Compliance

This refactoring follows **CODE_STANDARDS.md**:

- ✅ **Type Hints:** All methods have complete type hints
- ✅ **Documentation:** Detailed docstrings for every method
- ✅ **Error Handling:** Proper exception handling and logging
- ✅ **Signal-Slot:** Clean signal-slot communication
- ✅ **Memory Management:** Proper cleanup methods
- ✅ **MVC Pattern:** Correct architecture pattern

### Usage Examples

#### Basic Usage:
```python
from controllers.main_window_controller import MainWindowController

# Initialize
controller = MainWindowController(processor_controllers)
controller.show()

# Access components if needed
model = controller.get_model()
view = controller.get_view()
```

#### Advanced Usage:
```python
# Custom event handling
def on_custom_event():
    if controller.get_model().has_original_image:
        controller.get_view().show_success_message("Ready to process!")

# Connect custom signals
controller.get_model().image_loaded.connect(on_custom_event)
```

#### Testing:
```python
# Test individual components
model = MainWindowModel({})
view = MainWindowView()
controller = MainWindowController({})

# Mock dependencies for testing
```

### Refactoring Summary

This refactoring brings:
- **Better Architecture:** Pure MVC pattern without compatibility layers
- **Improved Maintainability:** Clean, readable and modifiable code
- **Enhanced Testability:** Individual component testing
- **Future-Proof:** Easy to extend and adapt to new requirements
- **Standards Compliant:** Fully follows CODE_STANDARDS.md requirements
- **Type Safety:** Complete type hints and validation
- **Clean Structure:** No legacy code or compatibility layers

The new structure provides a solid foundation for scalable development with clean MVC architecture.

## This document ensures:
- ✅ Consistent code structure across all components
- ✅ Type safety and documentation standards
- ✅ Memory-efficient resource management
- ✅ Clear extension patterns for new processors
- ✅ Maintainable and scalable architecture
- ✅ AI model compatibility for future development
- ✅ Comprehensive refactoring guidance
- ✅ Migration path for existing code
- ✅ Testing strategies for all components