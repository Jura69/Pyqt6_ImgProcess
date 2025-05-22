import numpy as np
import cv2
from models.base_model import BaseModel

class FlipModel(BaseModel):
    def __init__(self):
        self._flip_type = 0  # 0: vertical flip, 1: horizontal flip

    def get_name(self) -> str:
        return "Flip"

    def get_parameters(self) -> dict:
        return {"flip_type": self._flip_type}

    def set_parameters(self, parameters: dict):
        if "flip_type" in parameters:
            self._flip_type = parameters["flip_type"]

    def set_flip_type(self, flip_type: int):
        self._flip_type = flip_type

    def process(self, image: np.ndarray) -> np.ndarray:
        return cv2.flip(image, flipCode=self._flip_type)
