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
        self = None
        
class sinusoidal_enemy(enemy_box):
    
    def __init__(self, color, initial_pos):
        enemy_box.__init__(self, color, initial_pos)
        self.rect.right = K_WINDOW_DIM[0] - 3
        self.degree = 0
    
    def update(self, event=None, rest=None):
        self.degree += 5
        self.degree = self.degree % 360
        self.rect = self.rect.move(-K_ENEMY_MOV, 2 * K_ENEMY_MOV * math.sin(math.radians(self.degree)))
        if self.rect.bottom >= K_WINDOW_DIM[1] or self.rect.top <= 0:
            self.degree = (self.degree + 180) % 360
        if self.rect.right < -10:
            self.silent_die()
        if not self.cooldown:
            if random.randint(1,10) <= 6:
                x = elements.bullet( (255,255,255),
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
    
    def update(self, event=None, rest=None):
        self.rect = self.rect.move(-K_ENEMY_MOV * math.log(self.t))
        if self.rect.right < -10:
            self.silent_die()
        if not self.cooldown:
            if random.randint(1,10) <= 6:
                x = elements.bullet( (255,255,255),
                                     (self.rect.left, self.rect.centery),
                                     (-1,0),
                                     4)
                en_bullets.add(x)
            self.cooldown = K_COOLDOWN * float(20)/math.log(game_m.get_level()+1) + random.randint(1, 10)
        else:
            self.cooldown -= 1
        return