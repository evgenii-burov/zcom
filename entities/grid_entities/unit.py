import pygame
from entities.grid_entities.base import GridEntity
from map.types import GridPoint, to_pixel
from config import *
from enum import Enum, auto
from util.funcs import draw_rectangle

class Team(Enum):
    TEAM1 = auto()
    TEAM2 = auto()


class Unit(GridEntity):
    def __init__(self, position: GridPoint, hidden: bool, selected: bool, team: Team):
        super().__init__(position, hidden)
        self.render_position = position
        self.selected = selected
        self.team = team
        self.move_speed = 4
        self.color = COLOR_TEAM1 if self.team == Team.TEAM1 else COLOR_TEAM2
        self.base_hit_chance = .9

        self.blink_timer = 0
        self.blink_interval = .5
        self.blink_timer_max = self.blink_interval * FRAMERATE * 2

    def update(self):
        self.hidden = False
        if self.selected:
            self.blink_timer = (self.blink_timer + 1) % self.blink_timer_max
            if self.blink_timer > self.blink_timer_max // 2:
                self.hidden = True

    def render(self, surface:pygame.Surface):
        if self.hidden:
            return
        draw_rectangle(surface, self.render_position, UNIT_WIDTH, UNIT_HEIGHT, self.color) 
        

    def __str__(self):
        return "Friendly unit" if self.team == Team.TEAM1 else "Enemy unit"