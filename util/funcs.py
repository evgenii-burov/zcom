from __future__ import annotations
from typing import TYPE_CHECKING
from map.types import GridPoint, to_pixel, to_grid
from map.grid import Grid
import pygame
from config import *
if TYPE_CHECKING:
    from ui.cursor import Cursor


def draw_rectangle(surface: pygame.Surface, grid_point: GridPoint, width:int, height: int, color: pygame.Color):
    tile_top_left_point = to_pixel(grid_point)
    offset = ((TILE_SIZE - width)//2, (TILE_SIZE - height)//2)
    rect_top_left_point = (tile_top_left_point[0]+offset[0],tile_top_left_point[1]+offset[1])
    rectangle = pygame.Rect(rect_top_left_point[0], rect_top_left_point[1], width, height)
    pygame.draw.rect(surface,color,rectangle)

def handle_cursor_movement(event: pygame.Event, cursor:Cursor, grid: Grid):
    if event.type == pygame.MOUSEMOTION:
        new_position = to_grid(pygame.mouse.get_pos())
        if grid.in_bounds(new_position):
            new_position = ((new_position[0]) % grid.width,
                                        (new_position[1]) % grid.height)
            cursor.position = new_position
        else:
            return
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_LEFT:
            new_position = ((cursor.position[0] - 1) % grid.width,
                                     (cursor.position[1] + 0) % grid.height)
            cursor.position = new_position
        if event.key == pygame.K_RIGHT:
            new_position = ((cursor.position[0] + 1) % grid.width,
                                     (cursor.position[1] + 0) % grid.height)
            cursor.position = new_position
        if event.key == pygame.K_UP:
            new_position = ((cursor.position[0] + 0) % grid.width,
                                     (cursor.position[1] - 1) % grid.height)
            cursor.position = new_position
        if event.key == pygame.K_DOWN:
            new_position = ((cursor.position[0] + 0) % grid.width,
                                     (cursor.position[1] + 1) % grid.height)
            cursor.position = new_position