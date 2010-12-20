'''
Created on 09/dic/2010

@author: tosh
'''

try:
    import pygame
    from pygame.locals import *
    from killdashape_k import *
except Exception, message:
    print "sound_master.py:",message

pygame.init()

class sound_m(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        print 'Initializing sound...'
        self.snd = {}
        self.snd['enemy_explosion'] = pygame.mixer.Sound(SND_PATH + "enemy_explosion-1.wav")
        self.snd['shoot'] = pygame.mixer.Sound(SND_PATH + "shoot-3.wav")
        self.snd['triple_shoot'] = pygame.mixer.Sound(SND_PATH + "triple_shoot.wav")
        self.snd['beam'] = pygame.mixer.Sound(SND_PATH + "beam-1.wav")
        self.snd['1up'] = pygame.mixer.Sound(SND_PATH + "1up.wav")
        self.snd['wow'] = pygame.mixer.Sound(SND_PATH + "wow.wav")
        self.snd['triple_goodie'] = pygame.mixer.Sound(SND_PATH + "triple_goodie-1.wav")
        self.snd['base_loop'] = pygame.mixer.Sound(SND_PATH + "game_loop4.aif")
        self.snd['mark_boss'] = pygame.mixer.Sound(SND_PATH + "game_loop3.wav")
        self.snd['mark_explode'] = pygame.mixer.Sound(SND_PATH + "markexplode.wav")
        self.snd['base_loop'].play(-1)
        self.paused = False
        self.in_boss = False
        
    def play(self, sound):
        self.snd[sound].play()
    
    def pause_loop(self):
        if self.paused:
            self.snd['base_loop'].play(-1)
        else:    
            self.snd['base_loop'].stop()
        self.paused = not self.paused
        
    def boss_loop(self, boss_name=None):
        if not self.in_boss:
            self.pause_loop()
            self.snd['mark_boss'].play(-1)
        else:
            self.snd['mark_boss'].stop()
            self.pause_loop()
        self.in_boss = not self.in_boss
        
        
snd_master = sound_m()