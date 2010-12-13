'''
Created on 08/dic/2010

@author: tosh
'''

try:
    import pygame
except Exception, message:
    print "cazzo non ha importato bene in global_vars", message
    
enemies = pygame.sprite.RenderUpdates()
en_bullets = pygame.sprite.RenderUpdates()
bullets = pygame.sprite.RenderUpdates()
junkie = pygame.sprite.RenderUpdates()
g_goodies = pygame.sprite.RenderUpdates()
back_elements = pygame.sprite.RenderUpdates()
gds = pygame.sprite.RenderUpdates()
player = pygame.sprite.RenderUpdates()
lndscp_back = pygame.sprite.RenderUpdates()
lndscp_front = pygame.sprite.RenderUpdates()
active_weapons = []