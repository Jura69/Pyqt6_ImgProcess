import numpy as np
import cv2
from typing import Dict, Any, Literal
from models.base_model import BaseModel

class FlipModel(BaseModel):
    """
    Model for image flipping operations.
    
    Handles horizontal and vertical image flipping using OpenCV.
    """
    
    def __init__(self) -> None:
        """Initialize flip model with default parameters."""
        self._flip_type: Literal[0, 1] = 0  # 0: vertical flip, 1: horizontal flip

    def process(self, image: np.ndarray) -> np.ndarray:
        """
        Process the image by flipping it.
        
        Args:
            image (np.ndarray): Input image to flip
            
        Returns:
            np.ndarray: Flipped image
        """
        if not self.validate_image(image):
            return image
            
        return cv2.flip(image, flipCode=self._flip_type)

    def get_name(self) -> str:
        """
        Get the display name of this processor.
        
        Returns:
            str: Display name
        """
        return "Flip"

    def get_parameters(self) -> Dict[str, Any]:
        """
        Get current flip parameters.
        
        Returns:
            Dict[str, Any]: Current parameter values
        """
        return {"flip_type": self._flip_type}

    def set_parameters(self, parameters: Dict[str, Any]) -> None:
        """
        Set flip parameters.
        
        Args:
            parameters (Dict[str, Any]): Parameter values to set
            
        Raises:
            ValueError: If parameters are invalid
        """
        try:
            if "flip_type" in parameters:
                flip_type = int(parameters["flip_type"])
                if flip_type not in [0, 1]:
                    raise ValueError("Flip type must be 0 (vertical) or 1 (horizontal)")
                self._flip_type = flip_type
        except (ValueError, TypeError) as e:
            raise ValueError(f"Invalid flip parameters: {e}")

    def set_flip_type(self, flip_type: Literal[0, 1]) -> None:
        """
        Set the flip type.
        
        Args:
            flip_type: Type of flip - 0 for vertical, 1 for horizontal
            
        Raises:
            ValueError: If flip type is invalid
        """
        if flip_type not in [0, 1]:
            raise ValueError("Flip type must be 0 (vertical) or 1 (horizontal)")
        self._flip_type = flip_type
