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
        self.selected_unit: None | Unit = None
        self.hud.set_status("BATTLE", False, 1, MSG_RED)

        self.hud.add_tooltip("LMB/SPACE: ")
        self.hud.add_tooltip("RMB/TAB: ")
        self.hud.add_tooltip("ENTER: ")

    def select_unit(self):
        if self.selected_unit is not None:
            self.selected_unit.selected = False
        current_obj = self.grid.get_tile(self.cursor.position).obj
        if type(current_obj) is Unit:
            self.selected_unit = current_obj
            current_obj.selected = True
            self.hud.log_message("Unit selected", True, 3, MSG_BLUE)

    def handle_event(self, event: pygame.Event):
        handle_cursor_movement(event, self.cursor, self.grid)
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == pygame.BUTTON_LEFT:
                self.select_unit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                self.bus.emit(Event.STATE_TRANSITION, state=State.PLACING)

    def update(self):
        # self.hud.set_status(self.current_placeable.__str__(), False, 1, MSG_BLUE)
        self.grid.update()

    def render(self, surface: pygame.Surface):
        self.grid.render(surface)
        self.cursor.render(surface)
        self.hud.render(surface)