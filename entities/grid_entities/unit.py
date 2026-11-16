import pygame
from entities.grid_entities.base import GridEntity
from map.types import GridPoint, to_pixel
from config import *
from enum import Enum, auto
from util.funcs import draw_rectangle
from math import sin

class Team(Enum):
    TEAM1 = auto()
    TEAM2 = auto()

    def __str__(self):
        match self:
            case self.TEAM1:
                return "Blue team"
            case self.TEAM2:
                return "Red team"


class Action(Enum):
    MOVE = auto()
    SHOOT = auto()

    def cost(self):
            match self:
                case self.MOVE:
                    return 1
                case self.SHOOT:
                    return 2
                

class Unit(GridEntity):
    def __init__(self, position: GridPoint, hidden: bool, selected: bool, team: Team):
        super().__init__(position, hidden)
        self.cover_value = .1
        self.selected = selected
        self.team = team

        self.max_actions = 2
        self.actions_left = 2
        self.move_speed = 4
        self.base_hit_chance = .9

        self.color = COLOR_TEAM1 if self.team == Team.TEAM1 else COLOR_TEAM2

        self.hidden = False

    def update(self):
        pass

    def check_action_availability(self, action: Action):
        return self.actions_left>0
    
    def deduct_action_points(self, action: Action):
        self.actions_left -= action.cost()
    
    def reset_action_points(self):
        self.actions_left = self.max_actions
    
    def render(self, surface:pygame.Surface, time: int):
        if not self.selected:
            self.hidden = False
        else:
            if time % (1000*60/FRAMERATE) > (1000*60/FRAMERATE) / 2:
                self.hidden = False
            else:
                self.hidden = True
        if not self.hidden:
            draw_rectangle(surface, self.position, UNIT_WIDTH, UNIT_HEIGHT, self.color)
            draw_rectangle(surface, self.position, UNIT_WIDTH*2, UNIT_HEIGHT//3, MSG_BLACK, 0, -UNIT_HEIGHT//2)
            draw_rectangle(surface, self.position, UNIT_WIDTH, UNIT_HEIGHT//4, MSG_BLACK, 0, -1.5*UNIT_HEIGHT//2)
        

    def __str__(self):
        return "Friendly unit" if self.team == Team.TEAM1 else "Enemy unit"