from .base import UI

class DummyUI(UI):
    def __init__(self):
        super().__init__()

    def draw(self, surface):
        return super().draw(surface)
    