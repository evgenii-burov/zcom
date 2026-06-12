import pygame
from state_objects.cursor import Cursor

def handle_cursor_movement(self, event: pygame.event.Event, cursor: Cursor, bounds: tuple[int, int]):
    cursor_position_x, cursor_position_y = cursor.position
    new_position = (cursor_position_x, cursor_position_y)
    distance = 0
    mods = pygame.key.get_mods()
    if mods & pygame.KMOD_CTRL:
        distance = 5
    else:
        distance = 1
    if event.key == pygame.K_LEFT:
        new_position = (cursor_position_x - distance, cursor_position_y)
    elif event.key == pygame.K_RIGHT:
        new_position = (cursor_position_x + distance, cursor_position_y)
    elif event.key == pygame.K_UP:
        new_position = (cursor_position_x, cursor_position_y - distance)
    elif event.key == pygame.K_DOWN:
        new_position = (cursor_position_x, cursor_position_y + distance)
    self.cursor.move(new_position, bounds)