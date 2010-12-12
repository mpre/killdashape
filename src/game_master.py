'''
Created on 09/dic/2010

@author: tosh
'''

try:
    import weapons_l
    import enemies_l
    import pygame
    import goodies
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
        self.possible_states = ('5SIN', 'BEGIN', 'HORDE')
        self.state = 'BEGIN'
        self.level = K_LEVEL
        self.paused = False
        self.to_pos_y = 0
        self.wait_in_state = 0
        self.enemy_placed = 0
    
    def act(self):
        print self.state
        if not self.cooldown:
            if self.state == 'BEGIN':
                self.state = random.choice((self.possible_states))
            elif self.state == '5SIN':
                if not self.wait_in_state:
                    self.wait_in_state = 10 # Numero di clock tick da attendere
                    if not self.to_pos_y:
                        self.to_pos_y = random.randint(1, K_WINDOW_DIM[1]-60)
                    en = enemies_l.sinusoidal_enemy(
                                                    (random.randint(1,255),
                                                     random.randint(1,255),
                                                     random.randint(1,255)),
                                                     (K_WINDOW_DIM[0], self.to_pos_y)
                                                     )
                    enemies.add(en)
                    self.enemy_placed += 1
                else:
                    self.wait_in_state -= 1
                if self.enemy_placed >= 5:
                    self.enemy_placed = 0
                    self.wait_in_state = 0
                    self.to_pos_y = 0
                    self.state = 'BEGIN'
                    self.cooldown = 7 * K_COOLDOWN 
            elif self.state == 'HORDE':
                # Invia un'orda di nemici!!
                self.state = 'BEGIN'            
            else:
                # Nessuno stato ?
                self.state = 'BEGIN'
        else:
            self.cooldown -= 1
            if self.cooldown == 0:
                self.state = 'BEGIN'
                
        if math.sqrt(self.points/100) > self.level:
            self.level += 1
        
        if random.randint(1,100) == 42:
            useful_lib.casual_goodie()
            
        if random.randint(1,200) == 42:
            graphic_goodies.cloud()
                    
    def rollstate(self):
        return random.choice(self.possible_states)
    
    def add_player(self, player):
        self.player = player
        
    def set_base_weapon(self):
        self.player.clear_weapons()
        self.player.add_weapons((weapons_l.base_weapon((1,0))))
        
    def set_triple_weapon(self):
        self.player.clear_weapons()
        self.player.add_weapon(weapons_l.triple_directed_weapon((1,0)))
    
    def set_fan_weapon(self):
        self.player.clear_weapons()
        self.player.add_weapon(weapons_l.fan_weapon((1,0)))
        
    def set_h_weapon(self):
        self.player.clear_weapons()
        self.player.add_weapon(weapons_l.h_weapon((1,0)))
    
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
    
    def get_level(self):
        return self.level
    
    def get_hp(self):
        if self.player:
            return self.player.hit_point()
        else:
            return 0
        
    def is_dead(self, name):
        if name == 'enemy_box':
            self.points += K_ENEMY_BOX_PT
        elif name == 'sinusoidal_enemy':
            self.points += K_ENEMY_SIN
            
    def get_points(self):
        return self.points
        
    def get_ammo(self):
        if self.player:
            return self.player.ammo()
        else:
            return 0
        
    def get_weapon(self):
        if self.player:
            return self.player.get_weapon()
        else:
            return 'None?!'
                
    def is_paused(self):
        return self.paused
    
    def pause(self):
        self.paused = not self.paused
        if self.paused:
            useful_lib.init_pause()
                
game_m = game_master()