from PyQt6.QtWidgets import QWidget

class BaseController:
    def __init__(self, models, views):
        self.models = models
        self.views = views
        self._connect_signals()

    def _connect_signals(self):
        if hasattr(self.views, "parameters_changed"):
            self.views.parameters_changed.connect(self.models.set_parameters)

    def get_models(self):
        return self.models

    def get_views(self):
        return self.views 