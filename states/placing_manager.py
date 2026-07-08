from map.grid import Grid
from map.types import GridPoint
from entities.grid_entities.base import GridEntity
from entities.grid_entities.unit import Unit, Team
from entities.grid_entities.cover import Cover
from ui.cursor import Cursor
from util.funcs import handle_cursor_movement
from .base import StateManager
from event_bus import EventBus, Event
from enum import Enum, auto
import pygame
import itertools
from config import *
from states.base import State

class Placeable(Enum):
    ERASE = auto()
    FRIENDLY_UNIT = auto()
    ENEMY_UNIT = auto()
    COVER = auto()

    def __str__(self):
        match self:
            case self.ERASE:
                return "Erasing"
            case self.FRIENDLY_UNIT:
                return "Friendly unit"
            case self.ENEMY_UNIT:
                return "Enemy unit"
            case self.COVER:
                return "Cover"
            
    def get(self, position: GridPoint):
        match self:
            case self.ERASE:
                return None
            case self.FRIENDLY_UNIT:
                return Unit(position, False, False, Team.TEAM1)
            case self.ENEMY_UNIT:
                return Unit(position, False, False, Team.TEAM2)
            case self.COVER:
                return Cover(position, False)


class PlacingManager(StateManager):
    def __init__(self, grid:Grid, bus: EventBus):
        super().__init__(grid, bus)
        self.cursor = Cursor()
        self.placeables = [x for x in Placeable]
        self.cycler = itertools.cycle(self.placeables)
        self.current_placeable = next(self.cycler)
        self.hud.set_status(self.current_placeable.__str__(), False, 1, MSG_RED)

        self.hud.add_tooltip("LMB/SPACE: Place")
        self.hud.add_tooltip("RMB/TAB: Switch entity")
        self.hud.add_tooltip("ENTER: Start battle")

        self.bus.subscribe(Event.ENTITY_PLACED, self.on_entity_placed)

    def place_object(self):
        current_object = self.current_placeable.get(self.cursor.position)
        if current_object is None:
            self.grid.remove_object(self.cursor.position)
            return
        if self.grid.get_tile(self.cursor.position).occupied:
            self.grid.remove_object(self.cursor.position)
            self.grid.place_object(current_object)
            self.bus.emit(Event.ENTITY_PLACED, obj=current_object)
            return
        self.grid.place_object(current_object)
        self.bus.emit(Event.ENTITY_PLACED, obj=current_object)

    def on_entity_placed(self, obj: GridEntity):
        self.hud.log_message(f"Entity placed: {str.lower(obj.__str__())}", True, 3, MSG_BLUE)

    def handle_event(self, event: pygame.Event):
        handle_cursor_movement(event, self.cursor, self.grid)
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == pygame.BUTTON_RIGHT:
                self.current_placeable = next(self.cycler)
            if event.button == pygame.BUTTON_LEFT:
                self.place_object()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_TAB:
                self.current_placeable = next(self.cycler)
            if event.key == pygame.K_SPACE:
                self.place_object()
            if event.key == pygame.K_RETURN:
                self.bus.emit(Event.STATE_TRANSITION, state=State.BATTLE)

    def update(self):
        self.hud.set_status(self.current_placeable.__str__(), False, 1, MSG_BLUE)

    def render(self, surface: pygame.Surface):
        self.grid.render(surface)
        self.cursor.render(surface)
        self.hud.render(surface)