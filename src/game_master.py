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
    
    def add_player(self, player):
        self.player = player
        
    def set_base_weapon(self):
        self.player.add_weapons((elements.base_weapon((1,0), K_d),
                                 elements.base_weapon((0,1), K_s),
                                 elements.base_weapon((0,-1), K_a),
                                 elements.base_weapon((-1,0), K_w)))
        
    def set_triple_weapon(self):
        self.player.add_weapon(elements.triple_directed_weapon((1,0), K_z))
        
    def add_enemy(self):
        for _ in range(5):
            en = elements.enemy_box([random.randint(1,255),
                                     random.randint(1,255),
                                     random.randint(1,255)],                       
                                     [random.randint(200,640 - K_BOX_DIMENSION[0]),
                                      random.randint(30,320 - K_BOX_DIMENSION[1])])
        enemies.add(en)
    
game_m = game_master()