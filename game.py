import ctypes
import sys
import pygame
from config import *
from grid.grid import Grid, GridPoint
from grid.grid_objects.unit import Unit, Team
from states.placing_manager import PlacingManager
from collections import deque

class Game:
    def __init__(self):
        # Display scale consideration
        if sys.platform == "win32":
            try:
                # Per-monitor DPI awareness (best for multi-monitor setups)
                ctypes.windll.shcore.SetProcessDpiAwareness(2)
            except Exception:
                # Fallback for older Windows
                ctypes.windll.user32.SetProcessDPIAware()
        
        # Game initialization
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.grid = Grid()
        self.clock = pygame.time.Clock()
        self.current_tick = 0
        self.state_manager = PlacingManager(self)
        self.running = True
        # For State.Placing
        # For State.PlayerTurn or EnemyTurn
        # self.teams = [x for x in Team]
        # self.current_team = 0
        # self.selected_unit = None
        # self.reachable_tiles = set()
        # self.intersected_tiles = set()
        # self.trajectory = None


    def select_unit(self):
        new_selected_unit = self.grid.get_tile(self.cursor.position).obj
        if new_selected_unit is None:
            if self.selected_unit is None:
                self.ui.log_message("The tile is empty", True, 3, MSG_RED)
                return
            else:
                self.selected_unit.selected = False
                self.selected_unit = None
                self.reachable_tiles = set()
                return
        elif type(new_selected_unit) is not Unit:
            self.ui.log_message(f"Only units are selectable", True, 3, MSG_RED)
            return
        else:
            if type(new_selected_unit) is Unit:
                if new_selected_unit.team is Team.TEAM2:
                    self.ui.log_message("Only friendly units are selectable", True, 3, MSG_RED)
                    return
        if self.selected_unit is not None:
            self.selected_unit.selected = False
            self.reachable_tiles = set()
        self.ui.log_message("Selected a unit", True, 3, MSG_BLUE)
        self.selected_unit = new_selected_unit
        self.selected_unit.selected = True
        self.calculate_reachable_tiles()

    def move_unit(self):
        if self.selected_unit is None:
            self.ui.log_message("No unit selected", True, 3, MSG_RED)
            return
        if self.cursor.position not in self.reachable_tiles:
            self.ui.log_message("Unreachable tile", True, 3, MSG_RED)
            return
        self.grid.get_tile(self.selected_unit.position).obj = None
        self.selected_unit.position = self.cursor.position

        self.grid.get_tile(self.cursor.position).obj = self.selected_unit
        self.selected_unit.selected = False
        self.selected_unit = None
        self.reachable_tiles = set()
        self.ui.log_message("Moved a unit", True, 3, MSG_BLUE)

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
                neighbour_tile = GridPoint(current_tile.x + move[0], current_tile.y + move[1])
                if self.grid.in_bounds(neighbour_tile) and not self.grid.get_tile(neighbour_tile).occupied:
                    if neighbour_tile in visited and visited[neighbour_tile] >= movement_left - 1:
                        continue
                    tiles_queued.append((neighbour_tile, movement_left - 1))

    def calculate_trajectory(self, start: GridPoint, end: GridPoint):
        iterations = 0
        self.trajectory = (start.tile_center().tuple(), end.tile_center().tuple())
        self.intersected_tiles = set()

        dx = end.x - start.x
        dy = end.y - start.y
        sx = 1 if dx > 0 else -1
        sy = 1 if dy > 0 else -1

        # How far along the ray (in units of ray length) between
        # each vertical / horizontal grid crossing
        step_x = abs(1 / dx) if dx != 0 else float('inf')
        step_y = abs(1 / dy) if dy != 0 else float('inf')

        # Distance to first crossing on each axis from start tile
        t_x = step_x * (0.5 + (0.5 - (start.x - int(start.x)))) if dx != 0 else float('inf')
        t_y = step_y * (0.5 + (0.5 - (start.y - int(start.y)))) if dy != 0 else float('inf')

        x, y = start.x, start.y
        # Simpler — since your coords are integers:
        t_x = step_x * 0.5
        t_y = step_y * 0.5

        while x != end.x or y != end.y:
            self.intersected_tiles.add(GridPoint(x, y))
            if t_x < t_y:
                t_x += step_x
                x += sx
            elif t_y < t_x:
                t_y += step_y
                y += sy
            else:
                # Exact corner crossing — add BOTH neighbours
                self.intersected_tiles.add(GridPoint(x + sx, y))
                self.intersected_tiles.add(GridPoint(x, y + sy))
                t_x += step_x
                t_y += step_y
                x += sx
                y += sy

        self.intersected_tiles.add(GridPoint(end.x, end.y))



    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            pygame.display.flip()
            self.ms_since_last_frame = self.clock.tick(FRAMERATE)
        pygame.quit()
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                return
            self.state_manager.handle_event(event)

    def _handle_player_turn(self, event):
        mods = pygame.key.get_mods()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                # Shift+space
                if mods & pygame.KMOD_SHIFT:
                    # Move unit
                    self.move_unit()
                    return
                # Space
                self.select_unit()
            if event.key == pygame.K_f and mods & pygame.KMOD_SHIFT:
                if self.selected_unit is None:
                    self.ui.log_message("No shooter selected", True, 3, MSG_RED)
                    return
                self.calculate_trajectory(self.selected_unit.position, self.cursor.position)
                return

            self._handle_cursor_movement(event)

    def update(self):
        self.state_manager.update()
        
    def draw_reachable_tiles(self):
        for position in self.reachable_tiles:
            unit_origin_pixel_x = position.grid_point().pixel_point().x
            unit_origin_pixel_y = position.grid_point().pixel_point().y
            rect_origin_x = unit_origin_pixel_x + TILE_REACHABLE_ORIGIN_X_OFFSET
            rect_origin_y = unit_origin_pixel_y + TILE_REACHABLE_ORIGIN_Y_OFFSET

            unit_rect = pygame.Rect(rect_origin_x, rect_origin_y, TILE_REACHABLE_WIDTH, TILE_REACHABLE_HEIGHT)
            pygame.draw.rect(self.screen, COLOR_REACHABLE_TILE, unit_rect)

    def draw_intersected_tiles(self):
        for position in self.intersected_tiles:
            unit_origin_pixel_x = position.grid_point().pixel_point().x
            unit_origin_pixel_y = position.grid_point().pixel_point().y
            rect_origin_x = unit_origin_pixel_x + TILE_INTERSECTED_ORIGIN_X_OFFSET
            rect_origin_y = unit_origin_pixel_y + TILE_INTERSECTED_ORIGIN_Y_OFFSET

            unit_rect = pygame.Rect(rect_origin_x, rect_origin_y, TILE_INTERSECTED_WIDTH, TILE_INTERSECTED_HEIGHT)
            pygame.draw.rect(self.screen, COLOR_INTERSECTED_TILE, unit_rect)

    def draw_trajectory(self):
        if self.trajectory is None:
            return
        pygame.draw.line(self.screen, MSG_RED, self.trajectory[0], self.trajectory[1])

    def draw(self):
        self.screen.fill(COLOR_BACKGROUND)
        self.state_manager.draw()



        