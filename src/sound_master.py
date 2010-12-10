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
        
    def play(self, sound):
        self.snd[sound].play()
           
     
snd_master = sound_m()