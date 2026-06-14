from grid.grid_objects.base import GameObject
from grid.types import GridPoint, to_pixel
import pygame
from config import COVER_HEIGHT, COVER_WIDTH, COVER_ORIGIN_X_OFFSET, COVER_ORIGIN_Y_OFFSET, COLOR_COVER

class Cover(GameObject):
    def __init__(self, grid_point:GridPoint, hidden:bool, selected: bool):
        super().__init__(grid_point, hidden, selected)
        self.color = COLOR_COVER
        self.protection = .3

    def draw(self, surface:pygame.Surface):
        cover_origin_pixel_x = to_pixel(self.position)[0]
        cover_origin_pixel_y = to_pixel(self.position)[1]
        rect_origin_x = cover_origin_pixel_x + COVER_ORIGIN_X_OFFSET
        rect_origin_y = cover_origin_pixel_y + COVER_ORIGIN_Y_OFFSET

        cover_rect = pygame.Rect(rect_origin_x, rect_origin_y, COVER_WIDTH, COVER_HEIGHT)
        pygame.draw.rect(surface, self.color, cover_rect)

    def __str__(self):
        return "cover"
    