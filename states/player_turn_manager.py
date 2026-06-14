from .state_manager import StateManager, State
from .move_manager import MoveAnimationManager
from ui.player_turn_ui import PlayerTurnUI
from grid.grid_objects.unit import Team, Unit
from grid.grid_objects.cover import Cover
from grid.types import GridPoint, to_pixel
from .state_objects.cursor import Cursor
from .util.handle_cursor_movement import handle_cursor_movement
from config import *
from collections import deque
import pygame

class PlayerTurnManager(StateManager):
    def __init__(self, game, ui=PlayerTurnUI()):
        super().__init__(game, ui)
        self.cursor = Cursor()
        self.current_team = Team.TEAM1
        self.selected_unit: Unit | None = None
        self.game.reachable_tiles = set()
        self.intersected_tiles = set()
        self.trajectory = None
        self.shot_probability = 0

    def move_unit(self, start: GridPoint, end: GridPoint):
        # Animated motion
        self.selected_unit.selected = False
        self.shot_probability = 0
        self.game.shot_probability = self.shot_probability
        self.game.move_endpoints = (start, end)
        self.switch_state(State.MOVE_ANIMATION)

        # path = self.calculate_path

        # self.game.grid.move_object(start, end)
        # self.selected_unit.selected = False
        # self.selected_unit = None
        # self.reachable_tiles = set()

    def calculate_probability(self, start: GridPoint, end: GridPoint):
        self.shot_probability = self.selected_unit.base_hit_change

        x0, y0 = start
        x1, y1 = end
        
        dx = abs(x1 - x0)
        dy = abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx - dy
        
        excluded = {
            (x0 + i, y0 + j)
            for i in range(-1, 2)
            for j in range(-1, 2)
        }
        
        x, y = x0, y0
        
        while (x, y) != (x1, y1):
            if (x, y) not in excluded:
                tile = self.game.grid.get_tile((x, y))
                if type(tile.obj) is Cover:
                    self.shot_probability *= tile.obj.protection
            
            e2 = 2 * err
            if e2 > -dy:
                err -= dy
                x += sx
            if e2 < dx:
                err += dx
                y += sy
        self.game.shot_probability = self.shot_probability

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

            self.game.reachable_tiles.add(current_tile)
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
            self.game.reachable_tiles = set()
            self.shot_probability = 0
            self.game.shot_probability = self.shot_probability
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
        self.shot_probability = 0
        self.game.shot_probability = self.shot_probability

        self.calculate_reachable_tiles()

    def handle_event(self, event: pygame.event.Event):
        mods = pygame.key.get_mods()
        if event.type == pygame.KEYDOWN:
            # Cursor movement
            handle_cursor_movement(event, self.cursor, (self.game.grid.width, self.game.grid.height))
            if type(self.selected_unit) is not None:
                if event.key in (pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN):
                    self.calculate_probability(self.selected_unit.position, self.cursor.position)

            # Unit selection and movement
            if event.key == pygame.K_SPACE:
                # Shift+space
                if mods & pygame.KMOD_SHIFT:
                    # Move unit
                    if self.game.grid.get_tile(self.cursor.position).occupied:
                        self.ui.log_message("Tile occupied", True, 3, MSG_RED)
                        return
                    if self.game.grid.get_tile(self.cursor.position).position not in self.game.reachable_tiles:
                        self.ui.log_message("Can't reach", True, 3, MSG_RED)
                        return
                    self.move_unit(self.selected_unit.position, self.cursor.position)
                    return
                # Space
                self.select_unit(self.cursor.position)
                return
            
           
            if event.key == pygame.K_f:
                 # F: check accuracy
                if not mods & pygame.KMOD_SHIFT:
                # Shift+F: make a shot
                else:
                    if self.selected_unit is None:
                        self.ui.log_message("No shooter selected", True, 3, MSG_RED)
                        return
                    self.game.shooter_and_target = (self.selected_unit.position, self.cursor.position)
                    self.switch_state(State.SHOT_ANIMATION)
                    return

            
    def update(self):
        return super().update()
    
    def draw_reachable_tiles(self, surface: pygame.Surface):
        for position in self.game.reachable_tiles:
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