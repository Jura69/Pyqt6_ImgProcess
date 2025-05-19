from abc import ABC, abstractmethod
import cv2
import numpy as np

class BaseModel(ABC):
    """Base class for all image processors"""
    
    @abstractmethod
    def process(self, image: np.ndarray) -> np.ndarray:
        """Xử lý ảnh và trả về ảnh đã xử lý"""
        pass
    
    @abstractmethod
    def get_name(self) -> str:
        """Trả về tên của process"""
        pass
    
    @abstractmethod
    def get_parameters(self) -> dict:
        """Trả về tham số hiện tại của process"""
        pass
    
    @abstractmethod
    def set_parameters(self, parameters: dict) -> None:
        """Thiết lập tham số của process"""
        pass 