'''
Created on 08/dic/2010

@author: tosh
'''

try:
    import pygame
except:
    print "cazzo non ha importato bene"
    
enemies = pygame.sprite.RenderUpdates()
en_bullets = pygame.sprite.RenderUpdates()
bullets = pygame.sprite.RenderUpdates()
junkie = pygame.sprite.RenderUpdates()
g_goodies = pygame.sprite.RenderUpdates()
back_elements = pygame.sprite.RenderUpdates()
gds = pygame.sprite.RenderUpdates()
player = pygame.sprite.RenderUpdates()
landscape = pygame.sprite.RenderUpdates()
active_weapons = []