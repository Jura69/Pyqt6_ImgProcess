import sys
from PyQt6.QtWidgets import QApplication
from controllers.processors.rotation_controller import RotationController
from controllers.processors.crop_controller import CropController
from controllers.processors.flip_controller import FlipController
from controllers.processors.lowpass_controller import LowpassController
from controllers.main_window_controller import MainWindowController

def main():
    app = QApplication(sys.argv)
    
    processor_controllers = {
        "Rotation": RotationController(),
        "Crop": CropController(),
        "Flip": FlipController(),
        "Lowpass Filter": LowpassController()
    }
    
    # Use the new MVC structure
    main_controller = MainWindowController(processor_controllers)
    main_controller.show()
    
    # Cleanup on application exit
    def cleanup():
        main_controller.cleanup()
    
    app.aboutToQuit.connect(cleanup)
    
    sys.exit(app.exec())

if __name__ == '__main__':
    main() 