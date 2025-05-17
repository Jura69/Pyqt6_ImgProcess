import cv2
import numpy as np
from PyQt6.QtWidgets import QLineEdit, QHBoxLayout, QWidget
from ..base_processor import BaseProcessor

class CropProcessor(BaseProcessor):
    def __init__(self):
        self.controls_widget = QWidget()
        layout = QHBoxLayout(self.controls_widget)
        
        # Create input fields for x, y, width, height
        self.x_input = QLineEdit()
        self.x_input.setPlaceholderText("X")
        self.y_input = QLineEdit()
        self.y_input.setPlaceholderText("Y")
        self.width_input = QLineEdit()
        self.width_input.setPlaceholderText("Width")
        self.height_input = QLineEdit()
        self.height_input.setPlaceholderText("Height")
        
        # Add inputs to layout
        layout.addWidget(self.x_input)
        layout.addWidget(self.y_input)
        layout.addWidget(self.width_input)
        layout.addWidget(self.height_input)
        
    def process(self, image):
        try:
            x = int(self.x_input.text())
            y = int(self.y_input.text())
            width = int(self.width_input.text())
            height = int(self.height_input.text())
            
            # Ensure coordinates are within image bounds
            h, w = image.shape[:2]
            x = max(0, min(x, w-1))
            y = max(0, min(y, h-1))
            width = max(1, min(width, w-x))
            height = max(1, min(height, h-y))
            
            return image[y:y+height, x:x+width]
        except ValueError:
            return image
            
    def get_controls(self):
        return [self.controls_widget]
        
    def get_name(self):
        return "Crop"