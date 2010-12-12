'''
Created on 09/dic/2010

@author: tosh
'''

try:
    import pygame
    from pygame.locals import *
    from killdashape_k import *
except:
    print "cazzo non ha importato bene"

pygame.init()

class sound_m(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.snd = {}
        self.snd['enemy_explosion'] = pygame.mixer.Sound(SND_PATH + "enemy_explosion-1.wav")
        self.snd['shoot'] = pygame.mixer.Sound(SND_PATH + "shoot-1.wav")
        self.snd['beam'] = pygame.mixer.Sound(SND_PATH + "beam.wav")
        self.snd['wow'] = pygame.mixer.Sound(SND_PATH + "wow.wav")
        self.snd['base_loop'] = pygame.mixer.Sound(SND_PATH + "game_loop4.aif")
        self.snd['base_loop'].play(-1)
        self.paused = False
        
    def play(self, sound):
        self.snd[sound].play()
    
    def pause_loop(self):
        if self.paused:
            self.snd['base_loop'].play(-1)
        else:    
            self.snd['base_loop'].stop()
        self.paused = not self.paused
        
snd_master = sound_m()