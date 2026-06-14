from .state_manager import StateManager, State
import pygame
from ui.dummy_ui import DummyUI
from config import *
from collections import deque


class MoveAnimationManager(StateManager):
    def __init__(self, game, ui=DummyUI()):
        super().__init__(game, ui)
        self.endpoints = self.game.move_endpoints
        self.reachable_tiles = self.game.reachable_tiles
        # ms
        self.time_to_update = 150
        # time elapsed (resets when time to update is hit)
        self.time_elapsed = 0
        self.path = self.calculate_path(self.endpoints)
        self.current_path_index = 0

    def calculate_path(self, endpoints: tuple) -> list[tuple]:
        adjacent = ((0, 1), (0, -1), (1, 0), (-1, 0))
        start, end = endpoints
        predecessor = {start: None}
        tiles_queued = deque([start])

        while tiles_queued:
            current_tile = tiles_queued.popleft()
            if current_tile == end:
                break
            for move in adjacent:
                neighbour_tile = (current_tile[0] + move[0], current_tile[1] + move[1])
                if (
                    neighbour_tile not in predecessor
                    and self.game.grid.in_bounds(neighbour_tile)
                    and not self.game.grid.get_tile(neighbour_tile).occupied
                    and neighbour_tile in self.reachable_tiles
                ):
                    predecessor[neighbour_tile] = current_tile
                    tiles_queued.append(neighbour_tile)

        # Backtrack from end to start
        if end not in predecessor:
            return []  # No path found
        
        path = []
        current = end
        while current is not None:
            path.append(current)
            current = predecessor[current]
        
        path.reverse()
        return path

    def handle_event(self, event: pygame.event.Event):
        super().handle_event(event)

    def update(self):
        super().update()
        self.time_elapsed += self.game.ms_since_last_frame
        if self.current_path_index >= len(self.path) - 1:
            self.switch_state(State.PLAYER_TURN)
            return
        if self.time_elapsed > self.time_to_update:
            self.time_elapsed = 0
            start = (self.path[self.current_path_index][0], self.path[self.current_path_index][1])
            end = (self.path[self.current_path_index + 1][0], self.path[self.current_path_index + 1][1])
            self.game.grid.move_object(start, end)
            self.current_path_index += 1

    def draw(self):
        super().draw()
