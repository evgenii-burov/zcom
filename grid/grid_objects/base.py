import pygame
from grid.types import GridPoint

class GameObject:
    def __init__(self, position: GridPoint, hidden: bool, selected: bool):
        self.position = position
        self.hidden = hidden
        self.selected = selected
    
    def draw(self, surface: pygame.Surface):
        pass

    def update(self):
        pass
