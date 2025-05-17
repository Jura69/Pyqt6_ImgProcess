import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                           QHBoxLayout, QLabel, QPushButton, QFileDialog, 
                           QComboBox, QLineEdit, QFrame, QSizePolicy)
from PyQt6.QtGui import QPixmap, QImage
from PyQt6.QtCore import Qt, QSize
import cv2
import numpy as np

from image_processors import ProcessorFactory

class ImageProcessorApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Image Processor")
        self.setGeometry(100, 100, 1200, 800)
        
        # Create main widget and layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QHBoxLayout(main_widget)
        
        # Create left frame for original image
        self.original_frame = QFrame()
        self.original_frame.setFrameStyle(QFrame.Shape.StyledPanel)
        self.original_frame.setMinimumSize(400, 400)
        self.original_frame.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        original_layout = QVBoxLayout(self.original_frame)
        self.original_label = QLabel()
        self.original_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.original_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        original_layout.addWidget(self.original_label)
        
        # Create right frame for processed image
        self.processed_frame = QFrame()
        self.processed_frame.setFrameStyle(QFrame.Shape.StyledPanel)
        self.processed_frame.setMinimumSize(400, 400)
        self.processed_frame.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        processed_layout = QVBoxLayout(self.processed_frame)
        self.processed_label = QLabel()
        self.processed_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.processed_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        processed_layout.addWidget(self.processed_label)
        
        # Create control panel
        control_panel = QWidget()
        control_panel.setFixedWidth(200)
        control_layout = QVBoxLayout(control_panel)
        
        # Add upload button
        self.upload_button = QPushButton("Upload Image")
        self.upload_button.clicked.connect(self.upload_image)
        control_layout.addWidget(self.upload_button)
        
        # Add transformation selection
        self.transformation_combo = QComboBox()
        self.transformation_combo.addItems(["Select Transformation"] + ProcessorFactory.get_available_processors())
        self.transformation_combo.currentTextChanged.connect(self.update_controls)
        control_layout.addWidget(self.transformation_combo)
        
        # Add controls container
        self.controls_container = QWidget()
        self.controls_layout = QVBoxLayout(self.controls_container)
        control_layout.addWidget(self.controls_container)
        
        # Add process button
        self.process_button = QPushButton("Process Image")
        self.process_button.clicked.connect(self.process_image)
        control_layout.addWidget(self.process_button)
        
        # Add stretch to push controls to the top
        control_layout.addStretch()
        
        # Add frames and control panel to main layout
        main_layout.addWidget(self.original_frame)
        main_layout.addWidget(control_panel)
        main_layout.addWidget(self.processed_frame)
        
        # Initialize variables
        self.original_image = None
        self.processed_image = None
        self.current_processor = None

    def upload_image(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Open Image File", "", 
                                                 "Image Files (*.png *.jpg *.jpeg *.bmp *.gif)")
        if file_name:
            self.original_image = cv2.imread(file_name)
            self.display_image(self.original_image, self.original_label)
            
    def update_controls(self, text):
        # Clear existing controls
        while self.controls_layout.count():
            item = self.controls_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()
        
        if text == "Select Transformation":
            self.current_processor = None
            return
            
        # Create processor and its controls
        self.current_processor = ProcessorFactory.get_processor(text)
        if self.current_processor:
            for control in self.current_processor.get_controls():
                self.controls_layout.addWidget(control)

    def process_image(self):
        if self.original_image is None or self.current_processor is None:
            return
        
        self.processed_image = self.current_processor.process(self.original_image)
        self.display_image(self.processed_image, self.processed_label)

    def display_image(self, image, label):
        if image is None:
            return
            
        height, width, channel = image.shape
        bytes_per_line = 3 * width
        
        # Convert BGR to RGB
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
        # Convert numpy array to bytes
        image_bytes = rgb_image.tobytes()
        
        # Create QImage from bytes
        qt_image = QImage(image_bytes, width, height, bytes_per_line, QImage.Format.Format_RGB888)
        pixmap = QPixmap.fromImage(qt_image)
        
        # Get the frame size
        frame_size = label.size()
        
        # Calculate the scaled size while maintaining aspect ratio
        scaled_pixmap = pixmap.scaled(frame_size, 
                                    Qt.AspectRatioMode.KeepAspectRatio,
                                    Qt.TransformationMode.SmoothTransformation)
        
        label.setPixmap(scaled_pixmap)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ImageProcessorApp()
    window.show()
    sys.exit(app.exec())
