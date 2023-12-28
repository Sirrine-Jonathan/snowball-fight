import pygame

class PowerBar():
    width = 40
    height = 5

    def __init__(self, surface):
        self.surface = surface

    def draw(self, pos, yOffset, percent):
        pygame.draw.rect(self.surface, 'black', pygame.Rect(pos.x - (self.width / 2), pos.y - (yOffset + self.height + 30), self.width, self.height))
        pygame.draw.rect(self.surface, 'blue', pygame.Rect(pos.x - (self.width / 2), pos.y - (yOffset + self.height + 30), self.width * (percent / 100), self.height))