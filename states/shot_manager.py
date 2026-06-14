from .state_manager import StateManager, State
import pygame
from ui.dummy_ui import DummyUI
from config import *
from grid.types import center

class ShotAnimationManager(StateManager):
    def __init__(self, game, ui=DummyUI()):
        super().__init__(game, ui)
        # ms
        self.time_to_update = 30
        # time elapsed (resets when time to update is hit)
        self.time_elapsed = 0
        self.shooter_and_target = self.game.shooter_and_target
        self.current_shot_position = center(self.shooter_and_target[0])


    def handle_event(self, event: pygame.event.Event):
        super().handle_event(event)

    def update(self):
        super().update()
        self.time_elapsed += self.game.ms_since_last_frame
        # Switch state condition (shot made)
        if self.current_path_index >= len(self.path) - 1:
            self.switch_state(State.PLAYER_TURN)
            return
        # Update 
        if self.time_elapsed > self.time_to_update:
            self.time_elapsed = 0
            

    def draw(self):
        super().draw()
