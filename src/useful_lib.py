'''
Created on 08/dic/2010

@author: tosh
'''

try:
    import graphic_goodies
    import math
    import random
    import goodies
    from global_vars import *
    import elements
    from killdashape_k import *
    from game_master import *
except:
    print "cazzo non ha importato bene"

pl_goodies = []

# -*- Funzioni di supporto -*-
def angle(v1, v2):
    v1_length = math.sqrt(v1[0]**2 + v1[1]**2)
    v2_length = math.sqrt(v2[0]**2 + v2[1]**2)
    dotproduct = (v1[0] * v2[0]) + (v1[1] * v2[1]) # prodotto scalare
    
    return math.acos(dotproduct / (v1_length * v2_length))

def angle_deg(v1, v2):
    return math.degrees(angle(v1,v2))

def create_explosion_at(color, rect):
    for vector in ((1,0), (1,1), (0,1), (-1,1), 
                   (-1,0), (-1,-1), (0,-1), (1,-1),
                   (2,1), (2,-1), (0.5,1), (0.5,-1),
                   (-2,1), (-2,-1), (-0.5,1), (-0.5,-1)
                   ):
                elements.enemy_junkie(color, rect.center, vector)
                
def create_explosion_at_pos(color, pos):
    for vector in ((1,0), (1,1), (0,1), (-1,1), 
                   (-1,0), (-1,-1), (0,-1), (1,-1),
                   (2,1), (2,-1), (0.5,1), (0.5,-1),
                   (-2,1), (-2,-1), (-0.5,1), (-0.5,-1)
                   ):
                elements.enemy_junkie(color, pos, vector)
    
def init_stats():
    global pl_goodies
    graphic_goodies.HUD_point()
    graphic_goodies.HUD_level()
    for p in player:
        pl_goodies += [graphic_goodies.HUD_hp(p)]
        pl_goodies += [graphic_goodies.HUD_ammo(p)]
    #graphic_goodies.HUD_gun()
    
def init_landscape():
    y_pos = 0
    while y_pos < K_WINDOW_DIM[0]:
        graphic_goodies.floor(y_pos)
        y_pos += 8
    
def init_pause():
    graphic_goodies.HUD_pause()
    #snd_master.pause_loop()
    
def casual_goodie():
    # Sceglie un goodie casuale
    g = random.choice(goodies.f_names)
    eval('goodies.'+g+'()')
    
def clear_goodies():
    global pl_goodies
    for g in pl_goodies:
        g_goodies.remove(g)
        pl_goodies = []
    
def restart_pl_goodies():
    global pl_goodies
    for p in player:
        pl_goodies += [graphic_goodies.HUD_hp(p)]
        pl_goodies += [graphic_goodies.HUD_ammo(p)]