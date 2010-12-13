'''
Created on 10/dic/2010

@author: tosh
'''

try:
    import random
    import elements
    from killdashape_k import *
    from global_vars import *
    from sound_master import *
    from game_master import *
    import useful_lib
except:
    print 'Errore nell\'importazione in enemies'

class enemy_box(elements.box):
    """I nemici quadrati"""
    def __init__(self, color, initial_pos):
        elements.box.__init__(self, color, initial_pos)
        self.color = color
        self.cooldown = K_COOLDOWN + random.randint(1, 25)
        enemies.add(self)
    
    def update(self, event=None, rest=None):
        if random.randint(0,1):
            if random.randint(0,1):
                if not self.rect.bottom >= K_WINDOW_DIM[1]: 
                    self.rect = self.rect.move(0, K_ENEMY_MOV)
            else:
                if not self.rect.top <= 0:
                    self.rect = self.rect.move(0, -K_ENEMY_MOV)
        else:
            if random.randint(0,1):
                if not self.rect.right >= K_WINDOW_DIM[0]:
                    self.rect = self.rect.move(K_ENEMY_MOV, 0)
            else:
                if not self.rect.left <= 0:
                    self.rect = self.rect.move(-K_ENEMY_MOV, 0)
        if not self.cooldown:
            self.cooldown = K_COOLDOWN * 20 + random.randint(30, 200)
            x = elements.bullet( (255,255,255),
                                 (self.rect.left, self.rect.centery),
                                 (-1,0),
                                 0.5)
            en_bullets.add(x)
        else:
            self.cooldown -= 1
    
    def kill(self):
        snd_master.play('enemy_explosion')
        game_m.is_dead(self.__class__.__name__)
        useful_lib.create_explosion_at(self.color, self.rect)
        self.silent_die()
        
    def silent_die(self):
        enemies.remove(self)
        g_goodies.remove(self.baloon)
        self = None
        
class sinusoidal_enemy(enemy_box):
    
    def __init__(self, color, initial_pos):
        enemy_box.__init__(self, color, initial_pos)
        self.rect.right = K_WINDOW_DIM[0] - 3
        self.degree = 0
        self.amp = random.uniform(1,7)
        if random.randint(40,55) == 42:
            self.baloon = graphic_goodies.en_baloon(K_EN_SINUSOIDAL_SENT, self, 10, 
                                                    FONT_PATH + "bitrip.ttf", 
                                                    (255,255,255), (0,0,0), True)
        else:
            self.baloon = None
    
    def update(self, event=None, rest=None):
        self.degree += 5
        self.degree = self.degree % 360
        self.rect = self.rect.move(-K_ENEMY_MOV, 
                                   self.amp * math.sin(math.radians(self.degree)))
        if self.rect.bottom >= K_WINDOW_DIM[1]-8 or self.rect.top <= 0:
            self.degree = (self.degree + 180) % 360
        if self.rect.right < -10:
            self.silent_die()
        if not self.cooldown:
            if random.randint(1,10) <= 6:
                x = elements.bullet( (0,0,0),
                                     (self.rect.left, self.rect.centery),
                                     (-1,0),
                                     0.5)
                en_bullets.add(x)
            self.cooldown = int(K_COOLDOWN/math.log(game_m.get_level()+1)) + random.randint(1, 10)
        else:
            self.cooldown -= 1
            
            
class fw_enemy(enemy_box):
    def __init__(self, color, initial_pos):
        enemy_box.__init__(self, color, initial_pos)
        self.rect.right = K_WINDOW_DIM[0] - 3
        self.t = 1
        if random.randint(40,50) == 42:
            self.baloon = graphic_goodies.en_baloon(K_EN_FW_SENT, self, 10, 
                                                    FONT_PATH + "bitrip.ttf", 
                                                    (255,255,255), (0,0,0), True)
        else:
            self.baloon = None
    
    def update(self, event=None, rest=None):
        self.t += 1
        self.rect = self.rect.move(int(-K_ENEMY_MOV * math.log(self.t/2 + 0.5) * random.uniform(1,1.5)), 0)
        if self.rect.right < -10:
            self.silent_die()
        return
    
class follower_enemy(enemy_box):
    def __init__(self, color, initial_pos, p=None):
        enemy_box.__init__(self, color, initial_pos)
        self.rect.right = K_WINDOW_DIM[0] - 3
        if p:
            self.objective = p.rect.centery
        else:
            self.objective = game_m.get_random_player().rect.centery
        self.baloon = None
        
    def update(self):
        if not self.objective:
            # E' morto l'obiettivo
            self.rect = self.rect.move(-K_ENEMY_MOV, 0)
            if self.rect.right < -5:
                self.kill()
        if self.rect.centerx > K_WINDOW_DIM[0] - 60:
            # Deve entrare nella finestra
            self.rect = self.rect.move(-K_ENEMY_MOV, 0)
        elif self.cooldown:
            # Attende
            self.cooldown -= 1
        else:
            # Si muove o spara
            if self.rect.centery - 30 < self.objective < self.rect.centery + 30:
                # Spara
                bull = elements.v_bullet((253,253,0),
                                         (self.rect.left, self.rect.centery),
                                         (-1,0),
                                         0.3)
                en_bullets.add(bull)
                self.cooldown = int(K_COOLDOWN * 15 / math.log(game_m.get_level()+1)) + random.randint(10, 200)
                p = game_m.get_random_player()
                if p:
                    self.objective = p.rect.centery
            else:
                if self.rect.centery < self.objective:
                    self.rect = self.rect.move(0, K_ENEMY_MOV)
                else:
                    self.rect = self.rect.move(0, -K_ENEMY_MOV)
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        