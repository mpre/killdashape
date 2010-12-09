'''
Created on 09/dic/2010

@author: tosh
'''

try:
    import pygame
    from pygame.locals import *
    import random
    import math
    from killdashape_k import *
    import elements
    from global_vars import *
    from sound_master import *
except:
    print 'mmmm'

class game_master(object):
    
    def __init__(self, player=None):
        self.player = player
        self.points = 0
        self.cooldown = 0
        self.sintimes = 70
        self.pass_times = 50
        self.possible_states = ('5SIN', 'PASS')
        self.state = '5SIN'
        self.level = K_LEVEL
    
    def add_player(self, player):
        self.player = player
        
    def set_base_weapon(self):
        self.player.clear_weapons()
        self.player.add_weapons((elements.base_weapon((1,0), K_d)))
        
    def set_triple_weapon(self):
        self.player.clear_weapons()
        self.player.add_weapon(elements.triple_directed_weapon((1,0), K_d))
    
    def set_fan_weapon(self):
        self.player.clear_weapons()
        self.player.add_weapon(elements.fan_weapon((1,0), K_d))
        
    def set_h_weapon(self):
        self.player.clear_weapons()
        self.player.add_weapon(elements.h_weapon((1,0), K_d))    
    
    def add_enemy(self):
        for _ in range(5):
            en = elements.enemy_box([random.randint(30,255),
                                     random.randint(30,255),
                                     random.randint(30,255)],                       
                                     [random.randint(200,K_WINDOW_DIM[0] - K_BOX_DIMENSION[0]),
                                      random.randint(0,K_WINDOW_DIM[1] - K_BOX_DIMENSION[1])])
        enemies.add(en)
        
    def is_dead(self, name):
        if name == 'enemy_box':
            self.points += K_ENEMY_BOX_PT
        elif name == 'sinusoidal_enemy':
            self.points += K_ENEMY_SIN
            
    def get_points(self):
        return self.points
    
    def act(self):
        if not self.cooldown:
            if self.state == '5SIN':
                # Inserisco nemici sinusoidali
                if self.sintimes % 5 == 0:
                    en = elements.sinusoidal_enemy([random.randint(1,255),
                                                 random.randint(1,255),
                                                 random.randint(1,255)],                       
                                                 [random.randint(200,K_WINDOW_DIM[0] - K_BOX_DIMENSION[0]),
                                                  random.randint(10, K_WINDOW_DIM[1] - 10)])
                    enemies.add(en)
                self.sintimes -= 1
                if not self.sintimes:
                    self.cooldown = K_COOLDOWN * 30 / self.level
                    self.sintimes = 150
                    self.state = 'PASS'
                
            elif self.state == 'PASS':
                # Fa niente
                if not self.pass_times:
                    self.state = self.rollstate()
                    self.pass_times = K_COOLDOWN * 30 / self.level
                else:
                    self.pass_times -=1
                pass
        else:
            self.cooldown -= 1
            
        if math.sqrt(self.points/100) > self.level:
            self.level +=1
            
    def rollstate(self):
        return random.choice(self.possible_states)
    
    def get_level(self):
        return self.level
            
    
game_m = game_master()