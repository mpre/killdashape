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
    import game_master
    from global_vars import *
except Exception, message:
    print "cazzo non ha importato bene in elements:",message

class bullet(pygame.sprite.Sprite):
    """Single bullet class"""
    def __init__(self, color, initial_pos, vector, speed=1, 
                 bullet_dimension=K_BULLET_DIMENSION, father=None):
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
        self.father = father
        #bullets.add(self)
        
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
    
    def get_father(self):
        return self.father
        
class v_bullet(bullet):
    """Vertical bullet, non distruttibile"""
    def __init__(self, color, initial_pos, vector, speed=1, father=None):
        bullet.__init__(self, color, initial_pos, vector, speed, (7,K_WINDOW_DIM[1]/2), father)
        
    def update(self):
        offset_x = self.vector[0] * K_BULLET_SPEED * self.speed
        self.rect = self.rect.move(offset_x, 0)
        if self.rect[0] > K_WINDOW_DIM[0] or self.rect[0] < 0:
            self.kill()
        
    def kill(self):
        if self.rect[0] > K_WINDOW_DIM[0] or self.rect[0] < 0:
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

class player_box(box):
    """L'utente"""
    def __init__(self, color, initial_pos, nplayer=1, img_size=K_PLAYER_IMG_SIZE):
        box.__init__(self, color, initial_pos)
        self.direction = [False for _ in range(4)]
        self.weapons = pygame.sprite.GroupSingle()
        self.color = color
        self.hp = K_HP
        self.nplayer = nplayer - 1 #player_number
        self.baloon = graphic_goodies.baloon((str(nplayer)+'P', str(nplayer)+'P'), 
                                             self, 10, FONT_PATH + "bitlow.ttf", 
                                             (0,0,0), (255,255,255), False)
        self.col = 0
        self.row = 0
        self.img_size = [x/K_PLAYER_IMAGE_FACTOR for x in img_size]
        self.img_ss = pygame.image.load(IMG_PATH + 'elicopter' + str(nplayer) + '.png').convert()
        self.img_ss = pygame.transform.scale(self.img_ss, [x/K_PLAYER_IMAGE_FACTOR for x in self.img_ss.get_size()])
        self.ss_rect = (0,0,self.img_size[0],self.img_size[1])
        self.image = pygame.Surface(self.img_size)
        self.image.blit(self.img_ss, (0,0), self.ss_rect)
        self.image.set_colorkey(self.image.get_at((1,1)))
        #self.image = pygame.transform.scale(self.image, (34,21))
        self.rect = self.image.get_rect()
        #self.rect.bottomright = (-1, K_WINDOW_DIM[1] - 7)
        self.rect.center = initial_pos
        self.cooldown_img = 3
    
    def give(self, event=None, rest=None):
        done = True
        if event.type == KEYDOWN:
            if event.key in M_DOWN[self.nplayer]:
                self.direction[M_SOUTH] = True
            elif event.key in M_UP[self.nplayer]:
                self.direction[M_NORTH] = True
            elif event.key in M_LEFT[self.nplayer]:
                self.direction[M_WEST] = True
            elif event.key in M_RIGHT[self.nplayer]:
                self.direction[M_EAST] = True
            elif event.key in M_WEAPON_SHOOT[self.nplayer]:
                for weapon in self.weapons:
                    weapon.give(event)
            else:
                done = False
                print 'unrecognized:'+str(event)
                
        elif event.type == KEYUP:
            if event.key in M_DOWN[self.nplayer]:
                self.direction[M_SOUTH] = False
            elif event.key in M_UP[self.nplayer]:
                self.direction[M_NORTH] = False
            elif event.key in M_LEFT[self.nplayer]:
                self.direction[M_WEST] = False
            elif event.key in M_RIGHT[self.nplayer]:
                self.direction[M_EAST] = False
            elif event.key in M_WEAPON_SHOOT[self.nplayer]:
                for weapon in self.weapons:
                    weapon.give(event)
            else:
                done = False
                print 'unrecognized:'+str(event)
        return done
                
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
        if not self.cooldown_img:
            self.cooldown_img = 3
            self.col += 1
            self.col %= 5
            self.row += self.col % 5
            self.row %= 6
            self.ss_rect = (self.img_size[0]*self.col,
                            self.img_size[1]*self.row,
                            self.img_size[0]*(self.col+1),
                            self.img_size[1]*(self.row+1))
            self.image = pygame.Surface(self.img_size)
            self.image.blit(self.img_ss, (0,0), self.ss_rect)
            #self.image = pygame.transform.scale(self.image, (34,21))
            self.image.set_colorkey(self.image.get_at((1,1)))
        else:
            self.cooldown_img -= 1
        self.weapons.update()             
        
    def kill(self):
        self.hp -= 1
        snd_master.play('enemy_explosion')
        if self.hp == 0:
            create_explosion_at(self.color, self.rect)
            g_goodies.remove(self.baloon)
            player.remove(self)
            useful_lib.clear_goodies()
            useful_lib.restart_pl_goodies()
    
    def add_weapons(self, weapons=None):
        if weapons.__class__.__name__ == 'list':
            for weapon in weapons:
                self.add_weapon(weapon)
        else:
            self.add_weapon(weapons)
            
    def add_weapon(self, weapon):
        weapon.set_father(self)
        weapon.set_key(M_WEAPON_SHOOT[self.nplayer])
        self.weapons.add(weapon)
        
    def clear_weapons(self):
        self.weapons = pygame.sprite.GroupSingle()
            
    def hit_point(self):
        return self.hp
    
    def ammo(self):
        return self.weapons.sprite.get_ammo()
    
    def get_weapon(self):
        return self.weapons.sprite.get_name()
    
    def get_p_number(self):
        return self.nplayer
        
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
        junkie.add(self)
        
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
    

    
