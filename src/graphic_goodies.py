'''
Created on 10/dic/2010

@author: tosh
'''

try:
    import pygame
    import random
    from pygame.locals import *
    from killdashape_k import *
    from global_vars import *
    from game_master import *
except:
    print 'Errore importando in graphic_goodies'
    
class HUD_el(pygame.sprite.Sprite):
    
    def __init__(self, font_dim=10, font_color=K_FONT_COLOR, font=K_FONT):
        pygame.sprite.Sprite.__init__(self)
        self.font_type = font
        self.font_dim = font_dim
        self.font = pygame.font.Font(self.font_type, self.font_dim)
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
    
    def __init__(self, player=None):
        HUD_el.__init__(self)
        self.player = player
        self.image = self.font.render('HP[{1}]: {0}'.format(game_m.get_hp(player), 
                                                            self.player.get_p_number()),
                                      True, self.color)
        self.rect = self.image.get_rect()
        self.rect.topleft = (K_WINDOW_DIM[0]-50, 3 + (player.get_p_number())*15)
        
    def update(self):
        self.image = self.font.render('HP[{1}]: {0}'.format(game_m.get_hp(self.player), 
                                                            self.player.get_p_number()+1),
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
        
class HUD_ammo(HUD_el):
    
    def __init__(self, player=None):
        HUD_el.__init__(self)
        self.player = player
        self.image = self.font.render('AMMO[{1}]: {0}'.format(game_m.get_ammo(player), 
                                                              self.player.get_p_number()+1),
                                      True, self.color)
        self.rect = self.image.get_rect()
        self.rect.bottomleft = (10, K_WINDOW_DIM[1]-3 - (player.get_p_number())*15)
        
    def update(self):
        self.image = self.font.render('AMMO[{1}]: {0}'.format(game_m.get_ammo(self.player), 
                                                              self.player.get_p_number()+1),
                                      True, self.color)
        
class HUD_gun(HUD_el):
    
    def __init__(self):
        HUD_el.__init__(self)
        self.image = self.font.render('WEAPON: {0}'.format(game_m.get_weapon()),
                                      True, self.color)
        self.rect = self.image.get_rect()
        self.rect.bottom = K_WINDOW_DIM[1] - 3
        self.rect.left = K_WINDOW_DIM[0]/2 + self.image.get_size()[1]/2
        
    def update(self):
        self.image = self.font.render('WEAPON: {0}'.format(game_m.get_weapon()),
                                      True, self.color)
        
class HUD_pause(HUD_el):
    
    def __init__(self):
        HUD_el.__init__(self)
        self.image = self.font.render('PAUSED - Press ESC to exit',
                                      True, self.color)
        self.rect = self.image.get_rect()
        self.rect.center = (K_WINDOW_DIM[0]/2, K_WINDOW_DIM[1]/2)
        
    def update(self):
        if game_m.is_paused():
            self.image = self.font.render('PAUSED - Press ESC to exit'.format(game_m.get_level()),
                                          True, self.color)
        else:
            g_goodies.remove(self)
            
class HUD_msg(HUD_el):
    def __init__(self, msg):
        self.phase = 4
        self.max_dim = 50
        HUD_el.__init__(self, int(0.4*self.max_dim), (200,0,0))
        self.msg = msg
        self.image = self.font.render(self.msg,
                                      True, self.color)
        self.rect = self.image.get_rect()
        self.rect.center = K_WINDOW_DIM[0]/2, K_WINDOW_DIM[1]
        self.i = 2.0 * K_TICK
        self.colors = ((210,0,0),
                       (0,210,0),
                       (0,0,210),
                       )
        
    def update(self):
        if 0.05 <= (self.i / (self.phase*K_TICK)) < 0.1:
            self.font_dim = 0.4 * self.max_dim
        elif 0.1 <= (self.i / (self.phase*K_TICK)) < 0.15:
            self.font_dim = 0.50 * self.max_dim
        elif 0.15 <= (self.i / (self.phase*K_TICK)) < 0.20:
            self.font_dim = 0.60 * self.max_dim
        elif 0.20 <= (self.i / (self.phase*K_TICK)) < 0.25:
            self.font_dim = 0.70 * self.max_dim
        elif 0.25 <= (self.i / (self.phase*K_TICK)) < 0.30:
            self.font_dim = 0.60 * self.max_dim
        elif 0.30 <= (self.i / (self.phase*K_TICK)) < 0.35:
            self.font_dim = 0.50 * self.max_dim
        elif 0.35 <= (self.i / (self.phase*K_TICK)) < 0.45:
            self.font_dim = 0.40 * self.max_dim
        elif 0.45 <= (self.i / (self.phase*K_TICK)) < 0.50:
            self.font_dim = 0.30 * self.max_dim
        elif 0.55 <= (self.i / (self.phase*K_TICK)) < 0.6:
            self.font_dim = 0.40 * self.max_dim
        elif 0.6 <= (self.i / (self.phase*K_TICK)) < 0.65:
            self.font_dim = 0.50 * self.max_dim
        elif 0.65 <= (self.i / (self.phase*K_TICK)) < 0.70:
            self.font_dim = 0.60 * self.max_dim
        elif 0.70 <= (self.i / (self.phase*K_TICK)) < 0.75:
            self.font_dim = 0.70 * self.max_dim
        elif 0.75 <= (self.i / (self.phase*K_TICK)) < 0.80:
            self.font_dim = 0.60 * self.max_dim
        elif 0.80 <= (self.i / (self.phase*K_TICK)) < 0.85:
            self.font_dim = 0.50 * self.max_dim
        elif 0.85 <= (self.i / (self.phase*K_TICK)) < 0.95:
            self.font_dim = 0.40 * self.max_dim
        elif 0.95 <= (self.i / (self.phase*K_TICK)) < 1:
            self.font_dim = 0.30 * self.max_dim
        
        if not self.i % 20:
            self.color = random.choice(self.colors)
        self.font = pygame.font.Font(self.font_type, int(self.font_dim))     
        self.image = self.font.render(self.msg,
                                      True, self.color)
        self.rect = self.image.get_rect()
        self.rect.centerx = K_WINDOW_DIM[0]/2
        self.rect.bottom = K_WINDOW_DIM[1]
                
        self.i += 1
        
        if self.i > self.phase *K_TICK:
            self.kill()
            
    def kill(self):
        g_goodies.remove(self)
        self = None
    

class background_star(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((3,3))
        self.image.fill((139, 137, 137))
        self.rect = self.image.get_rect()
        self.rect.centery = random.randint(1, K_WINDOW_DIM[1]-50)
        self.rect.centerx = K_WINDOW_DIM[0]
        back_elements.add(self)
        
    def update(self):
        if self.rect.centerx + 3:
            self.rect.centerx -= 1 + 1 * (self.rect.centery / 20)
        else:
            self.kill()
    
    def kill(self):
        back_elements.remove(self)

class story_baloon(HUD_el):
    def __init__(self, msg, cooldown=2*K_TICK, font_dim=10, font=K_BALOON_FONT, font_color=(0,0,0), 
                 font_backgroud=(255,255,255), alpha_background=True):
        HUD_el.__init__(self, font_dim, font_color, font)
        self.msg = msg
        self.back_color = font_backgroud
        self.cooldown = cooldown
        self.died = False
        if alpha_background:
            self.image = self.font.render(self.msg, True, self.color, self.back_color)
        else:
            self.image = self.font.render(self.msg, True, self.color)
        self.rect = self.image.get_rect()
        
    def update(self):
        self.rect.center = (K_WINDOW_DIM[0]/2,
                            K_WINDOW_DIM[1]/2 - 15
                            )
        self.cooldown -= 1
        if self.cooldown == 0:
            self.kill()
            
    def kill(self):
        g_goodies.remove(self)
        self.died = True
        
    def is_died(self):
        return self.died
        

class baloon(HUD_el):
    def __init__(self, msg_group, father, font_dim=10, font=K_BALOON_FONT, font_color=(0,0,0), 
                 font_backgroud=(255,255,255), alpha_background=True):
        HUD_el.__init__(self, font_dim, font_color, font)
        self.msg = random.choice(msg_group)
        self.father = father
        self.back_color = font_backgroud
        if alpha_background:
            self.image = self.font.render(self.msg, True, self.color, self.back_color)
        else:
            self.image = self.font.render(self.msg, True, self.color)
        self.rect = self.image.get_rect()
        
    def update(self):
        self.rect.bottom = self.father.rect.top - 5
        self.rect.centerx = self.father.rect.centerx
        
class en_baloon(baloon):
    def __init__(self, msg_group, father, font_dim=15, 
                 font=K_FONT, font_color=(0,0,0), font_backgroud=(255,255,255),
                 alpha_background=False):
        baloon.__init__(self, msg_group, father, font_dim, 
                        font, font_color, font_backgroud, alpha_background)
        #self.image.set_alpha(170)
        pass
        
class cloud(pygame.sprite.Sprite):
    def __init__(self, y_pos=None):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(IMG_PATH + 'cloud2.png').convert()
        self.image.set_colorkey(self.image.get_at((0,0)))
        self.rect = self.image.get_rect()
        if not y_pos:
            y_pos=random.randint(5,K_WINDOW_DIM[1]/3)
        self.rect.centery = y_pos
        self.rect.left = K_WINDOW_DIM[0]
        lndscp_back.add(self)
        
    def update(self):
        self.rect.left -= 1
        #self.rect.centery = self.rect.centery + random.randint(-1,1)
        if self.rect.top < 0:
            self.rect.move(0,1)
        if self.rect.bottom > K_WINDOW_DIM[1]/3:
            self.rect.move(0,-1)
        if self.rect.right < 0:
            self.kill()
            
    def kill(self):
        g_goodies.remove(self)
        self = None
        
    def hurts(self):
        return False
        
class floor(pygame.sprite.Sprite):
    def __init__(self, y_pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(IMG_PATH + 'floor.png').convert()
        self.rect = self.image.get_rect()
        self.rect.left = y_pos
        self.rect.bottom = K_WINDOW_DIM[1]
        lndscp_back.add(self)
        
    def update(self):
        pass
        
    def hurts(self):
        return True

class star(pygame.sprite.Sprite):
    def __init__(self, father):
        pygame.sprite.Sprite.__init__(self)
        self.father = father
        self.image = pygame.Surface((K_BOX_DIMENSION[0], 
                                     K_BOX_DIMENSION[1]))
        self.image.fill((170,170,0))
        self.color = 0
        self.rect = self.image.get_rect()
        self.rect.center = self.father.rect.center
        self.cooldown = 3*K_TICK
        player_goodies.add(self)
        
    def update(self):
        self.cooldown -= 1
        if self.cooldown % 5 == 0:
            if self.color == 0:
                self.image.fill((250,250,250))
                self.color = 1
            else:
                self.image.fill((250,0,0))
                self.color = 0
        self.rect.center = self.father.rect.center
        if self.cooldown == 0:
            player_goodies.remove(self)
            self.father.remove_star()
            self = None
        
        
        
        
        
        
        
        

