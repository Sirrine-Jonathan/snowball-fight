import pygame

class HealthBar():
    width = 40
    height = 5

    def __init__(self, surface):
        self.surface = surface

    def draw(self, pos, yOffset, percent):
        pygame.draw.rect(self.surface, 'red', pygame.Rect(pos.x - (self.width / 2), pos.y - (yOffset + 30), self.width, self.height))
        pygame.draw.rect(self.surface, 'green', pygame.Rect(pos.x - (self.width / 2), pos.y - (yOffset + 30), self.width * (percent / 100), self.height))
