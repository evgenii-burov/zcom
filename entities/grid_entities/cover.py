from entities.grid_entities.base import GridEntity
from map.types import GridPoint, to_pixel
import pygame
from config import *
from util.funcs import draw_rectangle

class Cover(GridEntity):
    def __init__(self, grid_point:GridPoint, hidden:bool):
        super().__init__(grid_point, hidden)
        self.color = COLOR_COVER
        self.protection = .3

    def update(self):
        pass

    def render(self, surface:pygame.Surface):
        draw_rectangle(surface, self.position, COVER_WIDTH, COVER_HEIGHT, COLOR_COVER)

    def __str__(self):
        return "Cover"
    