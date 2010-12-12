'''
Created on 07/dic/2010

@author: tosh
'''



try:
    import enemies_l
    import pygame
    from pygame.locals import *
    import random
    import math
    import useful_lib
    from killdashape_k import *
    import elements
    from global_vars import *
    from sound_master import *
    from game_master import *
    import goodies
    import os
    import platform
except:
    print "cazzo non ha importato bene"
   
def main(): 
    
    def print_things():
        init_back_rect.right -= 3
        if init_back_rect.right <= 0:
            init_back_rect.right = K_WINDOW_DIM[0]
        screen.blit(background, [init_back_rect.left,0])
        screen.blit(background, [init_back_rect.right,0])
        rectlist = landscape.draw(screen)
        rectlist += g_goodies.draw(screen)
        rectlist += back_elements.draw(screen)
        rectlist += player.draw(screen)
        rectlist += bullets.draw(screen)
        rectlist += enemies.draw(screen)
        rectlist += junkie.draw(screen)
        rectlist += en_bullets.draw(screen)
        rectlist += gds.draw(screen)
            
        pygame.display.update(rectlist)
        if not platform.system() == 'Darwin':
            pygame.display.update()
        
    
    pygame.init()  
    END = False
    died = False
    
    
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode(K_WINDOW_DIM)#, pygame.FULLSCREEN)
    pygame.display.set_caption("killdashape")
    #background = pygame.Surface(K_WINDOW_DIM)
    background = pygame.image.load('../img/background.png').convert()
    init_back_rect = background.get_rect()
    b = elements.player_box([255, 0, 0], 
                            [K_BOX_DIMENSION[0]/2, K_WINDOW_DIM[1]/2])
    player.add(b)
    useful_lib.init_stats()
    useful_lib.init_landscape()
    graphic_goodies.cloud()
    game_m.add_player(b)
    game_m.set_fan_weapon()
    #game_m.add_enemy()
    
    while not END:
        if not game_m.is_paused():
            clock.tick(K_TICK)
            for e in pygame.event.get():
                if e.type == QUIT:
                    END = True
                elif e.type == KEYDOWN and e.key in M_PAUSE:
                    game_m.pause()
                else:
                    b.give(e)
            landscape.update()
            b.update()
            bullets.update()
            enemies.update()
            junkie.update()
            en_bullets.update()
            g_goodies.update()
            back_elements.update()
            gds.update()
            
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
            
            land_collided = pygame.sprite.spritecollide(b, landscape, 0)
            if land_collided != []:
                b.kill()
                if b.hit_point() == 0:
                    died = True
                    END = True
            
            pygame.sprite.spritecollide(b, gds, 1)
                   
            pygame.sprite.groupcollide(bullets, en_bullets, 0, 1)
            pygame.sprite.groupcollide(bullets, enemies, 1, 1)
            

            print_things()
            game_m.act()
            
            if died:
                player.remove(b)
                for _ in range(30):
                    clock.tick(K_TICK)
                    bullets.update()
                    landscape.update()
                    enemies.update()
                    junkie.update()
                    en_bullets.update()
                    g_goodies.update()
                    print_things()
        else:
            for e in pygame.event.get():
                if e.type == QUIT:
                    END = True
                elif e.type == KEYDOWN and e.key in M_EXIT:
                    END = True
                elif e.type == KEYDOWN and e.key in M_PAUSE:
                    game_m.pause()
            g_goodies.update()
            print_things()
        
    

if __name__ == '__main__':
    main()
        
    