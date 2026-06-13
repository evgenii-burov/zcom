from .state_manager import StateManager, State
from ui.player_turn_ui import PlayerTurnUI
from grid.grid_objects.unit import Team, Unit
from grid.types import GridPoint, to_pixel
from .state_objects.cursor import Cursor
from .util.handle_cursor_movement import handle_cursor_movement
from config import *
from collections import deque
import pygame

class PlayerTurnManager(StateManager):
    def __init__(self, game, state=State.PLAYER_TURN, ui=PlayerTurnUI()):
        super().__init__(game, state, ui)
        self.cursor = Cursor()
        self.current_team = Team.TEAM1
        self.selected_unit: Unit | None = None
        self.reachable_tiles = set()
        self.intersected_tiles = set()
        self.trajectory = None

    def move_unit(self, start: GridPoint, end: GridPoint):
        self.game.grid.move_object(start, end)
        self.selected_unit.selected = False
        self.selected_unit = None
        self.reachable_tiles = set()

    def calculate_reachable_tiles(self):
        adjacent = ((0,1),(0,-1),(1,0),(-1,0))
        visited = dict()
        tiles_queued = deque()
        tiles_queued.append((self.selected_unit.position, self.selected_unit.move_speed))
        while tiles_queued:
            current_tile, movement_left = tiles_queued.popleft()
            if current_tile not in visited:
                visited[current_tile] = movement_left
            else:
                if visited[current_tile] < movement_left:
                    visited[current_tile] = movement_left

            self.reachable_tiles.add(current_tile)
            if movement_left == 0:
                continue
            for move in adjacent:
                neighbour_tile = (current_tile[0] + move[0], current_tile[1] + move[1])
                if self.game.grid.in_bounds(neighbour_tile) and not self.game.grid.get_tile(neighbour_tile).occupied:
                    if neighbour_tile in visited and visited[neighbour_tile] >= movement_left - 1:
                        continue
                    tiles_queued.append((neighbour_tile, movement_left - 1))

    def select_unit(self, grid_point: GridPoint):
        if self.selected_unit is not None:
            self.selected_unit.selected = False
            self.selected_unit = None
            self.reachable_tiles = set()
            return
        if not self.game.grid.get_tile(grid_point).occupied and self.selected_unit is None:
            self.ui.log_message("Nothing to select", True, 3, MSG_RED)
            return
        if type(self.game.grid.get_tile(grid_point).obj) is not Unit:
            self.ui.log_message("Not a unit", True, 3, MSG_RED)
            return
        if self.game.grid.get_tile(grid_point).obj.team != Team.TEAM1:
            self.ui.log_message("Not a friendly unit", True, 3, MSG_RED)
            return
        self.selected_unit = self.game.grid.get_tile(grid_point).obj
        self.selected_unit.selected= True

        self.calculate_reachable_tiles()

    def handle_event(self, event: pygame.event.Event):
        mods = pygame.key.get_mods()
        if event.type == pygame.KEYDOWN:
            # Cursor movement
            handle_cursor_movement(event, self.cursor, (self.game.grid.width, self.game.grid.height))
            if event.key == pygame.K_SPACE:
                # Shift+space
                if mods & pygame.KMOD_SHIFT:
                    # Move unit
                    if self.game.grid.get_tile(self.cursor.position).occupied:
                        self.ui.log_message("Tile occupied", True, 3, MSG_RED)
                        return
                    if self.game.grid.get_tile(self.cursor.position).position not in self.reachable_tiles:
                        self.ui.log_message("Can't reach", True, 3, MSG_RED)
                        return
                    self.move_unit(self.selected_unit.position, self.cursor.position)
                    return
                # Space
                self.select_unit(self.cursor.position)
            # if event.key == pygame.K_f and mods & pygame.KMOD_SHIFT:
            #     if self.selected_unit is None:
            #         self.ui.log_message("No shooter selected", True, 3, MSG_RED)
            #         return
            #     self.calculate_trajectory(self.selected_unit.position, self.cursor.position)
            #     return

            
    def update(self):
        return super().update()
    
    def draw_reachable_tiles(self, surface: pygame.Surface):
        for position in self.reachable_tiles:
            tile_origin_pixel_x = to_pixel(position)[0]
            tile_origin_pixel_y = to_pixel(position)[1]
            rect_origin_x = tile_origin_pixel_x + TILE_REACHABLE_ORIGIN_X_OFFSET
            rect_origin_y = tile_origin_pixel_y + TILE_REACHABLE_ORIGIN_Y_OFFSET

            tile_rect = pygame.Rect(rect_origin_x, rect_origin_y, TILE_REACHABLE_WIDTH, TILE_REACHABLE_HEIGHT)
            pygame.draw.rect(surface, COLOR_REACHABLE_TILE, tile_rect)

    def draw(self):
        self.draw_reachable_tiles(self.game.screen)
        super().draw()
        self.cursor.draw(self.game.screen)
        self.ui.draw(self.game.screen, self.game.grid, self.cursor)