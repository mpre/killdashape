'''
Created on 10/dic/2010

@author: tosh
'''

try:
    import elements
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
    print "cazzo non ha importato bene in weapons"

class base_weapon(pygame.sprite.Sprite):
    """Arma basilare che spara un proiettile alla volta in una direzione"""
    def __init__(self, d_vector, firing_key=K_d, bullet_speed=1, father=None):
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
            x = elements.bullet(((random.randint(1,255)),
                                 (random.randint(1,255)),
                                 (random.randint(1,255))),
                                 (self.father.rect.center),
                                 self.direction) 
            snd_master.play('shoot')
            bullets.add(x)
        else:
            self.cooldown -= 1
        
    def set_father(self, father):
        self.father = father
                
class triple_directed_weapon(base_weapon):
    """Arma che spara tre proiettili alla volta, in una sola direzione"""
                
    def update(self):
        if not self.cooldown:
            self.cooldown = K_COOLDOWN
            x = elements.bullet(((random.randint(1,255)),
                                 (random.randint(1,255)),
                                 (random.randint(1,255))),
                                 (self.father.rect.topright),
                                 self.direction) 
            x = elements.bullet(((random.randint(1,255)),
                        (random.randint(1,255)),
                        (random.randint(1,255))),
                        ((self.father.rect.right, self.father.rect.centery)),
                         self.direction) 
            x = elements.bullet(((random.randint(1,255)),
                        (random.randint(1,255)),
                        (random.randint(1,255))),
                        (self.father.rect.bottomright),
                         self.direction) 
            snd_master.play('shoot')
            bullets.add(x)
        else:
            self.cooldown -= 1
        
class fan_weapon(base_weapon):
    
    def update(self):
        if not self.cooldown:
            self.cooldown = K_COOLDOWN
            x = elements.bullet(((random.randint(1,255)),
                        (random.randint(1,255)),
                        (random.randint(1,255))),
                        (self.father.rect.topright),
                         self.direction) 
            x = elements.bullet(((random.randint(1,255)),
                        (random.randint(1,255)),
                        (random.randint(1,255))),
                        ((self.father.rect.right, self.father.rect.centery)),
                         self.direction) 
            x = elements.bullet(((random.randint(1,255)),
                        (random.randint(1,255)),
                        (random.randint(1,255))),
                        (self.father.rect.bottomright),
                         self.direction) 
            x = elements.bullet(((random.randint(1,255)),
                        (random.randint(1,255)),
                        (random.randint(1,255))),
                        (self.father.rect.center),
                         (3,1), 0.5)
            x = elements.bullet(((random.randint(1,255)),
                        (random.randint(1,255)),
                        (random.randint(1,255))),
                        (self.father.rect.center),
                         (2,1), 0.7)
            x = elements.bullet(((random.randint(1,255)),
                        (random.randint(1,255)),
                        (random.randint(1,255))),
                        (self.father.rect.center),
                         (3,-1), 0.5) 
            x = elements.bullet(((random.randint(1,255)),
                        (random.randint(1,255)),
                        (random.randint(1,255))),
                        (self.father.rect.center),
                         (2,-1), 0.7)
            snd_master.play('shoot')           
            bullets.add(x)
        else:
            self.cooldown -= 1

class h_weapon(base_weapon):
    def update(self):
        if not self.cooldown:
            self.cooldown = K_COOLDOWN * 3
            x = elements.bullet(((random.randint(1,255)),
                        (random.randint(1,255)),
                        (random.randint(1,255))),
                        (self.father.rect.center),
                         self.direction,
                         0.5,
                         (5,15)) 
            snd_master.play('shoot')
            bullets.add(x)
        else:
            self.cooldown -= 1