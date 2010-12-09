'''
Created on 07/dic/2010

@author: tosh
'''

try:
    import pygame
    from pygame.locals import *
    import random
    import math
    from killdashape_k import *
    import elements
    from global_vars import *
    from sound_master import *
    from game_master import *
except:
    print "cazzo non ha importato bene"
   
def main():
    pygame.init()    
    END = False
    died = False
    paused = False
    
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode(K_WINDOW_DIM)
    pygame.display.set_caption("killdashape")
    background = pygame.Surface(K_WINDOW_DIM)
    b = elements.player_box([255, 0, 0], 
                            [K_BOX_DIMENSION[0]/2, K_WINDOW_DIM[1]/2])
    game_m.add_player(b)
    game_m.set_fan_weapon()
    #game_m.add_enemy()
    
    while not END:
        if not paused:
            clock.tick(K_TICK)
            for e in pygame.event.get():
                if e.type == QUIT:
                    END = True
                elif e.type == KEYDOWN and e.key == K_SPACE:
                    paused = True
                else:
                    b.give(e)
            b.update()
            bullets.update()
            enemies.update()
            junkie.update()
            en_bullets.update()
            en_collided = pygame.sprite.spritecollide(b, enemies, 0)
            if en_collided != []:
                b.kill()
                for enem in en_collided:
                    enem.kill()
                if b.hit_point() == 0:
                    died = True
                    END = True
            
            bull_collided = pygame.sprite.spritecollide(b, en_bullets, 0)
            if  bull_collided != []:
                b.kill()
                for bull in bull_collided:
                    bull.kill()
                if b.hit_point() == 0:
                    died = True
                    END = True
                
            point_f = pygame.font.Font(None, 20)
            point_i = point_f.render('{0} : {1}'.format('Points',game_m.get_points()), 
                                     True, K_FONT_COLOR)
            point_r = point_i.get_rect()
            point_r.topleft = (10, 3)
            
            hp_f = pygame.font.Font(None, 20)
            hp_i = hp_f.render('{0} : {1}'.format('HP',b.hit_point()), 
                                     True, K_FONT_COLOR)
            hp_r = hp_i.get_rect()
            hp_r.topleft = (K_WINDOW_DIM[0]-50, 3)
            
            level_f = pygame.font.Font(None, 20)
            level_i = level_f.render('{0} : {1}'.format('LEVEL', game_m.get_level()), 
                                     True, K_FONT_COLOR)
            level_r = level_i.get_rect()
            level_r.top = 3
            level_r.centerx = K_WINDOW_DIM[0]/2
            
            pygame.sprite.groupcollide(bullets, en_bullets, 0, 1)
            pygame.sprite.groupcollide(bullets, enemies, 1, 1)
            screen.blit(background, [0,0])
            screen.blit(b.image, b.rect)
            screen.blit(point_i, point_r)
            screen.blit(hp_i, hp_r)
            screen.blit(level_i, level_r)
            rectlist = bullets.draw(screen)
            rectlist += enemies.draw(screen)
            rectlist += junkie.draw(screen)
            rectlist += en_bullets.draw(screen)
            pygame.display.update(rectlist)
            pygame.display.update()
            game_m.act()
            
            if died:
                for _ in range(30):
                    clock.tick(K_TICK)
                    bullets.update()
                    enemies.update()
                    junkie.update()
                    en_bullets.update()
                    screen.blit(background, [0,0])
                    rectlist = bullets.draw(screen)
                    rectlist += enemies.draw(screen)
                    rectlist += junkie.draw(screen)
                    rectlist += en_bullets.draw(screen)
                    pygame.display.update(rectlist)
                    pygame.display.update()
        else:
            for e in pygame.event.get():
                if e.type == QUIT:
                    END = True
                elif e.type == KEYDOWN and e.key == K_SPACE:
                    paused = False
            

if __name__ == '__main__':
    main()
        
    