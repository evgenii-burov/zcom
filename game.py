import pygame
from config import *
from core.state import State
from core.turn_manager import TurnManager
from core.placeables import  Placeable
from core.ui import UI
from objects.cursor import Cursor
from objects.base import GameObject
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
        self.placeables = [x for x in Placeable]
        self.current_placeable = 0
        self.ui = UI()

        self.turn_manager = TurnManager()

    def delete_object(self, position: GridPoint):
        self.grid.get_tile(position).obj = None
        i = next(i for i, obj in enumerate(self.objects) if obj.position == position)
        self.objects.pop(i)

    def add_object(self, obj: GameObject):
        if self.grid.get_tile(obj.position.grid_point()).occupied:
            self.ui.log_message("Tile is occupied", True, 3, MSG_RED)
            return
        self.grid.place_object(obj)
        self.objects.append(obj)

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
            # Space for placing
            if event.key == pygame.K_SPACE:
                obj = self.placeables[self.current_placeable].get_instance(self.cursor.position)
                if obj is None:
                    if self.grid.get_tile(self.cursor.position).occupied:
                        self.delete_object(self.cursor.position)
                        return
                    else:
                        return
                if self.grid.get_tile(obj.position).occupied:
                    self.delete_object(obj.position)
                self.add_object(obj)
                self.ui.log_message(f"Placed {obj.__str__()}", True, 3, MSG_GREEN)
                return


            # Tab for placeable switching
            if event.key == pygame.K_TAB:
                self.current_placeable = (self.current_placeable + 1) % len(self.placeables)
                return
            # Cursor movement
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
        for obj in self.objects:
            obj.draw(self.screen)
        # cursor
        if not self.cursor.hidden:
            self.cursor.draw(self.screen)
        # ui
        self.ui.draw(self.screen, self.state, self.cursor, self.grid, self.placeables[self.current_placeable])

        