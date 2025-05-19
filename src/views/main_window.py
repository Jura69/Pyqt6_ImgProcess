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
        self.setGeometry(100, 100, 1200, 800)
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QHBoxLayout(main_widget)
        # Khung hiển thị ảnh gốc
        self.original_frame = self._create_image_frame("Original Image")
        # Khung hiển thị ảnh đã xử lý
        self.processed_frame = self._create_image_frame("Processed Image")
        # Panel điều khiển
        control_panel = self._create_control_panel()
        main_layout.addWidget(self.original_frame)
        main_layout.addWidget(control_panel)
        main_layout.addWidget(self.processed_frame)

    def _create_image_frame(self, title: str) -> QFrame:
        frame = QFrame()
        frame.setFrameStyle(QFrame.Shape.StyledPanel)
        frame.setMinimumSize(400, 400)
        frame.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        layout = QVBoxLayout(frame)
        label = QLabel(title)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(label)
        image_label = QLabel()
        image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        image_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        layout.addWidget(image_label)
        return frame

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
        # Nút xử lý ảnh
        self.process_button = QPushButton("Process Image")
        self.process_button.clicked.connect(self._on_process_clicked)
        layout.addWidget(self.process_button)
        layout.addStretch()
        return panel

    def _on_upload_clicked(self):
        file_name, _ = QFileDialog.getOpenFileName(
            self, "Open Image File", "",
            "Image Files (*.png *.jpg *.jpeg *.bmp *.gif)")
        if file_name:
            img = cv2.imread(file_name)
            img = image_scaling(img, max_width=400, max_height=400)
            self.original_image = img
            self.image_height, self.image_width = img.shape[:2]
            self._display_image(self.original_image, self.original_frame)
            self.error_message.clear_message()

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
        # Kiểm tra đã upload ảnh chưa
        if self.original_image is None:
            self.error_message.show_message("Vui lòng upload ảnh đầu vào trước!")
            return
        # Kiểm tra đã chọn processor chưa
        if self.current_processor is None:
            self.error_message.show_message("Vui lòng chọn bộ xử lý!")
            return
        self.error_message.clear_message()
        self.processed_image = self.current_processor.process(self.original_image)
        self._display_image(self.processed_image, self.processed_frame)

    def _display_image(self, image: np.ndarray, frame: QFrame):
        if image is None:
            return
        # Lấy kích thước ảnh gốc
        if hasattr(self, "image_height") and hasattr(self, "image_width"):
            height, width = self.image_height, self.image_width
        else:
            height, width = image.shape[:2]
        # Cắt ảnh nếu lớn hơn frame
        image = image[:height, :width]
        # Chuyển BGR -> RGB
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        qt_image = QImage(rgb_image.tobytes(), width, height, 3 * width, QImage.Format.Format_RGB888)
        pixmap = QPixmap.fromImage(qt_image)
        # Hiển thị ảnh lên QLabel
        for i in range(frame.layout().count()):
            widget = frame.layout().itemAt(i).widget()
            if isinstance(widget, QLabel) and (widget.pixmap() is not None or widget.text() == ""):
                widget.setFixedSize(width, height)
                widget.setPixmap(pixmap)
                break 