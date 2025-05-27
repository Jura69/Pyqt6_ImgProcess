import numpy as np
import math
import cv2
from typing import Dict, Any, Literal
from models.base_model import BaseModel

class RotationModel(BaseModel):
    """
    Model for image rotation operations.
    
    Handles rotation of images around center or origin point.
    """
    
    def __init__(self) -> None:
        """Initialize rotation model with default parameters."""
        self.rotation_type: Literal["center", "origin"] = "center"
        self.degree: float = 0.0
    
    def set_rotation_type(self, rotation_type: Literal["center", "origin"]) -> None:
        """
        Set the rotation type.
        
        Args:
            rotation_type: Type of rotation - 'center' or 'origin'
            
        Raises:
            ValueError: If rotation type is invalid
        """
        if rotation_type not in ["center", "origin"]:
            raise ValueError("Rotation type must be 'center' or 'origin'")
        self.rotation_type = rotation_type
    
    def set_parameters(self, parameters: Dict[str, Any]) -> None:
        """
        Set rotation parameters.
        
        Args:
            parameters (Dict[str, Any]): Parameter values to set
            
        Raises:
            ValueError: If parameters are invalid
        """
        try:
            if "degree" in parameters:
                self.degree = float(parameters["degree"])
            if "rotation_type" in parameters:
                self.set_rotation_type(parameters["rotation_type"])
        except (ValueError, TypeError) as e:
            raise ValueError(f"Invalid rotation parameters: {e}")
    
    def process(self, image: np.ndarray) -> np.ndarray:
        """
        Process the image by rotating it.
        
        Args:
            image (np.ndarray): Input image to rotate
            
        Returns:
            np.ndarray: Rotated image
        """
        if not self.validate_image(image):
            return image
            
        return self.rotate(image, self.degree)
    
    def rotate(self, image: np.ndarray, degree: float) -> np.ndarray:
        """
        Rotate image by specified degrees.
        
        Args:
            image (np.ndarray): Input image
            degree (float): Rotation angle in degrees
            
        Returns:
            np.ndarray: Rotated image
        """
        theta = -degree * math.pi / 180
        height, width = image.shape[:2]
        
        if self.rotation_type == "center":
            MT1 = np.float32([
                [1, 0, width//2],
                [0, 1, height//2],
                [0, 0, 1]
            ])
            MR = np.float32([
                [math.cos(theta), -math.sin(theta), 0],
                [math.sin(theta), math.cos(theta), 0],
                [0, 0, 1]
            ])
            MT2 = np.float32([
                [1, 0, -width//2],
                [0, 1, -height//2],
                [0, 0, 1]
            ])
            M = MT1 @ MR @ MT2
            M = M[:2, :]
        else:
            M = np.float32([
                [math.cos(theta), -math.sin(theta), 0],
                [math.sin(theta), math.cos(theta), 0]
            ])
      
        rotated = cv2.warpAffine(image, M, (width, height))
        return rotated
    
    def get_name(self) -> str:
        """
        Get the display name of this processor.
        
        Returns:
            str: Display name
        """
        return "Rotation"
    
    def get_parameters(self) -> Dict[str, Any]:
        """
        Get current rotation parameters.
        
        Returns:
            Dict[str, Any]: Current parameter values
        """
        return {
            "degree": self.degree,
            "rotation_type": self.rotation_type
        } 