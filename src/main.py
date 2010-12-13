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
except Exception, message:
    print "cazzo non ha importato bene sad a", message
   
def main(): 
    
    def print_things():
        init_back_rect.right -= 3
        if init_back_rect.right <= 0:
            init_back_rect.right = K_WINDOW_DIM[0]
        screen.blit(background, [init_back_rect.left,0])
        screen.blit(background, [init_back_rect.right,0])
        rectlist = lndscp_back.draw(screen)
        rectlist +=lndscp_front.draw(screen)
        rectlist += g_goodies.draw(screen)
        rectlist += back_elements.draw(screen)
        rectlist += player.draw(screen)
        rectlist += bullets.draw(screen)
        rectlist += enemies.draw(screen)
        rectlist += junkie.draw(screen)
        rectlist += en_bullets.draw(screen)
        rectlist += gds.draw(screen)
            
        pygame.display.update(rectlist)
        #if not platform.system() == 'Darwin':
        pygame.display.update()
        
    
    pygame.init()  
    END = False
    IMMEDIATE = False
    n_player = 1
    player_dead = [True for _ in range(4)]    
    
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode(K_WINDOW_DIM)
    pygame.display.set_caption("killdashape")
    #background = pygame.Surface(K_WINDOW_DIM)
    background = pygame.image.load(IMG_PATH + 'background.png').convert()
    init_back_rect = background.get_rect()        
    
    for i in range(n_player):
        player_dead[i] = False
        a = elements.player_box(K_PLAYER_COLOR[i], 
                                [K_BOX_DIMENSION[0]/2, K_WINDOW_DIM[1]/2 + 15*((-1)**i)*(i+1)], i+1)
        player.add(a)
        game_m.add_player(a)
        game_m.set_fan_weapon(a)
    
    useful_lib.init_stats()
    useful_lib.init_landscape()
    
    while not END:
        if not game_m.is_paused():
            clock.tick(K_TICK)
            for e in pygame.event.get():
                if e.type == QUIT:
                    END = True
                    IMMEDIATE = True
                elif e.type == KEYDOWN and e.key in M_PAUSE:
                    game_m.pause()
                else:
                    already_used = False
                    for p in player:
                        if not already_used:
                            already_used = p.give(e)
            lndscp_back.update()
            lndscp_front.update()
            player.update()
            bullets.update()
            enemies.update()
            junkie.update()
            en_bullets.update()
            g_goodies.update()
            back_elements.update()
            gds.update()
            
            for p in player:
                en_collided = pygame.sprite.spritecollide(p, enemies, 0)
                if en_collided != []:
                    p.kill()
                    for enem in en_collided:
                        enem.kill()
                    if p.hit_point() == 0:
                        if len(player) == 0:
                            END = True
                bull_collided = pygame.sprite.spritecollide(p, en_bullets, 0)
                if bull_collided != []:
                    p.kill()
                    for bull in bull_collided:
                        bull.kill()
                    if p.hit_point() == 0:
                        if len(player) == 0:
                            END = True
                land_collided = pygame.sprite.spritecollide(p, lndscp_back, 0)
                if land_collided != []:
                    for element in land_collided:
                        if element.hurts():
                            while p.hit_point() > 0:
                                p.kill()
                                if len(player) == 0:
                                    END = True
                gds_collided = pygame.sprite.spritecollide(p, gds, 0)
                if gds_collided != []:
                    for element in gds_collided:
                        element.kill(p)
                
                   
            pygame.sprite.groupcollide(bullets, en_bullets, 0, 1)
            pygame.sprite.groupcollide(bullets, enemies, 1, 1)
            

            print_things()
            game_m.act()

        else:
            for e in pygame.event.get():
                if e.type == QUIT:
                    END = True
                    IMMEDIATE = True
                elif e.type == KEYDOWN and e.key in M_EXIT:
                    END = True
                    IMMEDIATE = True
                elif e.type == KEYDOWN and e.key in M_PAUSE:
                    game_m.pause()
            g_goodies.update() # Per stampare 'pausa'
         
    if not IMMEDIATE:   
        for _ in range(30):
                        clock.tick(K_TICK)
                        bullets.update()
                        lndscp_back.update()
                        lndscp_front.update()
                        enemies.update()
                        junkie.update()
                        en_bullets.update()
                        g_goodies.update()
                        print_things()
            
    

if __name__ == '__main__':
    main()
        
    