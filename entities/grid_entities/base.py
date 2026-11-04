import pygame
from map.types import GridPoint

class GridEntity:
    def __init__(self, position: GridPoint, hidden: bool):
        self.position = position
        self.hidden = hidden
        self.cover_value = 0
    
    def update(self):
        pass
    
    def render(self, surface: pygame.Surface, time: int):
        pass

