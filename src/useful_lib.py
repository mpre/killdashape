'''
Created on 08/dic/2010

@author: tosh
'''

try:
    import math
    from global_vars import *
    import elements
except:
    print "cazzo non ha importato bene"

# -*- Funzioni di supporto -*-
def angle(v1, v2):
    v1_length = math.sqrt(v1[0]**2 + v1[1]**2)
    v2_length = math.sqrt(v2[0]**2 + v2[1]**2)
    dotproduct = (v1[0] * v2[0]) + (v1[1] * v2[1]) # prodotto scalare
    
    return math.acos(dotproduct / (v1_length * v2_length))

def create_explosion_at(color, rect):
    for vector in ((1,0), (1,1), (0,1), (-1,1), 
                   (-1,0), (-1,-1), (0,-1), (1,-1),
                   (2,1), (2,-1), (0.5,1), (0.5,-1),
                   (-2,1), (-2,-1), (-0.5,1), (-0.5,-1)
                   ):
                e = elements.enemy_junkie(color, rect.center, vector)
                junkie.add(e)