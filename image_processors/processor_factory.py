from .processors.rotation_processor import RotationProcessor
from .processors.crop_processor import CropProcessor

class ProcessorFactory:
    """Factory class for creating image processors"""
    
    _processors = {
        "Rotation": RotationProcessor,
        "Crop": CropProcessor
    }
    
    @classmethod
    def get_processor(cls, name):
        return cls._processors.get(name)()
    
    @classmethod
    def get_available_processors(cls):
        """Get list of available processor names"""
        return list(cls._processors.keys())
    
    @classmethod
    def register_processor(cls, name: str, processor_class):
        """Register a new processor type"""
        cls._processors[name] = processor_class 