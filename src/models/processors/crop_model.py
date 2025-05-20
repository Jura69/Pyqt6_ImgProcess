import numpy as np
from models.base_model import BaseModel
from utils.imageScaling_ultil import image_scaling

class CropModel(BaseModel):
    def __init__(self):
        self._start_y = 0
        self._end_y = 0
        self._start_x = 0
        self._end_x = 0
        
    def process(self, image: np.ndarray) -> np.ndarray:
        return self._apply_crop(image)
    
    def _apply_crop(self, image: np.ndarray) -> np.ndarray:
        h, w = image.shape[:2]
        start_y = max(0, min(self._start_y, h-1))
        end_y = max(0, min(self._end_y, h))
        start_x = max(0, min(self._start_x, w-1))
        end_x = max(0, min(self._end_x, w))
        # start < end
        if end_y <= start_y or end_x <= start_x:
            return image

        # Cắt vùng ảnh
        crop = image[start_y:end_y, start_x:end_x]
        
        # Scale vùng crop ra tối đa 650x650, giữ nguyên tỉ lệ
        crop_scaled = image_scaling(crop, max_width=650, max_height=650)
        return crop_scaled
    
    def get_name(self) -> str:
        return "Crop"
    
    def get_parameters(self) -> dict:
        return {
            "start_y": self._start_y,
            "end_y": self._end_y,
            "start_x": self._start_x,
            "end_x": self._end_x
        }
    
    def set_parameters(self, parameters: dict) -> None:
        self._start_y = int(parameters.get("start_y", 0))
        self._end_y = int(parameters.get("end_y", 0))
        self._start_x = int(parameters.get("start_x", 0))
        self._end_x = int(parameters.get("end_x", 0)) 