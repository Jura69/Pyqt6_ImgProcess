# type: ignore
from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                           QLabel, QPushButton, QFileDialog, QComboBox,
                           QFrame, QSizePolicy)
from PyQt6.QtGui import QPixmap, QImage
from PyQt6.QtCore import Qt, QSize
import cv2
import numpy as np
from utils.imageScaling_ultil import image_scaling
from views.components.error_message import ErrorMessage
from views.components.sucess_message import SucessMessage

class MainWindow(QMainWindow):
    def __init__(self, processor_controllers):
        super().__init__()
        self.processor_controllers = processor_controllers
        self.original_image = None
        self.processed_image = None
        self.current_processor = None
        self.current_views = None
        self._setup_ui()

    def _setup_ui(self):
        self.setWindowTitle("Image Processor")
        self.setGeometry(100, 100, 1800, 700)
        self.setFixedSize(1800, 700)  
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QHBoxLayout(main_widget)
        # Khung hiển thị ảnh gốc và label ảnh gốc
        self.original_frame, self.original_image_label = self._create_image_frame("Original Image")
        # Khung hiển thị ảnh đã xử lý và label ảnh kết quả
        self.processed_frame, self.processed_image_label = self._create_image_frame("Processed Image")
        # Panel điều khiển
        control_panel = self._create_control_panel()
        main_layout.addWidget(self.original_frame)
        main_layout.addWidget(control_panel)
        main_layout.addWidget(self.processed_frame)

    def _create_image_frame(self, title: str):
        frame = QFrame()
        frame.setFrameStyle(QFrame.Shape.StyledPanel)
        frame.setMinimumSize(400, 400)
        frame.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        main_layout = QVBoxLayout(frame)
        label = QLabel(title)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(label)

        image_widget = QWidget()
        image_layout = QVBoxLayout(image_widget)
        image_layout.setContentsMargins(0, 0, 0, 0)
        image_label = QLabel()
        image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        image_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        image_layout.addStretch(1)
        image_layout.addWidget(image_label)
        image_layout.addStretch(1)
        main_layout.addWidget(image_widget, stretch=1)

        return frame, image_label

    def _create_control_panel(self) -> QWidget:
        panel = QWidget()
        panel.setFixedWidth(400)
        layout = QVBoxLayout(panel)
        # Nút upload ảnh
        self.upload_button = QPushButton("Upload Image")
        self.upload_button.clicked.connect(self._on_upload_clicked)
        layout.addWidget(self.upload_button)
        # Chọn processor
        self.processor_combo = QComboBox()
        self.processor_combo.addItems(["Select Transformation"] + list(self.processor_controllers.keys()))
        self.processor_combo.currentTextChanged.connect(self._on_processor_changed)
        layout.addWidget(self.processor_combo)
        # Vùng chứa views động
        self.views_container = QWidget()
        self.views_layout = QVBoxLayout(self.views_container)
        layout.addWidget(self.views_container)
        # Thông báo lỗi
        self.error_message = ErrorMessage()
        layout.addWidget(self.error_message)
        # Thông báo thành công
        self.sucess_message = SucessMessage()
        layout.addWidget(self.sucess_message)
        # Nút xử lý ảnh
        self.process_button = QPushButton("Process Image")
        self.process_button.clicked.connect(self._on_process_clicked)
        layout.addWidget(self.process_button)
        # Nút lưu ảnh
        self.save_button = QPushButton("Save Processed Image")
        self.save_button.clicked.connect(self._on_save_clicked)
        self.save_button.setEnabled(False) 
        layout.addWidget(self.save_button)
        layout.addStretch()
        return panel

    def _on_upload_clicked(self):
        file_name, _ = QFileDialog.getOpenFileName(
            self, "Open Image File", "",
            "Image Files (*.png *.jpg *.jpeg *.bmp *.gif)")
        if file_name:
            img = cv2.imread(file_name)
            self.original_image = img
            self.image_height, self.image_width = img.shape[:2]
            # Scale ảnh để hiển thị
            display_img = image_scaling(img, max_width=650, max_height=650)
            self._display_image(display_img, self.original_image_label)
            self.error_message.clear_message()
            self.save_button.setEnabled(False)  

    def _on_processor_changed(self, name: str):
        # Xoá views cũ
        while self.views_layout.count():
            item = self.views_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()
        # Nếu chưa chọn processor
        if name == "Select Transformation":
            self.current_processor = None
            self.current_views = None
            return
        try:
            controller = self.processor_controllers[name]
            self.current_processor = controller.get_models()
            self.current_views = controller.get_views()
            self.views_layout.addWidget(self.current_views)
        except KeyError as e:
            print(f"Error creating processor: {e}")

    def _on_process_clicked(self):
        if self.original_image is None:
            self.error_message.show_message("Vui lòng upload ảnh đầu vào trước!")
            return
        if self.current_processor is None:
            self.error_message.show_message("Vui lòng chọn bộ xử lý!")
            return
        self.error_message.clear_message()
        self.processed_image = self.current_processor.process(self.original_image)
        # Scale ảnh để hiển thị
        display_img = image_scaling(self.processed_image, max_width=650, max_height=650)
        self._display_image(display_img, self.processed_image_label)
        self.save_button.setEnabled(True)  # Enable save button after processing

    def _on_save_clicked(self):
        if self.processed_image is None:
            self.error_message.show_message("Không có ảnh đã xử lý để lưu!")
            return
        
        file_name, _ = QFileDialog.getSaveFileName(
            self, "Save Processed Image", "",
            "PNG Image (*.png);;JPEG Image (*.jpg);;BMP Image (*.bmp)")
        
        if file_name:
            # Lưu ảnh
            cv2.imwrite(file_name, self.processed_image)
            self.sucess_message.show_message("Đã lưu ảnh thành công!")

    def _display_image(self, image: np.ndarray, image_label: QLabel):
        if image is None:
            return
        height, width = image.shape[:2]
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        qt_image = QImage(rgb_image.tobytes(), width, height, 3 * width, QImage.Format.Format_RGB888)
        pixmap = QPixmap.fromImage(qt_image)
        image_label.setFixedSize(width, height)
        image_label.setPixmap(pixmap) 