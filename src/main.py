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
        if not platform.system() == 'Darwin':
            pygame.display.update()
        
    
    pygame.init()  
    END = False
    a_died = False
    b_died = True
    two_players = False
    
    
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode(K_WINDOW_DIM)#, pygame.FULLSCREEN)
    pygame.display.set_caption("killdashape")
    #background = pygame.Surface(K_WINDOW_DIM)
    background = pygame.image.load(IMG_PATH + 'background.png').convert()
    init_back_rect = background.get_rect()
    
    a = elements.player_box(K_P1_COLOR, 
                            [K_BOX_DIMENSION[0]/2, K_WINDOW_DIM[1]/2])
    player.add(a)
    
    if two_players:
        b_died = False
        b = elements.player_box(K_P2_COLOR,
                                [K_BOX_DIMENSION[0]/2, K_WINDOW_DIM[1]/2], 2)
        player.add(b)
        
    
    useful_lib.init_stats()
    useful_lib.init_landscape()
    
    game_m.add_player(a)
    game_m.set_fan_weapon(0)
    if two_players:
        game_m.add_player(b)
        game_m.set_fan_weapon(1)
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
                    a.give(e)
                    if two_players:
                        b.give(e)
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
            
            if not a_died:
                en_collided = pygame.sprite.spritecollide(a, enemies, 0)
                if en_collided != []:
                    a.kill()
                    for enem in en_collided:
                        enem.kill()
                    if a.hit_point() == 0:
                        a_died = True
                        END = b_died and a_died
                
                bull_collided = pygame.sprite.spritecollide(a, en_bullets, 0)
                if  bull_collided != []:
                    a.kill()
                    for bull in bull_collided:
                        bull.kill()
                    if a.hit_point() == 0:
                        a_died = True
                        END = b_died and a_died
                
                land_collided = pygame.sprite.spritecollide(a, lndscp_back, 0)
                if land_collided != []:
                    for element in land_collided:
                        if element.hurts() and a:
                            a.kill()
                            if a.hit_point() == 0:
                                a_died = True
                                END = b_died and a_died
                
                gds_collided = pygame.sprite.spritecollide(a, gds, 0)
                if gds_collided != []:
                    for element in gds_collided:
                        element.kill(0)
                  
            if two_players and not b_died:  
                en_collided = pygame.sprite.spritecollide(b, enemies, 0)
                if en_collided != []:
                    b.kill()
                    for enem in en_collided:
                        enem.kill()
                    if b.hit_point() == 0:
                        b_died = True
                        END = b_died and a_died
                
                bull_collided = pygame.sprite.spritecollide(b, en_bullets, 0)
                if  bull_collided != []:
                    b.kill()
                    for bull in bull_collided:
                        bull.kill()
                    if b.hit_point() == 0:
                        b_died = True
                        END = b_died and a_died
                
                land_collided = pygame.sprite.spritecollide(b, lndscp_back, 0)
                if land_collided != []:
                    for element in land_collided:
                        if element.hurts() and a:
                            b.kill()
                            if b.hit_point() == 0:
                                b_died = True
                                END = b_died and a_died
                
                gds_collided = pygame.sprite.spritecollide(b, gds, 0)
                if gds_collided != []:
                    for element in gds_collided:
                        element.kill(1)
                   
            pygame.sprite.groupcollide(bullets, en_bullets, 0, 1)
            pygame.sprite.groupcollide(bullets, enemies, 1, 1)
            

            print_things()
            game_m.act()
            
            if a_died and b_died:
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
            elif a_died:
                player.remove(a)
            elif b_died and two_players:
                player.remove(b)
        else:
            for e in pygame.event.get():
                if e.type == QUIT:
                    END = True
                elif e.type == KEYDOWN and e.key in M_EXIT:
                    END = True
                elif e.type == KEYDOWN and e.key in M_PAUSE:
                    game_m.pause()
            g_goodies.update() # Per stampare 'pausa'
        
    

if __name__ == '__main__':
    main()
        
    