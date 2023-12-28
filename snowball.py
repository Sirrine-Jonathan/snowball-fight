import pygame

class SnowBall():
    damage = 10
    gravity = 1
    speed_hor = 10
    speed_ver = 7
    isDead = False
    isEnemy = 'enemy'
    plot = []
    size = 8
    color = 'white'

    def __init__(self, surface, x, y, vel, dieY = False, isRed = False):
        self.surface = surface
        self.pos = pygame.Vector2(x, y)
        self.start_pos = pygame.Vector2(x + 1, y)
        self.speed_hor = self.speed_hor + vel
        self.speed_ver = self.speed_hor + (vel / 2)
        self.isRed = isRed
        if dieY == False:
            self.dieY = self.start_pos.y
        else:
            self.dieY = dieY

    def draw(self):
        pygame.draw.circle(self.surface, self.color, self.pos, self.size)

    def move(self):
        if (self.isRed):
            self.pos.x += self.speed_hor
        else:
            self.pos.x -= self.speed_hor
        self.pos.y -= self.speed_ver
        self.speed_ver -= self.gravity
        self.plot.append(pygame.Vector2(self.pos.x, self.pos.y))
        if (self.speed_ver > 14):
            self.damage += 5;
        elif (self.speed_ver > 15):
            self.damage += 20;
        if (self.pos.y > self.dieY):
            self.isDead = True
            return False
        else:
            return True

    def drawPlot(self):
        self.plot = []
        while (self.move()):
            pass
        for pos in self.plot:
            pygame.draw.circle(self.surface, 'grey', pos, self.size / 2)