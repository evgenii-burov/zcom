from map.grid import Grid
from map.types import GridPoint
from entities.grid_entities.base import GridEntity
from entities.grid_entities.unit import Unit, Team
from entities.grid_entities.cover import Cover
from states.base import State
from ui.cursor import Cursor
from util.funcs import handle_cursor_movement
from .base import StateManager
from event_bus import EventBus, Event
from enum import Enum, auto
import pygame
import itertools
from config import *


class BattleManager(StateManager):
    def __init__(self, grid:Grid, bus: EventBus):
        super().__init__(grid, bus)
        self.cursor = Cursor()
        self.hud.set_status("BATTLE", False, 1, MSG_RED)

        self.hud.add_tooltip("LMB/SPACE: ")
        self.hud.add_tooltip("RMB/TAB: ")
        self.hud.add_tooltip("ENTER: ")


    def handle_event(self, event: pygame.Event):
        handle_cursor_movement(event, self.cursor, self.grid)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                self.bus.emit(Event.STATE_TRANSITION, state=State.PLACING)

    def update(self):
        # self.hud.set_status(self.current_placeable.__str__(), False, 1, MSG_BLUE)
        pass

    def render(self, surface: pygame.Surface):
        self.grid.render(surface)
        self.cursor.render(surface)
        self.hud.render(surface)