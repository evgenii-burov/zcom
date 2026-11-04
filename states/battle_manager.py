from map.grid import Grid
from map.types import GridPoint
from entities.grid_entities.base import GridEntity
from entities.grid_entities.unit import Unit, Team
from entities.grid_entities.cover import Cover
from states.base import State
from ui.hud import HUD
from ui.cursor import Cursor
from util.funcs import handle_cursor_movement
from .base import StateManager
from event_bus import EventBus, Event
from enum import Enum, auto
import pygame
import itertools
from random import random
from collections import deque
from util.funcs import draw_rectangle
from config import *
from entities.projectile import Projectile


class BattleManager(StateManager):
    def __init__(self, grid: Grid, bus: EventBus):
        super().__init__(grid, bus)
        self.cursor = Cursor()
        self.turn_manager = TurnManager()
        self.selection_manager = SelectionManager(self.cursor, self.grid, self.hud, self.turn_manager)
        self.movement_manager = MovementManager(self.cursor, self.grid, self.hud, self.turn_manager, self.selection_manager)
        self.shooting_manager = ShootingManager(self.cursor, self.grid, self.hud, self.turn_manager, self.selection_manager)
        
        self.hud.set_status("BATTLE", False, 1, MSG_RED)
        self.hud.add_tooltip("LMB/SPACE: ")
        self.hud.add_tooltip("RMB/TAB: ")
        self.hud.add_tooltip("ENTER: ")

    def handle_event(self, event: pygame.Event):
        handle_cursor_movement(event, self.cursor, self.grid)
        if self.turn_manager.animation_in_progress:
            return
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == pygame.BUTTON_LEFT:
                if self.selection_manager.selected_unit is None:
                    self.selection_manager.select_unit()
                else:
                    self.selection_manager.select_target()
            if event.button == pygame.BUTTON_RIGHT:
                self.movement_manager.move_unit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                self.bus.emit(Event.STATE_TRANSITION, state=State.PLACING)
            if event.key == pygame.K_f:
                self.shooting_manager.fire_shot()

    def update(self, time: int):
        super().update(time)
        # self.hud.set_status(self.grid.get_tile(self.cursor.position).__str__(), False, 1, MSG_BLUE)
        self.grid.update()
        self.shooting_manager.update(self.dt)

    def render(self, surface: pygame.Surface):
        self.selection_manager.render(surface)
        self.grid.render(surface, self.time)
        self.shooting_manager.render(surface)
        self.cursor.render(surface)
        self.hud.render(surface)


class TurnManager:
    def __init__(self):
        self.current_turn = 1
        self.current_team = Team.TEAM1
        self.animation_in_progress = False

class SelectionManager():
    def __init__(self, cursor:Cursor, grid: Grid, hud: HUD, turn_manager: TurnManager):
        self.cursor = cursor
        self.grid = grid
        self.hud = hud
        self.turn_manager = turn_manager
        self.selected_unit: None | Unit = None
        self.movement_tiles: list[GridPoint] = []
        self.movement_costs: dict[GridPoint, int] = {}
        self.long_movement_tiles = list[GridPoint]
        self.selected_target: None | Unit = None
        self.shot_trajectory_tiles: list[GridPoint] = []

    def deselect_unit(self):
        if self.selected_unit is not None:
            self.selected_unit.selected = False
        self.selected_unit = None
        self.movement_tiles: list[GridPoint] = []

    def deselect_target(self):
        if self.selected_target is not None:
            self.selected_target.selected = False
        self.selected_target = None
        self.shot_trajectory_tiles: list[GridPoint] = []

    def select_unit(self):
        self.deselect_unit()
        current_obj = self.grid.get_tile(self.cursor.position).obj
        if type(current_obj) is Unit:
            self.selected_unit = current_obj
            current_obj.selected = True
            self.hud.log_message("Unit selected", True, 3, MSG_BLUE)
            self.calculate_movement()

    def select_target(self):
        self.deselect_target()
        current_obj = self.grid.get_tile(self.cursor.position).obj
        if current_obj == self.selected_unit:
            return
        if type(current_obj) is Unit:
            self.selected_target = current_obj
            current_obj.selected = True
            self.hud.log_message("Target selected", True, 3, MSG_BLUE)
            self.calculate_trajectory()
        else:
            self.deselect_unit()

    def calculate_movement(self):
        if self.selected_unit is None:
            raise RuntimeError('Move calculation attempt when no unit is selected')

        start = self.selected_unit.position
        max_cost = self.selected_unit.move_speed

        costs: dict[GridPoint, int] = {start: 0}   # клетка -> стоимость пути
        queue = deque([start])

        while queue:
            current = queue.popleft()
            cost = costs[current]
            if cost == max_cost:          # дальше идти нельзя, соседей не смотрим
                continue

            x, y = current[0], current[1]
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                neighbour = (x + dx, y + dy)
                if neighbour in costs:
                    continue
                if not self.grid.in_bounds(neighbour):
                    continue
                if self.grid.occupied(neighbour):   # см. ниже
                    continue
                costs[neighbour] = cost + 1   # отмечаем сразу при добавлении в очередь
                queue.append(neighbour)

        self.movement_costs = costs
        self.movement_tiles = [tile for tile in costs if tile != start]

    def calculate_trajectory(self):
        start_tile = self.selected_unit.position
        end_tile = self.selected_target.position

        x0, y0 = start_tile
        x1, y1 = end_tile

        dx = abs(x1 - x0)
        dy = abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx - dy

        x, y = x0, y0
        self.shot_trajectory_tiles = []
        while True:
            if (x, y) != (x0, y0):          # исключаем стартовую клетку
                self.shot_trajectory_tiles.append((x, y))
            if x == x1 and y == y1:
                break
            e2 = 2 * err
            if e2 > -dy:
                err -= dy
                x += sx
            if e2 < dx:
                err += dx
                y += sy
    
    def render(self, surface: pygame.Surface):
        for tile in self.movement_tiles:
            draw_rectangle(surface, tile, TILE_REACHABLE_WIDTH, TILE_REACHABLE_HEIGHT, COLOR_REACHABLE_TILE)
        for tile in self.shot_trajectory_tiles:
            draw_rectangle(surface, tile, TILE_REACHABLE_WIDTH, TILE_REACHABLE_HEIGHT, MSG_RED)


class ShootingManager():
    def __init__(self, cursor:Cursor, grid: Grid, hud: HUD, turn_manager: TurnManager, selection_manager: SelectionManager):
        self.cursor = cursor
        self.grid = grid
        self.hud = hud
        self.turn_manager = turn_manager
        self.selection_manager = selection_manager
        self.target: GridEntity | None = None
        self.active_projectile: Projectile | None = None

    def fire_shot(self):
        if self.selection_manager.selected_target is None:
            self.hud.log_message("No target selected", True, 3, MSG_RED)
            return
        
        for tile in self.selection_manager.shot_trajectory_tiles:
            current_object = self.grid.get_tile(tile).obj
            if current_object is None:
                continue
            if random() < current_object.cover_value:
                self.target = current_object
                break
            elif self.selection_manager.selected_target == current_object:
                self.target = self.selection_manager.selected_target
                break
        
        self.active_projectile = Projectile(
            self.selection_manager.selected_unit.position,
            self.target.position
            )

        self.turn_manager.animation_in_progress = True

    def resolve_shot(self):
        self.active_projectile = None
        self.turn_manager.animation_in_progress = False
        self.hud.log_message(f'{self.target.__str__()} destroyed', True, 3, MSG_GREEN)
        self.grid.remove_object(self.target.position)
        self.target = None
        self.selection_manager.deselect_target()
        
    def update(self, dt: int):
        if not self.active_projectile:
            return
        self.active_projectile.update(dt)
        if self.active_projectile.reached_target:
            self.resolve_shot()

    def render(self, surface: pygame.Surface):
        if self.active_projectile:
            self.active_projectile.render(surface)


class MovementManager():
    def __init__(self, cursor:Cursor, grid: Grid, hud: HUD, turn_manager: TurnManager, selection_manager: SelectionManager):
        self.cursor = cursor
        self.grid = grid
        self.hud = hud
        self.turn_manager = turn_manager
        self.selection_manager = selection_manager

    def move_unit(self):
        if self.selection_manager.selected_unit is None:
            self.hud.log_message("No unit selected", True, 3, MSG_RED)
            return
        start_position = self.selection_manager.selected_unit.position
        end_position = self.cursor.position

        # Checks
        if start_position == end_position:
            self.selection_manager.deselect_unit()
            return
        if end_position not in self.selection_manager.movement_tiles:
            self.hud.log_message("Cannot reach tile", True, 3, MSG_RED)
            return

        self.selection_manager.deselect_unit()
        self.selection_manager.deselect_target()
        self.grid.move_object(start_position, end_position)
        self.hud.log_message("Unit moved", True, 3, MSG_BLUE)
