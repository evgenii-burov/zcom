import pygame
from util.types import Point

class GameObject:
    def __init__(self, position: Point, hidden: bool, selected: bool):
        self.position = position
        self.hidden = hidden
        self.selected = selected
    
    def draw(self, surface: pygame.Surface):
        pass

    def update(self):
        pass
