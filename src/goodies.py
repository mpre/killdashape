'''
Created on 10/dic/2010

@author: tosh
'''

try:
    import game_master
    import pygame
    import random
    from global_vars import *
    from killdashape_k import *
except:
    print 'Errore in goodies'

f_names = ['triple_w_goodie',
           'beam_goodie',
           'fan_goodie']

class goodie(pygame.sprite.Sprite):
    
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.cooldown = K_GOODIE_COOLDOWN
        gds.add(self)
        
    def update(self):
        self.cooldown -= 1
        if not self.cooldown:
            self.die()
            
    def die(self):
        gds.remove(self)
        
class triple_w_goodie(goodie):
    
    def __init__(self, letter='Triple!'):
        goodie.__init__(self)
        self.image = pygame.font.Font(None, 15).render(letter, True, (0,0,250), (255,255,255))
        self.rect = self.image.get_rect()
        self.rect.center = ((random.randint(100, K_WINDOW_DIM[0]),
                            random.randint(0, K_WINDOW_DIM[1])))
        
    def kill(self):
        game_master.game_m.set_triple_weapon()
        self.die()

class beam_goodie(goodie):
    
    def __init__(self, letter='Beam!'):
        goodie.__init__(self)
        self.image = pygame.font.Font(None, 15).render(letter, True, (0,0,250), (0,255,255))
        self.rect = self.image.get_rect()
        self.rect.center = ((random.randint(100, K_WINDOW_DIM[0]),
                            random.randint(0, K_WINDOW_DIM[1])))
        
    def kill(self):
        game_master.game_m.set_beam_weapon()
        self.die()

class fan_goodie(goodie):
    
    def __init__(self, letter='Fan!!'):
        goodie.__init__(self)
        self.image = pygame.font.Font(None, 15).render(letter, True, (0,0,250), (255,255,0))
        self.rect = self.image.get_rect()
        self.rect.center = ((random.randint(100, K_WINDOW_DIM[0]),
                            random.randint(0, K_WINDOW_DIM[1])))
        
    def kill(self):
        game_master.game_m.set_fan_weapon()
        self.die()
