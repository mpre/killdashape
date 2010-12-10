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
    from game_master import *
except:
    print "cazzo non ha importato bene pappa"

class bullet(pygame.sprite.Sprite):
    """Single bullet class"""
    def __init__(self, color, initial_pos, vector, speed=1, bullet_dimension=K_BULLET_DIMENSION):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface(bullet_dimension)
        # Ruoto l'immagine in modo che sia concorde
        # al vettore direzione
        alpha = math.degrees(angle(vector, (1,0)))
        self.image = pygame.transform.rotate(self.image, alpha) 
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.center = initial_pos
        self.vector = vector
        self.speed = speed
        bullets.add(self)
        
    def update(self):
        offset_x = self.vector[0] * K_BULLET_SPEED * self.speed
        offset_y = self.vector[1] * K_BULLET_SPEED 
        self.rect = self.rect.move(offset_x, offset_y)
        if self.rect[0] > K_WINDOW_DIM[0] or self.rect[0] < 0 or self.rect[1] > K_WINDOW_DIM[1] or self.rect[1] < 0 :
            self.kill()
         
    def kill(self):
        if self in bullets:
            bullets.remove(self)
        else:
            en_bullets.remove(self)
        self = None

class box(pygame.sprite.Sprite):
    """Superclasse di personaggio e nemico"""
    def __init__(self, color, initial_pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface(K_BOX_DIMENSION)
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.center = initial_pos

class player_box(box):
    """L'utente"""
    def __init__(self, color, initial_pos):
        box.__init__(self, color, initial_pos)
        self.direction = [False for _ in range(4)]
        self.weapons = []
        self.color = color
        self.hp = K_HP
    
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
            if not self.rect.bottom >= K_WINDOW_DIM[1] - K_MOV:
                self.rect = self.rect.move(0, K_MOV)
        if self.direction[M_NORTH]:
            if not self.rect.top <= K_MOV:
                self.rect = self.rect.move(0, -K_MOV)
        if self.direction[M_WEST]:
            if not self.rect.left <= K_MOV:
                self.rect = self.rect.move(-K_MOV, 0)
        if self.direction[M_EAST]:
            if not self.rect.right >= K_WINDOW_DIM[0] - K_MOV:
                self.rect = self.rect.move(K_MOV, 0)
        if active_weapons:
            active_weapons[0].update()              
        
    def kill(self):
        self.hp -= 1
        snd_master.play('enemy_explosion')
        if self.hp == 0:
            create_explosion_at(self.color, self.rect)
    
    def add_weapons(self, weapons=None):
        if weapons.__class__.__name__ == 'list':
            for weapon in weapons:
                self.add_weapon(weapon)
        else:
            self.add_weapon(weapons)
            
    def add_weapon(self, weapon):
        weapon.set_father(self)
        self.weapons.append(weapon)
        
    def clear_weapons(self):
        self.weapons = []
        
    def hit_point(self):
        return self.hp
        
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
    

    
