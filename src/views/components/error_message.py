from .base_message import BaseMessage

class ErrorMessage(BaseMessage):
    def __init__(self):
        super().__init__("error")