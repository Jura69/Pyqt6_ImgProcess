import numpy as np
from typing import Dict, Any, Literal
from models.base_model import BaseModel
from models.processors.lowpass_filter.gaussian import gaussian_filter
from models.processors.lowpass_filter.average import average_filter
from models.processors.lowpass_filter.median import median_filter
from models.processors.lowpass_filter.min import min_filter
from models.processors.lowpass_filter.max import max_filter

class LowpassModel(BaseModel):
    """
    Model for lowpass image filtering operations.
    
    Handles various types of lowpass filters including Gaussian, Average,
    Median, Min, and Max filters with configurable kernel sizes.
    """
    
    def __init__(self) -> None:
        """Initialize lowpass model with default parameters."""
        self._filter_type: Literal["gaussian", "average", "median", "min", "max"] = "gaussian"
        self._kernel_size: int = 3
        self._filter_functions = {
            "gaussian": gaussian_filter,
            "average": average_filter,
            "median": median_filter,
            "min": min_filter,
            "max": max_filter
        }
    
    def process(self, image: np.ndarray) -> np.ndarray:
        """
        Process the image using the selected lowpass filter.
        
        Args:
            image (np.ndarray): Input image to filter
            
        Returns:
            np.ndarray: Filtered image
        """
        if not self.validate_image(image):
            return image
            
        return self._apply_lowpass_filter(image)
    
    def _apply_lowpass_filter(self, image: np.ndarray) -> np.ndarray:
        """
        Apply the selected lowpass filter to the image.
        
        Args:
            image (np.ndarray): Input image
            
        Returns:
            np.ndarray: Filtered image
        """
        try:
            # Ensure kernel size is odd and >= 3
            kernel_size = max(3, self._kernel_size)
            if kernel_size % 2 == 0:
                kernel_size += 1
            
            # Get filter function
            filter_func = self._filter_functions[self._filter_type]
            
            # Apply filter
            filtered_image = filter_func(image, kernel_size)
            
            # Ensure output is in valid range
            return np.clip(filtered_image, 0, 255).astype(np.uint8)
            
        except Exception as e:
            # Return original image if filtering fails
            return image
    
    def set_filter_type(self, filter_type: Literal["gaussian", "average", "median", "min", "max"]) -> None:
        """
        Set the lowpass filter type.
        
        Args:
            filter_type: Type of lowpass filter to use
            
        Raises:
            ValueError: If filter type is invalid
        """
        if filter_type not in self._filter_functions:
            raise ValueError(f"Invalid filter type. Must be one of: {list(self._filter_functions.keys())}")
        self._filter_type = filter_type
    
    def get_name(self) -> str:
        """
        Get the display name of this processor.
        
        Returns:
            str: Display name
        """
        return "Lowpass Filter"
    
    def get_parameters(self) -> Dict[str, Any]:
        """
        Get current lowpass filter parameters.
        
        Returns:
            Dict[str, Any]: Current parameter values
        """
        return {
            "filter_type": self._filter_type,
            "kernel_size": self._kernel_size
        }
    
    def set_parameters(self, parameters: Dict[str, Any]) -> None:
        """
        Set lowpass filter parameters.
        
        Args:
            parameters (Dict[str, Any]): Parameter values to set
            
        Raises:
            ValueError: If parameters are invalid
        """
        try:
            if "filter_type" in parameters:
                self.set_filter_type(parameters["filter_type"])
            
            if "kernel_size" in parameters:
                kernel_size = int(parameters["kernel_size"])
                if kernel_size < 3:
                    raise ValueError("Kernel size must be at least 3")
                if kernel_size > 15:
                    raise ValueError("Kernel size must be at most 15")
                self._kernel_size = kernel_size
                
        except (ValueError, TypeError) as e:
            raise ValueError(f"Invalid lowpass filter parameters: {e}") 