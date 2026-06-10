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
                self._handle_placing(event)

    def _handle_placing(self, event):
        if event.type == pygame.KEYDOWN:
            direction = Direction.NULL
            distance = 0
            mods = pygame.key.get_mods()
            if mods & pygame.KMOD_CTRL:
                distance = 5
            else:
                distance = 1
            if event.key == pygame.K_LEFT:
                direction = Direction.LEFT
            elif event.key == pygame.K_RIGHT:
                direction = Direction.RIGHT
            elif event.key == pygame.K_UP:
                direction = Direction.UP
            elif event.key == pygame.K_DOWN:
                direction = Direction.DOWN
            self.cursor.move(direction, distance)

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

        