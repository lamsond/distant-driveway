import pygame, sys, math, random

#game constants
FPS = 60
WIN_WIDTH = 1080
WIN_HEIGHT = 720
TANK_WIDTH = 50
TANK_LENGTH = 75
TANK_SPEED = 3
TIRE_DIAMETER = 40
TIRE_WIDTH = 20
TANK_RAD = 22
GUN_LENGTH = 60
GUN_WIDTH = 8
DEBUG = False

#game colors
JUNGLE = (5, 69, 6)
RED_MUD = (69, 5, 5)
MUD = (69, 37, 5)
NEPTUNE = (5, 5, 69)
JUICE = (69, 5, 68)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (103, 103, 103)
GRASS = (26, 97, 27)
RED = (255, 0, 0)
ORANGE = (255, 166, 0)
YELLOW = (255, 255, 0)

#game variables
explosion_frame = 0
nMines = 10
nCoins = 20
mines = []
coins = []
closest_mine = WIN_WIDTH + WIN_HEIGHT
points = 0
distance_color = JUICE

#init
pygame.init()
screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption("Distance Demo")
clock = pygame.time.Clock()
fnt = pygame.font.Font("freesansbold.ttf", 48)
sm_fnt = pygame.font.Font("freesansbold.ttf", 14)

#game functions
def distance(a, b):
    diff_x =  b[0] - a[0]
    diff_y = b[-1] - a[-1]
    sq_x = diff_x ** 2
    sq_y = diff_y ** 2
    sum_sq = sq_x + sq_y
    d = math.sqrt(sum_sq)
    return d

def draw_tire(x, y, direction):
    if direction == "NORTH" or direction == "SOUTH":
        pygame.draw.rect(screen, BLACK, 
        (x, y, TIRE_WIDTH, TIRE_DIAMETER))
    else:
        pygame.draw.rect(screen, BLACK,
        (x, y, TIRE_DIAMETER, TIRE_WIDTH))
        
def update_tires(center_point):
    x = center_point[0]-int(TIRE_WIDTH/2)
    y = center_point[1]-int(TIRE_DIAMETER/2)
    x_step = int(TANK_WIDTH/2)
    y_step = int(TANK_LENGTH/2)
    tires = [
    [x-x_step, y-y_step], 
    [x+x_step, y-y_step], 
    [x+x_step, y+y_step], 
    [x-x_step, y+y_step]
    ]
    return tires
        
#game classes
class Tank():
    
    def __init__(self, x, y):
        self.pos = [x, y]
        self.alive = True
        self.tires = update_tires(self.pos)
        
    def draw(self):
        for tire in self.tires:
            draw_tire(tire[0], tire[1], "NORTH")
            
        pygame.draw.rect(screen, BLACK,
        (self.pos[0]-int(TANK_WIDTH/2), self.pos[1]-int(TANK_LENGTH/2), 
        TANK_WIDTH, TANK_LENGTH), 2)
        pygame.draw.rect(screen, JUNGLE,
        (self.pos[0]-int(TANK_WIDTH/2), self.pos[1]-int(TANK_LENGTH/2), 
        TANK_WIDTH, TANK_LENGTH))
        
        pygame.draw.rect(screen, JUNGLE, (self.pos[0]-TANK_RAD, self.pos[1]-TANK_RAD, 2*TANK_RAD, 2*TANK_RAD))
        pygame.draw.rect(screen, BLACK, (self.pos[0]-TANK_RAD, self.pos[1]-TANK_RAD, 2*TANK_RAD, 2*TANK_RAD), 2)
        
        pygame.draw.rect(screen, GRAY,
        (self.pos[0]-int(GUN_WIDTH/2), self.pos[1]-GUN_LENGTH, GUN_WIDTH, GUN_LENGTH))
        pygame.draw.rect(screen, BLACK,
        (self.pos[0]-int(GUN_WIDTH/2), self.pos[1]-GUN_LENGTH, GUN_WIDTH, GUN_LENGTH), 2)
    
    def move(self, direction):
        if direction == "UP":
            self.pos[1] -= TANK_SPEED
        elif direction == "DOWN":
            self.pos[1] += TANK_SPEED
        elif direction == "LEFT":
            self.pos[0] -= TANK_SPEED
        else:
            self.pos[0] += TANK_SPEED
        self.tires = update_tires(self.pos)
    
    def explode(self, frame):
        if frame < 100:
            pygame.draw.circle(screen, RED, self.pos, frame*3)
            pygame.draw.circle(screen, ORANGE, self.pos, int(frame*2.5))
            pygame.draw.circle(screen, YELLOW, self.pos, frame*2)
        elif frame < 150:
            pygame.draw.circle(screen, (150-frame, 150-frame, 150-frame), self.pos, (150-frame)*2)

class Mine():
    def __init__(self, x, y, rad):
        self.pos = [x, y]
        self.rad = rad
    
    def draw(self):
        pygame.draw.circle(screen, JUICE, self.pos, self.rad)

class Coin():
    def __init__(self, x, y, screen):
        self.pos = [x, y]
        self.rad = 15
        self.value = random.randint(1, 100)
        self.screen = screen

    def draw(self):
        pygame.draw.circle(screen, YELLOW, self.pos, self.rad)
        pygame.draw.circle(screen, BLACK, self.pos, self.rad+1, 3)
        txt = sm_fnt.render(str(self.value), True, JUICE)
        txt_rect = txt.get_rect()
        txt_rect.center = self.pos
        screen.blit(txt, txt_rect)

tank = Tank(300, 300)
for i in range(nMines):
    mines.append(Mine(random.randint(0, WIN_WIDTH), random.randint(0, WIN_HEIGHT), 10))
for i in range(nCoins):
	coins.append(Coin(random.randint(0, WIN_WIDTH), random.randint(0, WIN_HEIGHT), screen))
  
#game loop
while True:
    #animate
    if closest_mine < 50:
       screen.fill(RED_MUD)
       distance_color = WHITE
    else:
        screen.fill(GRASS)
        distance_color = JUICE
    if tank.alive:
        if DEBUG:
            for mine in mines:
                mine.draw()
        for coin in coins:
            coin.draw()
        tank.draw()
    else:
        explosion_frame += 1
        tank.explode(explosion_frame)
    
    #event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    keys = pygame.key.get_pressed()
    if tank.alive:
        if keys[pygame.K_RIGHT]:
            tank.move("RIGHT")
        elif keys[pygame.K_LEFT]:
            tank.move("LEFT")
        elif keys[pygame.K_UP]:
            tank.move("UP")
        elif keys[pygame.K_DOWN]:
            tank.move("DOWN")
    
    #check for explosion
    closest_mine = WIN_WIDTH + WIN_HEIGHT
    for tire in tank.tires:
        tire_mid = [tire[0] + int(TIRE_WIDTH/2), tire[1] + int(TIRE_DIAMETER/2)]
        for mine in mines:
            d = distance(tire_mid, mine.pos)
            if d < mine.rad:
                tank.alive = False
                break
            elif d < closest_mine:
                closest_mine = d
        for coin in coins:
            d = distance(tire_mid, coin.pos)
            if d < coin.rad:
                points += coin.value
                coins.remove(coin)

    if tank.alive:         
        txt = fnt.render(str(round(closest_mine, 1)), True, distance_color)
        txt_rect = txt.get_rect()
        txt_rect.center = (WIN_WIDTH - 100, 50)
        screen.blit(txt, txt_rect)
        
    txt = fnt.render(str(points), True, YELLOW)
    txt_rect = txt.get_rect()
    txt_rect.center = (100, 50)
    screen.blit(txt, txt_rect)
    
    #update screen and clock
    pygame.display.update()
    clock.tick(FPS)
