from abc import ABC, abstractmethod
import cv2
import numpy as np
from PyQt6.QtWidgets import QWidget

class BaseProcessor(ABC):
    """Base class for all image processors"""
    
    @abstractmethod
    def process(self, image):
        """Process the input image and return the processed image"""
        pass
    
    @abstractmethod
    def get_controls(self) -> list[QWidget]:
        """Return a list of control widgets needed for this processor"""
        pass
    
    @abstractmethod
    def get_name(self) -> str:
        """Return the name of the processor"""
        pass 