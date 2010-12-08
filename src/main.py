'''
Created on 07/dic/2010

@author: tosh
'''

try:
    import pygame
    from pygame.locals import *
    import random
except:
    print "cazzo non ha importato bene"

# Costanti
M_NORTH = 0
M_WEST = 1
M_SOUTH = 2
M_EAST = 3
K_MOV = 15
K_ENEMY_MOV = 7
K_LEVEL = 3 # BULLET SPEED IN PIXEL
K_COOLDOWN = 5
K_BOX_DIMENSION = (15, 15)
K_BULLET_DIMENSION = [10,3]
K_JUNK_DIMENSION = (3,3)
K_WINDOW_DIM = (640,320)

enemies = pygame.sprite.RenderUpdates()
bullets = pygame.sprite.RenderUpdates()
junkie = pygame.sprite.RenderUpdates()

# -*- Class definition -*-

class bullet(pygame.sprite.Sprite):
    
    def __init__(self, color, initial_pos, direction):
        pygame.sprite.Sprite.__init__(self)
        if direction == M_NORTH or direction == M_SOUTH:
            self.image = pygame.Surface(K_BULLET_DIMENSION[::-1])
        else:
            self.image = pygame.Surface(K_BULLET_DIMENSION)
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.topleft = initial_pos
        self.direction = direction
        bullets.add(self)
        
    def update(self):
        if self.direction == M_SOUTH:
            self.rect = self.rect.move(0, K_LEVEL)
        if self.direction == M_NORTH:
            self.rect = self.rect.move(0, -K_LEVEL)
        if self.direction == M_WEST:
            self.rect = self.rect.move(-K_LEVEL, 0)
        if self.direction == M_EAST:
            self.rect = self.rect.move(K_LEVEL, 0)
        if self.rect[0] > K_WINDOW_DIM[0] or self.rect[0] < 0 or self.rect[1] > K_WINDOW_DIM[1] or self.rect[1] < 0 :
            self.kill()
            
    def kill(self):
        print bullets
        bullets.remove(self)
        print bullets
        self = None
            

class box(pygame.sprite.Sprite):
    
    def __init__(self, color, initial_pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface(K_BOX_DIMENSION)
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.topleft = initial_pos


class enemy_box(box):
    
    def __init__(self, color, initial_pos):
        box.__init__(self, color, initial_pos)
        self.color = color
        enemies.add(self)
    
    def update(self, event=None, rest=None):
        if random.randint(0,1):
            if random.randint(0,1):
                self.rect = self.rect.move(0, K_ENEMY_MOV)
            else:
                self.rect = self.rect.move(0, -K_ENEMY_MOV)
        else:
            if random.randint(0,1):
                self.rect = self.rect.move(K_ENEMY_MOV, 0)
            else:
                self.rect = self.rect.move(-K_ENEMY_MOV, 0)
#    
    def kill(self):
        print enemies
        enemies.remove(self)
        print enemies
        for vector in ([1,0], [0,1], [1,1], [-1,0], [0,-1], [-1,-1]):
                e = enemy_junkie(self.color, self.rect.center, vector, 1)
                junkie.add(e)
                e = enemy_junkie(self.color, self.rect.center, vector, -1)
                junkie.add(e)
        self = None
        

class player_box(box):
    
    def __init__(self, color, initial_pos):
        box.__init__(self, color, initial_pos)
        self.direction = [False for _ in range(4)]
        self.shooting = False
        self.cooldown = 0
    
    def update(self, event=None, rest=None):
        if event.type == KEYDOWN:
            if event.key == K_DOWN:
                self.direction[M_SOUTH] = True
            elif event.key == K_UP:
                self.direction[M_NORTH] = True
            elif event.key == K_LEFT:
                self.direction[M_WEST] = True
            elif event.key == K_RIGHT:
                self.direction[M_EAST] = True
            elif event.key == K_SPACE:
                self.shooting = True
                
        elif event.type == KEYUP:
            if event.key == K_DOWN:
                self.direction[M_SOUTH] = False
            elif event.key == K_UP:
                self.direction[M_NORTH] = False
            elif event.key == K_LEFT:
                self.direction[M_WEST] = False
            elif event.key == K_RIGHT:
                self.direction[M_EAST] = False
            elif event.key == K_SPACE:
                self.shooting = False
                
    def move(self):
        if self.direction[M_SOUTH]:
            self.rect = self.rect.move(0, K_MOV)
        if self.direction[M_NORTH]:
            self.rect = self.rect.move(0, -K_MOV)
        if self.direction[M_WEST]:
            self.rect = self.rect.move(-K_MOV, 0)
        if self.direction[M_EAST]:
            self.rect = self.rect.move(K_MOV, 0)
        if self.shooting:
            if not self.cooldown:
                self.cooldown = K_COOLDOWN
                for i in range(4):
                    x = bullet(((random.randint(1,255)),
                                (random.randint(1,255)),
                                (random.randint(1,255))),
                                (self.rect.center),
                                i)
                    bullets.add(x)
            else:
                self.cooldown -= 1                
        
    def die(self):
        pass

class enemy_junkie(pygame.sprite.Sprite):
    def __init__(self, color, init_pos, vector, direction):
        pygame.sprite.Sprite.__init__(self) 
        self.image = pygame.Surface(K_JUNK_DIMENSION)
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.center = init_pos
        self.init_pos = init_pos
        self.vector = vector
        self.direction = direction
        self.i = 0
        
    def update(self):
        offset_x = self.vector[0] * K_LEVEL 
        offset_y = self.vector[1] * K_LEVEL * self.direction
        self.rect = self.rect.move(offset_x, offset_y)
        self.i += 1
        if self.i >= 15:
            self.kill()
        
    def kill(self):
        junkie.remove(self)
        self = None
           

def main():
    pygame.init()    
    END = False
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode(K_WINDOW_DIM)
#    background = pygame.image.load("../img/background.png")
#    background = background.convert()
    background = pygame.Surface(K_WINDOW_DIM)
    b = player_box([255, 0, 0], [0, 0])
    for _ in range(15):
        en = enemy_box([random.randint(1,255),
                        random.randint(1,255),
                        random.randint(1,255)],                       
                       [random.randint(30,640 - K_BOX_DIMENSION[0]),
                        random.randint(30,320 - K_BOX_DIMENSION[1])])
        enemies.add(en)
    
    while not END:
        clock.tick(24)
        for e in pygame.event.get():
            if e.type == QUIT:
                END = True
            else:
                b.update(e)
        b.move()
        bullets.update()
        enemies.update()
        junkie.update()
        if pygame.sprite.spritecollide(b, enemies, 0, None) != []:
            b.die()
            END = True
        pygame.sprite.groupcollide(bullets, enemies, 1, 1)
        screen.blit(background, [0,0])
        screen.blit(b.image, b.rect)
        rectlist = bullets.draw(screen)
        pygame.display.update(rectlist)
        rectlist = enemies.draw(screen)
        pygame.display.update(rectlist)
        rectlist = junkie.draw(screen)
        pygame.display.update(rectlist)
        pygame.display.update()

if __name__ == '__main__':
    main()
        
    