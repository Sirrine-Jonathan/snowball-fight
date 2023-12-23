# Example file showing a circle moving on screen
import pygame
import random
import math
import random


# pygame setup
pygame.init()
pygame.display.set_caption('Snowball Fight')
screen = pygame.display.set_mode((900, 506))
clock = pygame.time.Clock()
running = True
dt = 0
isGameOver = False


pygame.font.init()
gameOverFont = pygame.font.SysFont('Comic Sans MS', 30)
otherFont = pygame.font.SysFont('Comic Sans MS', 20)
gameOverText = gameOverFont.render('Game Over', False, (0, 0, 0))
winnerText = otherFont.render('You Win', False, (0, 0, 0))
loserText = otherFont.render('You Lose', False, (0, 0, 0))

class Object:
    vel = 100
    x_min = 0
    x_max = screen.get_width()
    y_min = 0
    y_max = screen.get_height()

    def __init__(self, color = 'yellow', size = 15):
        self.color = color
        self.size = size;
        if (color == 'red'):
            self.pos = self.random_left()
            self.x_max = screen.get_width() / 2
        elif (color == 'blue'):
            self.pos = self.random_right()
            self.x_min = screen.get_width() / 2
        else:
            self.pos = self.random_position()

    def draw(self):
        pygame.draw.circle(screen, self.color, self.pos, self.size)

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
            return random.uniform(0 + (self.size / 2), (screen.get_width() / 2) - (self.size / 2))
        elif (place == 'right'):
            return random.uniform((screen.get_width() / 2) + (self.size / 2), screen.get_width() - (self.size / 2))
        else:
            return random.uniform(0 + (self.size / 2), screen.get_width() - (self.size / 2))

    def random_y(self):
        return random.uniform(0 + (self.size / 2), screen.get_height() - (self.size / 2))

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

class healthBar():
    width = 40
    height = 5

    def draw(self, pos, yOffset, percent):
        pygame.draw.rect(screen, 'red', pygame.Rect(pos.x - (self.width / 2), pos.y - (yOffset + 10), self.width, self.height))
        pygame.draw.rect(screen, 'green', pygame.Rect(pos.x - (self.width / 2), pos.y - (yOffset + 10), self.width * (percent / 100), self.height))

class powerBar():
    width = 40
    height = 5

    def draw(self, pos, yOffset, percent):
        pygame.draw.rect(screen, 'black', pygame.Rect(pos.x - (self.width / 2), pos.y - (yOffset + self.height + 10), self.width, self.height))
        pygame.draw.rect(screen, 'blue', pygame.Rect(pos.x - (self.width / 2), pos.y - (yOffset + self.height + 10), self.width * (percent / 100), self.height))


redSnowballs = []
blueSnowballs = []


def isHit(obj1, obj2):
    dist = math.hypot(obj1.pos.x - obj2.pos.x, obj1.pos.y - obj2.pos.y)
    return dist <= (obj1.size) + (obj2.size)

class Snowball(Object):
    damage = 10
    gravity = 1
    speed_hor = 10
    speed_ver = 7
    isDead = False
    isEnemy = 'enemy'
    plot = []
    size = 8
    color = 'white'

    def __init__(self, x, y, vel, dieY = False, isRed = False):
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
        pygame.draw.circle(screen, self.color, self.pos, self.size)

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
            pygame.draw.circle(screen, 'grey', pos, self.size / 2)



class Person(Object):
    vel = 75
    health = 100
    charge = 0
    healthBar = healthBar()
    powerBar = powerBar()
    isDead = False
    isCharging = False
    check_count = 0
    initial_max_check = random.randrange(70, 90)
    max_check = initial_max_check
    throw_check = random.randrange(30, 90, 10)

    def __init__(self, color = 'red', size = 15):
        super().__init__(color, size)
        self.x_left = bool(random.getrandbits(1))
        self.y_up = bool(random.getrandbits(1))
        self.x_moving = bool(random.getrandbits(1))
        self.y_moving = bool(random.getrandbits(1))

    def draw(self):
        super().draw()
        self.healthBar.draw(self.pos, self.size, self.health)
        self.powerBar.draw(self.pos, self.size, self.charge)
        if (self.color == 'blue' and self.isCharging):
            snowball = self.makeSnowball()
            snowball.drawPlot()

    def hit(self, damage):
        self.health -= damage
        if (self.health <= 0):
            self.isDead = True

    def throw(self):
        if (self.color == 'red'):
            redSnowballs.append(self.makeSnowball())
        else:
            blueSnowballs.append(self.makeSnowball())
        self.charge = 1

    def makeSnowball(self):
        x = self.pos.x
        y = self.pos.y - (self.size / 2)
        charge = self.charge / 10
        yDie = self.pos.y + (self.size / 2)
        isRed = self.color == 'red'
        if (not isRed):
            x += self.size
        return Snowball(x, y, charge, yDie, isRed)

    def chargeThrow(self, chargeAmount):
        self.charge += chargeAmount
        if self.charge > 100:
            self.charge = 100

    def moveUp(self, dt):
        return self.move(0, -1, dt)

    def moveDown(self, dt):
        return self.move(0, 1, dt)

    def moveLeft(self, dt):
        return self.move(-1, 0, dt)

    def moveRight(self, dt):
        return self.move(1, 0, dt)

    def auto(self, dt):
        self.check_count += 1
        if (self.check_count > self.max_check):
            self.check_count = 0
            self.x_moving = bool(random.getrandbits(1))
            self.y_moving = bool(random.getrandbits(1))
            self.x_left = bool(random.getrandbits(1))
            self.y_up = bool(random.getrandbits(1))
        if (self.x_moving):
            if self.x_left:
                if self.moveLeft(dt):
                    self.x_left = not self.x_left
            else:
                if self.moveRight(dt):
                    self.x_left = not self.x_left
        if (self.y_moving):
            if (self.y_up):
                if self.moveUp(dt):
                    self.y_up = not self.y_up
            else:
                if self.moveDown(dt):
                    self.y_up = not self.y_up
        if (self.x_moving or self.y_moving):
            self.max_check = self.initial_max_check
        else:
            self.max_check = random.randrange(30, 80)
        if (bool(random.getrandbits(1))):
            self.chargeThrow(1)
        if (self.check_count % 50 == 0 and random.getrandbits(1)):
            self.throw()



redTeam = [Person('red'), Person('red'), Person('red'), Person('red'), Person('red'), Person('red')]
blueTeam = [Person('blue')]
playerIndex = 0;

while running:

    if 0 > playerIndex >= len(blueTeam):
        playerIndex = 0

    if not isGameOver:
        dude = blueTeam[playerIndex]

    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYUP:
            if (event.key == pygame.K_LCTRL):
                playerIndex += 1
                if (playerIndex >= len(blueTeam)):
                    playerIndex = 0

        if not isGameOver and event.type == pygame.MOUSEBUTTONUP or (event.type == pygame.KEYUP and event.key == pygame.K_SPACE):
            mouse_pos = pygame.mouse.get_pos()
            curr_guy = blueTeam[playerIndex]
            dude = blueTeam[playerIndex]
            dude.throw()

    m_left, _, _ = pygame.mouse.get_pressed()
    keys = pygame.key.get_pressed()

    if not isGameOver:
        if m_left or keys[pygame.K_SPACE]:
            dude.isCharging = True
            dude.chargeThrow(1)
        else:
            dude.isCharging = False

    for ball in blueSnowballs:
        ball.move()

    for ball in redSnowballs:
        ball.move()

    if (not isGameOver):
        for person in redTeam:
            person.auto(dt)

    if not isGameOver:
        for index, person in enumerate(blueTeam):
            if (index != playerIndex):
                person.auto(dt)

    for ball in redSnowballs:
        for person in blueTeam:
            if (isHit(person, ball)):
                person.hit(ball.damage)
                ball.isDead = True

    for ball in blueSnowballs:
        for person in redTeam:
            if (isHit(person, ball)):
                person.hit(ball.damage)
                ball.isDead = True

    redSnowballs = list(filter(lambda x: not x.isDead, redSnowballs))
    blueSnowballs = list(filter(lambda x: not x.isDead, blueSnowballs))
    redTeam = list(filter(lambda x: not x.isDead, redTeam))
    blueTeam = list(filter(lambda x: not x.isDead, blueTeam))

    if len(blueTeam) == 0:
        isGameOver = True
        isWinner = False

    if len(redTeam) == 0:
        isGameOver = True
        isWinner = True

    if 0 > playerIndex >= len(blueTeam):
        playerIndex = 0

    if not isGameOver and len(blueTeam) > 0:
        keys = pygame.key.get_pressed()
        dude = blueTeam[playerIndex]
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            dude.moveUp(dt)
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            dude.moveDown(dt)
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            dude.moveLeft(dt)
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            dude.moveRight(dt)

    screen.fill("purple")

    for ball in blueSnowballs:
        ball.draw()

    for ball in redSnowballs:
        ball.draw()

    for person in redTeam:
        person.draw()

    for index, person in enumerate(blueTeam):
        if (index == playerIndex):
            pygame.draw.circle(screen, 'black', person.pos, person.size + 2)
        person.draw()

    if (isGameOver):
        screen.fill("purple")

        screen.blit(gameOverText, (0,0))
        if (isWinner):
            screen.blit(winnerText, (0, 40))
        else:
            screen.blit(loserText, (0, 40))


    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000

pygame.quit()