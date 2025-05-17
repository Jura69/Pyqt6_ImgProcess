import cv2
import numpy as np
import math
from PyQt6.QtWidgets import QLineEdit
from ..base_processor import BaseProcessor

class RotationProcessor(BaseProcessor):
    def __init__(self):
        self.degree_input = QLineEdit()
        self.degree_input.setPlaceholderText("Enter rotation degree")
        
    def process(self, image):
        try:
            degree = float(self.degree_input.text())
            return self.image_rotation(image, degree)
        except ValueError:
            return image
            
    def image_rotation(self, image, degree):
        theta = -degree * math.pi / 180
        (h, w) = image.shape[:2]
        MT1 = np.float32([[1, 0, w//2], [0, 1, h//2], [0, 0, 1]])
        MR = np.float32([[math.cos(theta), -math.sin(theta), 0], 
                        [math.sin(theta), math.cos(theta), 0], [0, 0, 1]])
        MT2 = np.float32([[1, 0, -w//2], [0, 1, -h//2], [0, 0, 1]])
        # M: final transformation matrix
        M = MT1 @ MR @ MT2
        M = M[:2, :]
        return cv2.warpAffine(image, M, (w, h))
        
    def get_controls(self):
        return [self.degree_input]
        
    def get_name(self):
        return "Rotation"