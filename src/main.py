import sys
from PyQt6.QtWidgets import QApplication
from controllers.processors.rotation_controller import RotationController
from controllers.processors.crop_controller import CropController
from controllers.processors.flip_controller import FlipController
from views.main_window import MainWindow

def main():
    app = QApplication(sys.argv)
    
    processor_controllers = {
        "Rotation": RotationController(),
        "Crop": CropController(),
        "Flip": FlipController()
    }
    
    window = MainWindow(processor_controllers)
    window.show()
    
    sys.exit(app.exec())

if __name__ == '__main__':
    main() 