import numpy as np
import math
from typing import Tuple, Literal

class RotationModel:
    """Xử lý xoay ảnh."""
    
    def __init__(self):
        self.rotation_type: Literal["center", "origin"] = "center"
        self.degree: float = 0.0
    
    def set_rotation_type(self, rotation_type: Literal["center", "origin"]) -> None:
        """Chọn kiểu xoay: quanh tâm hoặc quanh gốc (0,0)."""
        if rotation_type not in ["center", "origin"]:
            raise ValueError("Phải chọn kiểu xoay là 'center' hoặc 'origin'")
        self.rotation_type = rotation_type
    
    def set_parameters(self, parameters: dict) -> None:
        """Nhận tham số góc xoay (độ)."""
        if "degree" in parameters:
            self.degree = float(parameters["degree"])
    
    def process(self, image: np.ndarray) -> np.ndarray:
        """Xử lý ảnh với tham số hiện tại."""
        return self.rotate(image, self.degree)
    
    def rotate(self, image: np.ndarray, degree: float) -> np.ndarray:
        """Xoay ảnh theo góc (độ)."""
        if image is None:
            raise ValueError("Ảnh đầu vào không được None")
        
        # Đổi độ sang radian, âm là xoay thuận chiều kim đồng hồ
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
        rotated = np.zeros_like(image)
        for y in range(height):
            for x in range(width):
                new_x = int(M[0,0] * x + M[0,1] * y + M[0,2])
                new_y = int(M[1,0] * x + M[1,1] * y + M[1,2])
                if 0 <= new_x < width and 0 <= new_y < height:
                    rotated[new_y, new_x] = image[y, x]
        return rotated
    
    def get_name(self) -> str:
        return "Rotation"
    
    def get_parameters(self) -> dict:
        return {"degree": self.degree} 