'''
Created on 09/dic/2010

@author: tosh
'''

try:
    import weapons_l
    import enemies_l
    import pygame
    import graphic_goodies
    from pygame.locals import *
    import random
    import math
    from killdashape_k import *
    import elements
    from global_vars import *
    from sound_master import *
    import useful_lib
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
        self.paused = False
    
    def add_player(self, player):
        self.player = player
        
    def set_base_weapon(self):
        self.player.clear_weapons()
        self.player.add_weapons((weapons_l.base_weapon((1,0), K_d)))
        
    def set_triple_weapon(self):
        self.player.clear_weapons()
        self.player.add_weapon(weapons_l.triple_directed_weapon((1,0), K_d))
    
    def set_fan_weapon(self):
        self.player.clear_weapons()
        self.player.add_weapon(weapons_l.fan_weapon((1,0), K_d))
        
    def set_h_weapon(self):
        self.player.clear_weapons()
        self.player.add_weapon(weapons_l.h_weapon((1,0), K_d))
    
    def set_beam_weapon(self):
        self.player.clear_weapons()
        self.player.add_weapon(weapons_l.beam_wall_weapon((1,0)))
        
    def add_enemy(self):
        for _ in range(5):
            en = enemies_l.enemy_box([random.randint(30,255),
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
                    en = enemies_l.sinusoidal_enemy([random.randint(1,255),
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
            if self.level == 5:
                graphic_goodies.HUD_msg("WOW")
                snd_master.play('wow')
            
        graphic_goodies.background_star()
        
    def rollstate(self):
        return random.choice(self.possible_states)
    
    def get_level(self):
        return self.level
    
    def get_hp(self):
        if self.player:
            return self.player.hit_point()
        else:
            return 0
        
    def is_paused(self):
        return self.paused
    
    def pause(self):
        self.paused = not self.paused
        if self.paused:
            useful_lib.init_pause()
                
game_m = game_master()