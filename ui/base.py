import pygame
from config import FRAMERATE, TEXT_SPACING
from grid.types import PixelPoint


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
            text_surface = self.font.render(message.text, True, message.color)
            surface.blit(text_surface, position)
            position = (position[0], position[1] + self.line_spacing)


class UI:
    def __init__(self):
        pygame.font.init()
        self.font = pygame.font.SysFont("trebuchetms", 30)
        self.font.bold = False
        self.tooltip = MessageBlock(self.font)
        self.action_log = MessageBlock(self.font)

    def log_message(self, message: str, temporary: bool, lifetime_sec: float, color: pygame.Color):
        self.action_log.push(message, temporary, lifetime_sec * FRAMERATE, color)

    def draw(self, surface: pygame.Surface):
        pass
