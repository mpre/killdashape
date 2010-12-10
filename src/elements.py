'''
Created on 08/dic/2010

@author: tosh
'''
try:
    import pygame
    from pygame.locals import *
    import random
    import math
    from killdashape_k import *
    from global_vars import *
    from useful_lib import *
    from sound_master import *
    from game_master import *
except:
    print "cazzo non ha importato bene pappa"

class bullet(pygame.sprite.Sprite):
    """Single bullet class"""
    def __init__(self, color, initial_pos, vector, speed=1, bullet_dimension=K_BULLET_DIMENSION):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface(bullet_dimension)
        # Ruoto l'immagine in modo che sia concorde
        # al vettore direzione
        alpha = math.degrees(angle(vector, (1,0)))
        self.image = pygame.transform.rotate(self.image, alpha) 
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.center = initial_pos
        self.vector = vector
        self.speed = speed
        bullets.add(self)
        
    def update(self):
        offset_x = self.vector[0] * K_BULLET_SPEED * self.speed
        offset_y = self.vector[1] * K_BULLET_SPEED 
        self.rect = self.rect.move(offset_x, offset_y)
        if self.rect[0] > K_WINDOW_DIM[0] or self.rect[0] < 0 or self.rect[1] > K_WINDOW_DIM[1] or self.rect[1] < 0 :
            self.kill()
         
    def kill(self):
        if self in bullets:
            bullets.remove(self)
        else:
            en_bullets.remove(self)
        self = None

class box(pygame.sprite.Sprite):
    """Superclasse di personaggio e nemico"""
    def __init__(self, color, initial_pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface(K_BOX_DIMENSION)
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.center = initial_pos

class enemy_box(box):
    """I nemici quadrati"""
    def __init__(self, color, initial_pos):
        box.__init__(self, color, initial_pos)
        self.color = color
        self.cooldown = K_COOLDOWN * 10 + random.randint(1, 25)
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
            x = bullet( (255,255,255),
                        (self.rect.left, self.rect.centery),
                        (-1,0),
                        0.5)
            en_bullets.add(x)
        else:
            self.cooldown -= 1
    
    def kill(self):
        snd_master.play('enemy_explosion')
        game_m.is_dead(self.__class__.__name__)
        create_explosion_at(self.color, self.rect)
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
            if random.randint(1,10) <= 3:
                self.cooldown = K_COOLDOWN * 5 + random.randint(30, 200)
                x = bullet( (255,255,255),
                            (self.rect.left, self.rect.centery),
                            (-1,0),
                            0.5)
                en_bullets.add(x)
            self.cooldown = K_COOLDOWN * 20 + random.randint(30, 200)
        else:
            self.cooldown -= 1

class player_box(box):
    """L'utente"""
    def __init__(self, color, initial_pos):
        box.__init__(self, color, initial_pos)
        self.direction = [False for _ in range(4)]
        self.weapons = []
        self.color = color
        self.hp = K_HP
    
    def give(self, event=None, rest=None):
        if event.type == KEYDOWN:
            if event.key == K_DOWN:
                self.direction[M_SOUTH] = True
            elif event.key == K_UP:
                self.direction[M_NORTH] = True
            elif event.key == K_LEFT:
                self.direction[M_WEST] = True
            elif event.key == K_RIGHT:
                self.direction[M_EAST] = True
            else:
                for weapon in self.weapons:
                    weapon.give(event)
                
        elif event.type == KEYUP:
            if event.key == K_DOWN:
                self.direction[M_SOUTH] = False
            elif event.key == K_UP:
                self.direction[M_NORTH] = False
            elif event.key == K_LEFT:
                self.direction[M_WEST] = False
            elif event.key == K_RIGHT:
                self.direction[M_EAST] = False
            else:
                for weapon in self.weapons:
                    weapon.give(event)
                
    def update(self):
        if self.direction[M_SOUTH]:
            if not self.rect.bottom >= K_WINDOW_DIM[1] - K_MOV:
                self.rect = self.rect.move(0, K_MOV)
        if self.direction[M_NORTH]:
            if not self.rect.top <= K_MOV:
                self.rect = self.rect.move(0, -K_MOV)
        if self.direction[M_WEST]:
            if not self.rect.left <= K_MOV:
                self.rect = self.rect.move(-K_MOV, 0)
        if self.direction[M_EAST]:
            if not self.rect.right >= K_WINDOW_DIM[0] - K_MOV:
                self.rect = self.rect.move(K_MOV, 0)
        if active_weapons:
            active_weapons[0].update()              
        
    def kill(self):
        self.hp -= 1
        snd_master.play('enemy_explosion')
        if self.hp == 0:
            create_explosion_at(self.color, self.rect)
    
    def add_weapons(self, weapons=None):
        if weapons.__class__.__name__ == 'list':
            for weapon in weapons:
                self.add_weapon(weapon)
        else:
            self.add_weapon(weapons)
            
    def add_weapon(self, weapon):
        weapon.set_father(self)
        self.weapons.append(weapon)
        
    def clear_weapons(self):
        self.weapons = []
        
    def hit_point(self):
        return self.hp
        
class enemy_junkie(pygame.sprite.Sprite):
    """Gli scarti generati dalla morte dei nemici"""
    def __init__(self, color, init_pos, vector):
        pygame.sprite.Sprite.__init__(self) 
        self.image = pygame.Surface(K_JUNK_DIMENSION)
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.center = init_pos
        self.init_pos = init_pos
        self.vector = vector
        self.times = 0
        
    def update(self):
        offset_x = self.vector[0] * K_JUNK_MOV / math.sqrt(( self.vector[0]**2 + self.vector[1]**2))
        offset_y = self.vector[1] * K_JUNK_MOV / math.sqrt(( self.vector[0]**2 + self.vector[1]**2))
        self.rect = self.rect.move(offset_x, offset_y)
        self.times += 1
        if self.times * K_JUNK_MOV >= K_JUNKIE_RADIUS:
            self.kill()
        
    def kill(self):
        junkie.remove(self)
        self = None
    
class base_weapon(pygame.sprite.Sprite):
    """Arma basilare che spara un proiettile alla volta in una direzione"""
    def __init__(self, d_vector, firing_key=K_d, bullet_speed=1, father=None):
        pygame.sprite.Sprite.__init__(self)
        self.cooldown = 0
        self.key = firing_key
        self.direction = d_vector
        self.father = father
        
    def give(self, event, *rest):
        if event.type == KEYDOWN:
            if event.key == self.key:
                active_weapons.append(self)
        elif event.type == KEYUP:
            if event.key == self.key:
                active_weapons.remove(self)
                self.cooldown = 0
                
    def update(self):
        if not self.cooldown:
            self.cooldown = K_COOLDOWN
            x = bullet(((random.randint(1,255)),
                        (random.randint(1,255)),
                        (random.randint(1,255))),
                        (self.father.rect.center),
                         self.direction) 
            snd_master.play('shoot')
            bullets.add(x)
        else:
            self.cooldown -= 1
        
    def set_father(self, father):
        self.father = father
                
class triple_directed_weapon(base_weapon):
    """Arma che spara tre proiettili alla volta, in una sola direzione"""
                
    def update(self):
        if not self.cooldown:
            self.cooldown = K_COOLDOWN
            x = bullet(((random.randint(1,255)),
                        (random.randint(1,255)),
                        (random.randint(1,255))),
                        (self.father.rect.topright),
                         self.direction) 
            x = bullet(((random.randint(1,255)),
                        (random.randint(1,255)),
                        (random.randint(1,255))),
                        ((self.father.rect.right, self.father.rect.centery)),
                         self.direction) 
            x = bullet(((random.randint(1,255)),
                        (random.randint(1,255)),
                        (random.randint(1,255))),
                        (self.father.rect.bottomright),
                         self.direction) 
            snd_master.play('shoot')
            bullets.add(x)
        else:
            self.cooldown -= 1
        
class fan_weapon(base_weapon):
    
    def update(self):
        if not self.cooldown:
            self.cooldown = K_COOLDOWN
            x = bullet(((random.randint(1,255)),
                        (random.randint(1,255)),
                        (random.randint(1,255))),
                        (self.father.rect.topright),
                         self.direction) 
            x = bullet(((random.randint(1,255)),
                        (random.randint(1,255)),
                        (random.randint(1,255))),
                        ((self.father.rect.right, self.father.rect.centery)),
                         self.direction) 
            x = bullet(((random.randint(1,255)),
                        (random.randint(1,255)),
                        (random.randint(1,255))),
                        (self.father.rect.bottomright),
                         self.direction) 
            x = bullet(((random.randint(1,255)),
                        (random.randint(1,255)),
                        (random.randint(1,255))),
                        (self.father.rect.center),
                         (3,1), 0.5)
            x = bullet(((random.randint(1,255)),
                        (random.randint(1,255)),
                        (random.randint(1,255))),
                        (self.father.rect.center),
                         (2,1), 0.7)
            x = bullet(((random.randint(1,255)),
                        (random.randint(1,255)),
                        (random.randint(1,255))),
                        (self.father.rect.center),
                         (3,-1), 0.5) 
            x = bullet(((random.randint(1,255)),
                        (random.randint(1,255)),
                        (random.randint(1,255))),
                        (self.father.rect.center),
                         (2,-1), 0.7)
            snd_master.play('shoot')           
            bullets.add(x)
        else:
            self.cooldown -= 1

class h_weapon(base_weapon):
    def update(self):
        if not self.cooldown:
            self.cooldown = K_COOLDOWN * 3
            x = bullet(((random.randint(1,255)),
                        (random.randint(1,255)),
                        (random.randint(1,255))),
                        (self.father.rect.center),
                         self.direction,
                         0.5,
                         (5,15)) 
            snd_master.play('shoot')
            bullets.add(x)
        else:
            self.cooldown -= 1
    
