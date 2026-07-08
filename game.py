import ctypes
import sys
import pygame
from config import *
from enum import Enum, auto
from map.grid import Grid
from states.base import State, StateManager
from states.placing_manager import PlacingManager
from states.battle_manager import BattleManager
from event_bus import EventBus, Event
from ui.hud import HUD


class GameManager:
    def __init__(self):
        # Display scale consideration
        if sys.platform == "win32":
            try:
                ctypes.windll.shcore.SetProcessDpiAwareness(2)
            except Exception:
                ctypes.windll.user32.SetProcessDPIAware()
        
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.grid = Grid()
        self.clock = pygame.time.Clock()
        self.bus = EventBus()
        self.bus.subscribe(Event.STATE_TRANSITION, self.on_state_transition)
        self.states: dict[State, StateManager] = {
            State.PLACING: PlacingManager(self.grid, self.bus),
            State.BATTLE: BattleManager(self.grid, self.bus)
        }
        self.current_state:StateManager = self.states[State.PLACING]
        self.running = True

    def on_state_transition(self, state: State):
        self.current_state = self.states[state]

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.render()
            pygame.display.flip()
            self.ms_since_last_frame = self.clock.tick(FRAMERATE)
        pygame.quit()
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                return
            self.current_state.handle_event(event)

    def update(self):
        self.current_state.update()

    def render(self):
        self.screen.fill(COLOR_BACKGROUND)
        self.current_state.render(self.screen)



        