'''
Created on 08/dic/2010

@author: tosh
'''

try:
    import graphic_goodies
    import math
    from global_vars import *
    import elements
    from killdashape_k import *
    from game_master import *
except:
    print "cazzo non ha importato bene"

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
                e = elements.enemy_junkie(color, rect.center, vector)
                junkie.add(e)
                
def blitstats(screen):
    point_font = pygame.font.Font(None, 20)
    point_i = point_font.render('{0} : {1}'.format('Points',game_m.get_points()), 
                                     True, K_FONT_COLOR)
    point_r = point_i.get_rect()
    point_r.topleft = (10, 3)
    screen.blit(point_i, point_r)
    return screen

def init_stats():
    graphic_goodies.HUD_point()
    graphic_goodies.HUD_hp()
    graphic_goodies.HUD_level()
    
def init_pause():
    graphic_goodies.HUD_pause()