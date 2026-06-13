from __future__ import annotations
from typing import TYPE_CHECKING
from enum import Enum, auto
from states.state_objects.cursor import Cursor
from ui.base import UI

if TYPE_CHECKING:
    from game import Game


class State(Enum):
    PLACING = auto()
    PLAYER_TURN = auto()
    AI_TURN = auto()
    ANIMATING = auto()
    GAME_OVER = auto()


class StateManager:
    def __init__(self, game: Game, state:State, ui: UI):
        self.game = game
        self.state = state
        self.ui = ui

    def handle_event(self):
        pass

    def update(self):
        self.game.grid.update()
        return

    def draw(self):
        self.game.grid.draw(self.game.screen)
        return

    def switch_state(self, state_manager: StateManager):
        self.game.state_manager = state_manager



    
