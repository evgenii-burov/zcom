import pygame
from map.types import GridPoint

class GridEntity:
    def __init__(self, position: GridPoint, hidden: bool):
        self.position = position
        self.hidden = hidden
    
    def update(self):
        pass
    
    def render(self, surface: pygame.Surface):
        pass

