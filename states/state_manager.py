from enum import Enum, auto
from __future__ import annotations
from typing import TYPE_CHECKING
from states.state_objects.cursor import Cursor
from config import CE

if TYPE_CHECKING:
    from game import Game


class State(Enum):
    PLACING = auto()
    PLAYER_TURN = auto()
    AI_TURN = auto()
    ANIMATING = auto()
    GAME_OVER = auto()


class StateManager:
    def __init__(self, game: Game, state:State):
        self.game = game
        self.state = state

    def handle_event(self):
        pass

    def update(self):
        pass

    def draw(self):
        pass

    def switch_state(self, state_manager: StateManager):
        self.game.state_manager = state_manager



    
