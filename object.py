import pygame
import random

class Object:
    vel = 100
    x_min = 0
    y_min = 0

    def __init__(self, surface, color = 'yellow', size = 15):
        self.surface = surface
        self.color = color
        self.size = size
        self.x_max = self.surface.get_width()
        self.y_max = self.surface.get_height()

        if (color == 'red'):
            self.pos = self.random_left()
            self.x_max = self.surface.get_width() / 2
        elif (color == 'blue'):
            self.pos = self.random_right()
            self.x_min = self.surface.get_width() / 2
        else:
            self.pos = self.random_position()

    def draw(self):
        pygame.draw.circle(self.surface, self.color, self.pos, self.size)

    def move(self, x, y, dt):
        self.pos.x += x * self.vel * dt
        self.pos.y += y * self.vel * dt
        return self.adjust_pos()

    def random_position(self):
        return pygame.Vector2(self.random_x(), self.random_y())

    def random_left(self):
        return pygame.Vector2(self.random_x('left'), self.random_y())

    def random_right(self):
        return pygame.Vector2(self.random_x('right'), self.random_y())

    def random_x(self, place):
        if (place == 'left'):
            return random.uniform(0 + (self.size / 2), (self.surface.get_width() / 2) - (self.size / 2))
        elif (place == 'right'):
            return random.uniform((self.surface.get_width() / 2) + (self.size / 2), self.surface.get_width() - (self.size / 2))
        else:
            return random.uniform(0 + (self.size / 2), self.surface.get_width() - (self.size / 2))

    def random_y(self):
        return random.uniform(0 + (self.size / 2), self.surface.get_height() - (self.size / 2))

    def adjust_pos(self):
        adjusted = False
        if self.pos.x < self.x_min + self.size:
            self.pos.x = self.x_min + self.size
            adjusted = True
        if self.pos.x > self.x_max - self.size:
            self.pos.x = self.x_max - self.size
            adjusted = True
        if self.pos.y < self.y_min + self.size:
            self.pos.y = self.y_min + self.size
            adjusted = True
        if self.pos.y > self.y_max - self.size:
            self.pos.y = self.y_max - self.size
            adjusted = True
        return adjusted