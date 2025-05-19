import sys
from PyQt6.QtWidgets import QApplication
from controllers.processors.rotation_controller import RotationController
from controllers.processors.crop_controller import CropController
from views.main_window import MainWindow

def main():
    app = QApplication(sys.argv)
    
    # Create a mapping of processor names to their controllers
    processor_controllers = {
        "Rotation": RotationController(),
        "Crop": CropController()
    }
    
    # Create and show main window
    window = MainWindow(processor_controllers)
    window.show()
    
    sys.exit(app.exec())

if __name__ == '__main__':
    main() 