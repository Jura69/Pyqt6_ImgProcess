import cv2
import numpy as np
from models.base_model import BaseModel

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

        crop = image[start_y:end_y, start_x:end_x]
        crop_h, crop_w = crop.shape[:2]
        # Tính hệ số scale lớn nhất mà không vượt quá frame gốc
        scale = min(h / crop_h, w / crop_w)
        new_w = int(crop_w * scale)
        new_h = int(crop_h * scale)
        # Scale vùng crop
        crop_scaled = cv2.resize(crop, (new_w, new_h), interpolation=cv2.INTER_LINEAR)
        # Tạo ảnh đen cùng kích thước gốc
        result = np.zeros_like(image)
        # Tính vị trí để dán crop vào giữa
        y_offset = (h - new_h) // 2
        x_offset = (w - new_w) // 2
        result[y_offset:y_offset+new_h, x_offset:x_offset+new_w] = crop_scaled
        return result
    
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