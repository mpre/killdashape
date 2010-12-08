'''
Created on 08/dic/2010

@author: tosh
'''

try:
    import pygame
except:
    print "cazzo non ha importato bene"
    
enemies = pygame.sprite.RenderUpdates()
bullets = pygame.sprite.RenderUpdates()
junkie = pygame.sprite.RenderUpdates()
active_weapons = []