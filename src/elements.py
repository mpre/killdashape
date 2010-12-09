'''
Created on 08/dic/2010

@author: tosh
'''
try:
    import pygame
    from pygame.locals import *
    import random
    import math
    from killdashape_k import *
    from global_vars import *
    from useful_lib import *
    from sound_master import *
except:
    print "cazzo non ha importato bene pappa"

class bullet(pygame.sprite.Sprite):
    """Single bullet class"""
    def __init__(self, color, initial_pos, vector):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface(K_BULLET_DIMENSION)
        # Ruoto l'immagine in modo che sia concorde
        # al vettore direzione
        alpha = math.degrees(angle(vector, (1,0)))
        self.image = pygame.transform.rotate(self.image, alpha) 
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.center = initial_pos
        self.vector = vector
        bullets.add(self)
        
    def update(self):
        offset_x = self.vector[0] * K_LEVEL
        offset_y = self.vector[1] * K_LEVEL 
        self.rect = self.rect.move(offset_x, offset_y)
        if self.rect[0] > K_WINDOW_DIM[0] or self.rect[0] < 0 or self.rect[1] > K_WINDOW_DIM[1] or self.rect[1] < 0 :
            self.kill()
         
    def kill(self):
        bullets.remove(self)
        self = None
            
class box(pygame.sprite.Sprite):
    """Superclasse di personaggio e nemico"""
    def __init__(self, color, initial_pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface(K_BOX_DIMENSION)
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.topleft = initial_pos

class enemy_box(box):
    """I nemici quadrati"""
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
        snd_master.play('enemy_explosion')
        enemies.remove(self)
        for vector in ((1,0), (1,1), (0,1), (-1,1), (-1,0), (-1,-1), (0,-1), (1, -1)):
                e = enemy_junkie(self.color, self.rect.center, vector)
                junkie.add(e)
        self = None
        
class player_box(box):
    """L'utente"""
    def __init__(self, color, initial_pos):
        box.__init__(self, color, initial_pos)
        self.direction = [False for _ in range(4)]
        self.weapons = []

    
    def give(self, event=None, rest=None):
        if event.type == KEYDOWN:
            if event.key == K_DOWN:
                self.direction[M_SOUTH] = True
            elif event.key == K_UP:
                self.direction[M_NORTH] = True
            elif event.key == K_LEFT:
                self.direction[M_WEST] = True
            elif event.key == K_RIGHT:
                self.direction[M_EAST] = True
            else:
                for weapon in self.weapons:
                    weapon.give(event)
                
        elif event.type == KEYUP:
            if event.key == K_DOWN:
                self.direction[M_SOUTH] = False
            elif event.key == K_UP:
                self.direction[M_NORTH] = False
            elif event.key == K_LEFT:
                self.direction[M_WEST] = False
            elif event.key == K_RIGHT:
                self.direction[M_EAST] = False
            else:
                for weapon in self.weapons:
                    weapon.give(event)
                
    def update(self):
        if self.direction[M_SOUTH]:
            self.rect = self.rect.move(0, K_MOV)
        if self.direction[M_NORTH]:
            self.rect = self.rect.move(0, -K_MOV)
        if self.direction[M_WEST]:
            self.rect = self.rect.move(-K_MOV, 0)
        if self.direction[M_EAST]:
            self.rect = self.rect.move(K_MOV, 0)
        if active_weapons:
            active_weapons[0].update()              
        
    def die(self):
        pass
    
    def add_weapons(self, weapons=None):
        for weapon in weapons:
            weapon.set_father(self)
            self.weapons.append(weapon)
            
    def add_weapon(self, weapon):
        weapon.set_father(self)
        self.weapons.append(weapon)

class enemy_junkie(pygame.sprite.Sprite):
    """Gli scarti generati dalla morte dei nemici"""
    def __init__(self, color, init_pos, vector):
        pygame.sprite.Sprite.__init__(self) 
        self.image = pygame.Surface(K_JUNK_DIMENSION)
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.center = init_pos
        self.init_pos = init_pos
        self.vector = vector
        self.times = 0
        
    def update(self):
        offset_x = self.vector[0] * K_JUNK_MOV / math.sqrt(( self.vector[0]**2 + self.vector[1]**2))
        offset_y = self.vector[1] * K_JUNK_MOV / math.sqrt(( self.vector[0]**2 + self.vector[1]**2))
        self.rect = self.rect.move(offset_x, offset_y)
        self.times += 1
        if self.times * K_JUNK_MOV >= K_JUNKIE_RADIUS:
            self.kill()
        
    def kill(self):
        junkie.remove(self)
        self = None
           
class base_weapon(pygame.sprite.Sprite):
    """Arma basilare che spara un proiettile alla volta in una direzione"""
    def __init__(self, d_vector, firing_key=K_LCTRL, father=None):
        pygame.sprite.Sprite.__init__(self)
        self.cooldown = 0
        self.key = firing_key
        self.direction = d_vector
        self.father = father
        
    def give(self, event, *rest):
        if event.type == KEYDOWN:
            if event.key == self.key:
                active_weapons.append(self)
        elif event.type == KEYUP:
            if event.key == self.key:
                active_weapons.remove(self)
                self.cooldown = 0
                
    def update(self):
        if not self.cooldown:
            self.cooldown = K_COOLDOWN
            x = bullet(((random.randint(1,255)),
                        (random.randint(1,255)),
                        (random.randint(1,255))),
                        (self.father.rect.center),
                         self.direction) 
            bullets.add(x)
        else:
            self.cooldown -= 1
        
    def set_father(self, father):
        self.father = father
                
class triple_directed_weapon(pygame.sprite.Sprite):
    """Arma che spara tre proiettili alla volta, in una sola direzione"""
    def __init__(self, direction, firing_key=K_LCTRL, father=None):
        pygame.sprite.Sprite.__init__(self)
        self.cooldown = 0
        self.key = firing_key
        self.father = father
        self.direction = direction
        
    def give(self, event, *rest):
        if event.type == KEYDOWN:
            if event.key == self.key:
                active_weapons.append(self)
        elif event.type == KEYUP:
            if event.key == self.key:
                active_weapons.remove(self)
                self.cooldown = 0
                
    def update(self):
        if not self.cooldown:
            self.cooldown = K_COOLDOWN
            x = bullet(((random.randint(1,255)),
                        (random.randint(1,255)),
                        (random.randint(1,255))),
                        (self.father.rect.topright),
                         self.direction) 
            x = bullet(((random.randint(1,255)),
                        (random.randint(1,255)),
                        (random.randint(1,255))),
                        ((self.father.rect.right, self.father.rect.centery)),
                         self.direction) 
            x = bullet(((random.randint(1,255)),
                        (random.randint(1,255)),
                        (random.randint(1,255))),
                        (self.father.rect.bottomright),
                         self.direction) 
            snd_master.play('shoot')
            bullets.add(x)
        else:
            self.cooldown -= 1
            
    def set_father(self, father):
        self.father = father