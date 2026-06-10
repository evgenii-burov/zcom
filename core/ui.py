import pygame
from objects.cursor import Cursor
from util.grid import Grid
from core.state import State
from core.placeables import Placeable
from config import SCREEN_WIDTH, SCREEN_HEIGHT, FRAMERATE, TEXT_SPACING, MSG_BLACK, MSG_GREEN, MSG_RED
from config import TOOLTIP_POSITION_X, TOOLTIP_POSITION_Y, ACTION_LOG_POSITION_X, ACTION_LOG_POSITION_Y
from config import CURRENT_TILE_INFO_POSITION_X, CURRENT_TILE_INFO_POSITION_Y
from util.types import PixelPoint


class Message:
    def __init__(self, text:str, temporary: bool, lifetime: int, color: pygame.Color):
        self.text = text
        self.temporary = temporary
        self.lifetime = lifetime
        self.color = color


class MessageBlock:
    def __init__(self, font: pygame.font):
        self.messages = []
        self.font = font
        self.line_spacing = self.font.get_height() * TEXT_SPACING

    def push(self, text:str, temporary: bool, lifetime: int, color: pygame.Color):
        self.messages.insert(0, Message(text, temporary, lifetime, color))

    def render(self, surface: pygame.Surface, position: PixelPoint):
        for message in self.messages:
            if message.temporary:
                message.lifetime -= 1
        self.messages = [message for message in self.messages if message.lifetime > 0]

        for message in self.messages:
            text_surface = self.font.render(message.text, False, message.color)
            surface.blit(text_surface, (position.x, position.y))
            position = PixelPoint(position.x, position.y + self.line_spacing)


class UI:
    def __init__(self):
        self.font = pygame.font.SysFont("monospace", 22)
        self.font.bold = True
        self.tooltip = MessageBlock(self.font)
        self.action_log = MessageBlock(self.font)

        self.PLACING_TOOLTIP = MessageBlock(self.font)
        self.PLACING_TOOLTIP.push("ARROW KEYS: move cursor", False, 1, MSG_BLACK)
        self.PLACING_TOOLTIP.push("TAB: switch object", False, 1, MSG_BLACK)

    def log_message(self, message: str, temporary: bool, lifetime_sec: float, color: pygame.Color):
        self.action_log.push(message, temporary, lifetime_sec * FRAMERATE, color)

    def draw_tooltip(self, surface: pygame.Surface, state:State):
        if state == State.PLACING:
            self.PLACING_TOOLTIP.render(surface, PixelPoint(TOOLTIP_POSITION_X, TOOLTIP_POSITION_Y))

    def draw_action_log(self, surface: pygame.Surface):
        self.action_log.render(surface, PixelPoint(ACTION_LOG_POSITION_X, ACTION_LOG_POSITION_Y))

    def draw_cursor_state(self, surface: pygame.Surface, state:State, cursor: Cursor, placeable: Placeable):
        if state == State.PLACING:
            text_surface = self.font.render(f'Cursor: {placeable.__str__()}', False, MSG_BLACK)
            surface.blit(text_surface, (CURRENT_TILE_INFO_POSITION_X, CURRENT_TILE_INFO_POSITION_Y))

    def draw(self, surface: pygame.Surface, state:State, cursor: Cursor, grid: Grid, placeable: Placeable):
        self.draw_tooltip(surface, state)
        self.draw_cursor_state(surface, state, cursor, placeable)
        self.draw_action_log(surface)

