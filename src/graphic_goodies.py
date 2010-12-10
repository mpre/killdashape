'''
Created on 10/dic/2010

@author: tosh
'''

try:
    import pygame
    from pygame.locals import *
    from killdashape_k import *
    from global_vars import *
    from game_master import *
except:
    print 'Errore importando in graphic_goodies'
    
class HUD_el(pygame.sprite.Sprite):
    
    def __init__(self, font_dim=20, font_color=K_FONT_COLOR, font=None):
        pygame.sprite.Sprite.__init__(self)
        self.font = pygame.font.Font(font, font_dim)
        self.color = font_color
        g_goodies.add(self)
        
class HUD_point(HUD_el):
    
    def __init__(self):
        HUD_el.__init__(self)
        self.image = self.font.render('Points: {0}'.format(game_m.get_points()),
                                      True, self.color)
        self.rect = self.image.get_rect()
        self.rect.topleft = (10,3)
        
    def update(self):
        self.image = self.font.render('POINTS: {0}'.format(game_m.get_points()),
                                      True, self.color)
        
class HUD_hp(HUD_el):
    
    def __init__(self):
        HUD_el.__init__(self)
        self.image = self.font.render('HP: {0}'.format(game_m.get_hp()),
                                      True, self.color)
        self.rect = self.image.get_rect()
        self.rect.topleft = (K_WINDOW_DIM[0]-50, 3)
        
    def update(self):
        self.image = self.font.render('HP: {0}'.format(game_m.get_hp()),
                                      True, self.color)
        
class HUD_level(HUD_el):
    
    def __init__(self):
        HUD_el.__init__(self)
        self.image = self.font.render('LEVEL: {0}'.format(game_m.get_level()),
                                      True, self.color)
        self.rect = self.image.get_rect()
        self.rect.top = 3
        self.rect.centerx = K_WINDOW_DIM[0]/2
        
    def update(self):
        self.image = self.font.render('LEVEL: {0}'.format(game_m.get_level()),
                                      True, self.color)
        
class HUD_pause(HUD_el):
    
    def __init__(self):
        HUD_el.__init__(self)
        self.image = self.font.render('PAUSED',
                                      True, self.color)
        self.rect = self.image.get_rect()
        self.rect.center = (K_WINDOW_DIM[0]/2, K_WINDOW_DIM[1]/2)
        
    def update(self):
        if game_m.is_paused():
            self.image = self.font.render('PAUSED'.format(game_m.get_level()),
                                          True, self.color)
        else:
            g_goodies.remove(self)



