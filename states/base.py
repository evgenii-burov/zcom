from map.grid import Grid
from map.types import GridPoint
from enum import Enum, auto
from event_bus import EventBus
import pygame
from ui.hud import HUD

class State(Enum):
    PLACING = auto()
    BATTLE = auto()


class StateManager:
    def __init__(self, grid:Grid, bus: EventBus):
        self.grid = grid
        self.bus = bus
        self.hud = HUD()

    def handle_event(self, event: pygame.Event):
        pass

    def update(self):
        pass

    def render(self):
        pass