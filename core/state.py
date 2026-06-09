from enum import Enum, auto

class State(Enum):
    PLACING = auto()
    PLAYER_TURN = auto()
    AI_TURN = auto()
    ANIMATING = auto()
    GAME_OVER = auto()