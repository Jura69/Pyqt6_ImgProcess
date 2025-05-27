from .base_message import BaseMessage

class WarningMessage(BaseMessage):
    """
    Warning message component for displaying warning notifications.
    
    Inherits from BaseMessage and uses orange color scheme for warnings.
    """
    def __init__(self):
        super().__init__("warning") 