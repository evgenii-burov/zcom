import pygame

from objects.base import GameObject
from util.types import Point, GridPoint
from core.team import Team
from config import COLOR_TEAM1, COLOR_TEAM2, UNIT_HEIGHT, UNIT_WIDTH, UNIT_ORIGIN_X_OFFSET, UNIT_ORIGIN_Y_OFFSET


class Unit(GameObject):
    def __init__(self, position: GridPoint, hidden: bool, selected: bool, team: Team):
        super().__init__(position, hidden, selected)
        self.team = team
        self.color = COLOR_TEAM1 if self.team == Team.TEAM1 else COLOR_TEAM2

    def draw(self, surface:pygame.Surface):
        unit_origin_pixel_x = self.position.grid_point().pixel_point().x
        unit_origin_pixel_y = self.position.grid_point().pixel_point().y
        rect_origin_x = unit_origin_pixel_x + UNIT_ORIGIN_X_OFFSET
        rect_origin_y = unit_origin_pixel_y + UNIT_ORIGIN_Y_OFFSET

        unit_rect = pygame.Rect(rect_origin_x, rect_origin_y, UNIT_WIDTH, UNIT_HEIGHT)
        pygame.draw.rect(surface, self.color, unit_rect, 3)

