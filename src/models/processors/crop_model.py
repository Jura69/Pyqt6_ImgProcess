import numpy as np
from typing import Dict, Any
from models.base_model import BaseModel
from utils.imageScaling_ultil import image_scaling

class CropModel(BaseModel):
    """
    Model for image cropping operations.
    
    Handles cropping of images based on specified coordinates.
    """
    
    def __init__(self) -> None:
        """Initialize crop model with default parameters."""
        self._x1: int = 0
        self._x2: int = 0
        self._y1: int = 0
        self._y2: int = 0
        
    def process(self, image: np.ndarray) -> np.ndarray:
        """
        Process the image by cropping it to specified coordinates.
        
        Args:
            image (np.ndarray): Input image to crop
            
        Returns:
            np.ndarray: Cropped image
        """
        if not self.validate_image(image):
            return image
            
        return self._apply_crop(image)
    
    def _apply_crop(self, image: np.ndarray) -> np.ndarray:
        """
        Apply cropping operation to the image.
        
        Args:
            image (np.ndarray): Input image
            
        Returns:
            np.ndarray: Cropped image
        """
        height, width = image.shape[:2]
        
        # Validate coordinates
        if self._y2 <= self._y1 or self._x2 <= self._x1:
            return image
            
        # Ensure coordinates are within image bounds
        y1 = max(0, min(self._y1, height - 1))
        y2 = max(0, min(self._y2, height))
        x1 = max(0, min(self._x1, width - 1))
        x2 = max(0, min(self._x2, width))
        
        # Apply crop using numpy array slicing
        cropped = image[y1:y2, x1:x2]
        return cropped
    
    def get_name(self) -> str:
        """
        Get the display name of this processor.
        
        Returns:
            str: Display name
        """
        return "Crop"
    
    def get_parameters(self) -> Dict[str, Any]:
        """
        Get current crop parameters.
        
        Returns:
            Dict[str, Any]: Current parameter values
        """
        return {
            "x1": self._x1,
            "x2": self._x2,
            "y1": self._y1,
            "y2": self._y2
        }
    
    def set_parameters(self, parameters: Dict[str, Any]) -> None:
        """
        Set crop parameters.
        
        Args:
            parameters (Dict[str, Any]): Parameter values to set
            
        Raises:
            ValueError: If parameters are invalid
        """
        try:
            self._x1 = int(parameters.get("x1", 0))
            self._x2 = int(parameters.get("x2", 0))
            self._y1 = int(parameters.get("y1", 0))
            self._y2 = int(parameters.get("y2", 0))
        except (ValueError, TypeError) as e:
            raise ValueError(f"Invalid crop parameters: {e}") 