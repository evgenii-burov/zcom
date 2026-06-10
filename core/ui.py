import pygame
from pyexpat.errors import messages

from objects.cursor import Cursor
from util.grid import Grid
from core.state import State
from core.placeables import Placeable
from config import SCREEN_WIDTH, SCREEN_HEIGHT, FRAMERATE, TEXT_SPACING, MSG_BLACK, MSG_GREEN, MSG_RED
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
        self.messages.append(Message(text, temporary, lifetime, color))

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

    def log_message(self, message: str, color: pygame.Color):
        self.action_log.append(Message(message, 3*FRAMERATE, color))

    def draw(self, surface: pygame.Surface, state:State, cursor: Cursor, grid: Grid, placeable: Placeable):
        if state == State.PLACING:
            text = (f"Placing object: {placeable.__str__()}\n"
                    "ARROW KEYS: move cursor\n"
                    "TAB: switch object")

            self._render_multiline(surface, text, (SCREEN_WIDTH*0, SCREEN_HEIGHT*.8))

