from .base_message import BaseMessage

class SuccessMessage(BaseMessage):
    def __init__(self):
        super().__init__("success") 