import pygame
from grid.grid_objects.base import GameObject
from grid.types import GridPoint
from config import COLOR_TEAM1, COLOR_TEAM2, UNIT_HEIGHT, UNIT_WIDTH, UNIT_ORIGIN_X_OFFSET, UNIT_ORIGIN_Y_OFFSET, FRAMERATE
from enum import Enum, auto


class Team(Enum):
    TEAM1 = auto()
    TEAM2 = auto()


class Unit(GameObject):
    def __init__(self, position: GridPoint, hidden: bool, selected: bool, team: Team):
        super().__init__(position, hidden, selected)
        self.team = team
        self.move_speed = 4
        self.moved = False
        self.acted = False
        self.color = COLOR_TEAM1 if self.team == Team.TEAM1 else COLOR_TEAM2

        self.blink_timer = 0
        self.blink_interval = .5
        self.blink_timer_max = self.blink_interval * FRAMERATE * 2

    def update(self):
        self.hidden = False
        if self.selected:
            self.blink_timer = (self.blink_timer + 1) % self.blink_timer_max
            if self.blink_timer > self.blink_timer_max // 2:
                self.hidden = True

    def draw(self, surface:pygame.Surface):
        if self.hidden:
            return
        unit_origin_pixel_x = self.position.grid_point().pixel_point().x
        unit_origin_pixel_y = self.position.grid_point().pixel_point().y
        rect_origin_x = unit_origin_pixel_x + UNIT_ORIGIN_X_OFFSET
        rect_origin_y = unit_origin_pixel_y + UNIT_ORIGIN_Y_OFFSET

        unit_rect = pygame.Rect(rect_origin_x, rect_origin_y, UNIT_WIDTH, UNIT_HEIGHT)
        pygame.draw.rect(surface, self.color, unit_rect)

    def __str__(self):
        return "friendly unit" if self.team == Team.TEAM1 else "enemy unit"