import pygame
from map.types import GridPoint, PixelPoint, center
from config import *
import math

class Projectile:
    def __init__(self, start_tile: GridPoint, end_tile: GridPoint,
                 velocity: float = PROJECTILE_VELOCITY):   # пикселей в секунду
        self.start_tile = start_tile
        self.end_tile = end_tile
        self.velocity = velocity
        self.color = PROJECTILE_COLOR

        sx, sy = center(start_tile)
        ex, ey = center(end_tile)
        self.start_pos = (float(sx), float(sy))
        self.end_pos = (float(ex), float(ey))

        vx, vy = ex - sx, ey - sy
        self.total_distance = math.hypot(vx, vy)
        # единичный вектор направления (если старт == цель, расстояние 0)
        if self.total_distance > 0:
            self.direction = (vx / self.total_distance, vy / self.total_distance)
        else:
            self.direction = (0.0, 0.0)

        self.travelled = 0.0
        self.position: tuple[float, float] = self.start_pos
        self.render_position: PixelPoint = (int(sx), int(sy))
        self.reached_target = self.total_distance == 0

    def update(self, dt: float):
        """dt в секундах."""
        if self.reached_target:
            return
        self.travelled += self.velocity * dt
        if self.travelled >= self.total_distance:
            self.travelled = self.total_distance
            self.reached_target = True
        self.position = (self.start_pos[0] + self.direction[0] * self.travelled,
                         self.start_pos[1] + self.direction[1] * self.travelled)
        self.render_position = (round(self.position[0]), round(self.position[1]))
            
    def render(self, surface: pygame.Surface):
        pygame.draw.circle(surface, self.color, self.render_position, PROJECTILE_SIZE)