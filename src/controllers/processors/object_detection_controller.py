from controllers.base_controller import BaseController
from models.processors.object_detection_model import ObjectDetectionModel
from views.processors.object_detection_view import ObjectDetectionView

class ObjectDetectionController(BaseController):
    """
    Controller for object detection processor.
    
    Coordinates between ObjectDetectionModel and ObjectDetectionView,
    handling parameter changes and processing requests.
    """
    
    def __init__(self) -> None:
        """Initialize object detection controller with model and view."""
        model = ObjectDetectionModel()
        view = ObjectDetectionView()
        super().__init__(model, view) 