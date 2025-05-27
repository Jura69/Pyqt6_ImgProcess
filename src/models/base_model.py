from abc import ABC, abstractmethod
from typing import Dict, Any
import cv2
import numpy as np

class BaseModel(ABC):
    """
    Abstract base class for all image processors.
    
    This class defines the interface that all image processing models must implement.
    Each processor should inherit from this class and implement all abstract methods.
    """
    
    @abstractmethod
    def process(self, image: np.ndarray) -> np.ndarray:
        """
        Process the input image and return the processed result.
        
        Args:
            image (np.ndarray): Input image as numpy array
            
        Returns:
            np.ndarray: Processed image as numpy array
            
        Raises:
            ValueError: If input image is invalid
        """
        pass
    
    @abstractmethod
    def get_name(self) -> str:
        """
        Get the display name of this processor.
        
        Returns:
            str: Human-readable name of the processor
        """
        pass
    
    @abstractmethod
    def get_parameters(self) -> Dict[str, Any]:
        """
        Get current parameters of the processor.
        
        Returns:
            Dict[str, Any]: Dictionary containing current parameter values
        """
        pass
    
    @abstractmethod
    def set_parameters(self, parameters: Dict[str, Any]) -> None:
        """
        Set parameters for the processor.
        
        Args:
            parameters (Dict[str, Any]): Dictionary containing parameter values
            
        Raises:
            ValueError: If parameters are invalid
            KeyError: If required parameters are missing
        """
        pass
    
    def validate_image(self, image: np.ndarray) -> bool:
        """
        Validate input image.
        
        Args:
            image (np.ndarray): Input image to validate
            
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