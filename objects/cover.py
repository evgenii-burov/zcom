from objects.base import GameObject
from util.types import Point, GridPoint
import pygame
from config import COVER_HEIGHT, COVER_WIDTH, COVER_ORIGIN_X_OFFSET, COVER_ORIGIN_Y_OFFSET, COLOR_COVER

class Cover(GameObject):
    def __init__(self, grid_point:GridPoint, hidden:bool, selected: bool):
        super().__init__(grid_point, hidden, selected)
        self.color = COLOR_COVER

    def draw(self, surface:pygame.Surface):
        unit_origin_pixel_x = self.position.grid_point().pixel_point().x
        unit_origin_pixel_y = self.position.grid_point().pixel_point().y
        rect_origin_x = unit_origin_pixel_x + COVER_ORIGIN_X_OFFSET
        rect_origin_y = unit_origin_pixel_y + COVER_ORIGIN_Y_OFFSET

        unit_rect = pygame.Rect(rect_origin_x, rect_origin_y, COVER_WIDTH, COVER_HEIGHT)
        pygame.draw.rect(surface, self.color, unit_rect)