from map.types import GridPoint, to_pixel
from config import *
import pygame
from math import sqrt
from util.funcs import draw_rectangle

class Cursor:
    def __init__(self, position: GridPoint = (GRID_WIDTH//2, GRID_HEIGHT//2)):
        self.position = position
        self.color=COLOR_CURSOR
        self.hidden = False

    def update(self):
        pass

    def render(self, surface: pygame.Surface):
        # Circular cursor
        # top_left = to_pixel(self.position)
        # center = (top_left[0] + TILE_SIZE//2, top_left[1] + TILE_SIZE//2)
        # pygame.draw.aacircle(surface, self.color, center, TILE_SIZE/sqrt(2), 3)
        # pygame.draw.aacircle(surface, (0,0,0), center, TILE_SIZE/sqrt(2)+1, 1)
        # pygame.draw.aacircle(surface, (0,0,0), center, TILE_SIZE/sqrt(2)-3, 1)
        # Rectangular cursor
        # draw_rectangle(surface, self.position, TILE_SIZE *1.1, TILE_SIZE*1.1, self.color)
        rect_size = (TILE_SIZE, TILE_SIZE)
        rectangle_surface = pygame.Surface(rect_size, pygame.SRCALPHA)
        rectangle_surface.fill((*self.color, 128))
        surface.blit(rectangle_surface, to_pixel(self.position))
