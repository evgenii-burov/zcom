import pygame
from config import *
from core.state import State
from core.turn_manager import TurnManager
from objects.cursor import Cursor
from util.types import Point, GridPoint, PixelPoint, Direction
from util.grid import Grid

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.grid = Grid()
        self.clock = pygame.time.Clock()
        self.state = State.PLACING
        self.running = True

        self.objects = []
        self.units = []
        self.cursor = Cursor(GridPoint(GRID_WIDTH/2,GRID_HEIGHT/2), False, False, self.grid)
        # self.cursor = Cursor(Point(0, 0), False, False)

        self.turn_manager = TurnManager()
    
    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            pygame.display.flip()
            self.clock.tick(FRAMERATE)
        pygame.quit()
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif self.state == State.PLACING:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.cursor.move(Direction.LEFT)
                    elif event.key == pygame.K_RIGHT:
                        self.cursor.move(Direction.RIGHT)
                    elif event.key == pygame.K_UP:
                        self.cursor.move(Direction.UP)
                    elif event.key == pygame.K_DOWN:
                        self.cursor.move(Direction.DOWN)

    def update(self):
        # objects
        # cursor
        self.cursor.update()

    def draw(self):
        self.screen.fill(COLOR_BACKGROUND)
        # grid
        self.grid.draw(self.screen)
        # objects
        # cursor
        if not self.cursor.hidden:
            self.cursor.draw(self.screen)

        