import pygame
from config import SCREEN_WIDTH, SCREEN_HEIGHT
from core.state import State
from core.turn_manager import TurnManager

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.state = State.PLACING
        self.running = True
        
        #test section
        bob = 

        self.objects = []
        self.units = []
        self.cursor
        self.turn_manager = TurnManager()
    
    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            pygame.display.flip()
            self.clock.tick(60)
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

    def update(self):
        pass

    def draw(self):
        self.screen.fill((120,120,80))
        