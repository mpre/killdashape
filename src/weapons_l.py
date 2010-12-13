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
    import game_master
except:
    print "cazzo non ha importato bene in weapons"

class base_weapon(pygame.sprite.Sprite):
    """Arma basilare che spara un proiettile alla volta in una direzione"""
    def __init__(self, d_vector, firing_key=M_WEAPON_SHOOT[0], bullet_speed=1, 
                 active=False, father=None, nplayer=0):
        pygame.sprite.Sprite.__init__(self)
        self.cooldown = 0
        self.key = firing_key
        self.direction = d_vector
        self.father = father
        self.active = active
        self.ammo = -1
        self.name = 'James Bond from the HELL'
        
    def give(self, event, *rest):
        if event.type == KEYDOWN:
            if event.key in self.key:
                self.active = True
        elif event.type == KEYUP:
            if event.key in self.key:
                self.active = False
                self.cooldown = 0
                
    def update(self):
        if not self.cooldown:
            if self.active:
                self.cooldown = K_COOLDOWN
                x = elements.bullet(((random.randint(1,255)),
                                     (random.randint(1,255)),
                                     (random.randint(1,255))),
                                     (self.father.rect.center),
                                     self.direction, father=self.father) 
                snd_master.play('shoot')
                bullets.add(x)
        else:
            self.cooldown -= 1
        
    def set_father(self, father):
        self.father = father
        
    def set_key(self, keys):
        self.key = keys
        
    def kill(self):
        self = None
        
    def get_ammo(self):
        if self.ammo > -1:
            return str(self.ammo)
        else:
            return "Infinite"
        
    def get_name(self):
        return self.name
                
class triple_directed_weapon(base_weapon):
    """Arma che spara tre proiettili alla volta, in una sola direzione"""
                
    def __init__(self, d_vector, firing_key=M_WEAPON_SHOOT[0], bullet_speed=1, 
                 active=False, father=None, nplayer=0):
        base_weapon.__init__(self, d_vector, firing_key, bullet_speed, active, father, nplayer)
        self.ammo = K_TRIPLE_AMMO
        self.name = 'Saddam rifle'
    
    def update(self):
        if not self.cooldown:
            if self.active:
                self.ammo -= 1
                self.cooldown = K_COOLDOWN
                x = elements.bullet(((random.randint(1,255)),
                                     (random.randint(1,255)),
                                     (random.randint(1,255))),
                                     (self.father.rect.topright),
                                     self.direction, father=self.father) 
                bullets.add(x)
                x = elements.bullet(((random.randint(1,255)),
                            (random.randint(1,255)),
                            (random.randint(1,255))),
                            ((self.father.rect.right, self.father.rect.centery)),
                             self.direction, father=self.father) 
                bullets.add(x)
                x = elements.bullet(((random.randint(1,255)),
                            (random.randint(1,255)),
                            (random.randint(1,255))),
                            (self.father.rect.bottomright),
                             self.direction, father=self.father) 
                bullets.add(x)
                snd_master.play('shoot')
                if not self.ammo:
                    game_master.game_m.set_base_weapon(self.father)
                    self.kill()
        else:
            self.cooldown -= 1
        
class fan_weapon(base_weapon):
    def __init__(self, d_vector, firing_key=M_WEAPON_SHOOT[0], bullet_speed=1, 
                 active=False, father=None, nplayer=0):
        base_weapon.__init__(self, d_vector, firing_key, bullet_speed, active, father, nplayer)
        self.ammo = K_FAN_AMMO
        self.name = 'Color HELL!'
    
    def update(self):
        if not self.cooldown:
            if self.active:
                self.ammo -= 1
                self.cooldown = K_COOLDOWN
                x = elements.bullet(((random.randint(1,255)),
                            (random.randint(1,255)),
                            (random.randint(1,255))),
                            (self.father.rect.topright),
                            (1,0.1), father=self.father)
                bullets.add(x) 
                x = elements.bullet(((random.randint(1,255)),
                            (random.randint(1,255)),
                            (random.randint(1,255))),
                            ((self.father.rect.right, self.father.rect.centery)),
                             self.direction,father=self.father)
                bullets.add(x) 
                x = elements.bullet(((random.randint(1,255)),
                            (random.randint(1,255)),
                            (random.randint(1,255))),
                            (self.father.rect.bottomright),
                            (1,-0.1), father=self.father)
                bullets.add(x) 
                x = elements.bullet(((random.randint(1,255)),
                            (random.randint(1,255)),
                            (random.randint(1,255))),
                            (self.father.rect.center),
                             (1,0.2), father=self.father)
                bullets.add(x)
                x = elements.bullet(((random.randint(1,255)),
                            (random.randint(1,255)),
                            (random.randint(1,255))),
                            (self.father.rect.center),
                             (1,0.5), 0.7, father=self.father)
                bullets.add(x)
                x = elements.bullet(((random.randint(1,255)),
                            (random.randint(1,255)),
                            (random.randint(1,255))),
                            (self.father.rect.center),
                             (1,-0.2), father=self.father)
                bullets.add(x) 
                x = elements.bullet(((random.randint(1,255)),
                            (random.randint(1,255)),
                            (random.randint(1,255))),
                            (self.father.rect.center),
                             (1,-0.5), 0.7, father=self.father)
                snd_master.play('shoot')           
                bullets.add(x)
                if not self.ammo:
                    game_master.game_m.set_base_weapon(self.father)
                    self.kill()
        else:
            self.cooldown -= 1

class h_weapon(base_weapon):
    def __init__(self, d_vector, firing_key=M_WEAPON_SHOOT[0], bullet_speed=1, 
                 active=False, father=None, nplayer=0):
        base_weapon.__init__(self, d_vector, firing_key, bullet_speed, active, father, nplayer)
        self.name = 'Slam Dunk!'
    
    def update(self):
        if not self.cooldown:
            if self.active:
                self.cooldown = K_COOLDOWN * 3
                x = elements.bullet(((random.randint(1,255)),
                            (random.randint(1,255)),
                            (random.randint(1,255))),
                            (self.father.rect.center),
                             self.direction,
                             0.5,
                             (5,15), father=self.father) 
                snd_master.play('shoot')
                bullets.add(x)
        else:
            self.cooldown -= 1
            
class beam_wall_weapon(base_weapon):
    
    def __init__(self, d_vector, firing_key=M_WEAPON_SHOOT[0], bullet_speed=1, 
                 active=False, father=None, nplayer=0):
        base_weapon.__init__(self, d_vector, firing_key, bullet_speed, father, nplayer)
        self.ammo = K_BEAM_AMMO  
        self.name = "Hell's hoover"      
    
    def update(self):
        if not self.cooldown:
            if self.active:
                self.ammo -= 1
                self.cooldown = K_COOLDOWN * 10
                x = elements.v_bullet(((random.randint(1,255)),
                                     (random.randint(1,255)),
                                     (random.randint(1,255))),
                                     (self.father.rect.topright),
                                     self.direction, father=self.father)
                snd_master.play('beam')
                bullets.add(x)
                if not self.ammo:
                    game_master.game_m.set_base_weapon(self.father)
                    self.kill()
        else:
            self.cooldown -= 1
            
        