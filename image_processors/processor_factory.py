from .processors.rotation_processor import RotationProcessor
from .processors.crop_processor import CropProcessor

class ProcessorFactory:
    _processors = {
        "Rotation": RotationProcessor,
        "Crop": CropProcessor
    }
    
    @classmethod
    def get_processor(cls, name):
        return cls._processors.get(name)()
        
    @classmethod
    def get_available_processors(cls):
        return list(cls._processors.keys())