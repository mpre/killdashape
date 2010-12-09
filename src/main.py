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
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode(K_WINDOW_DIM)
    pygame.display.set_caption("killdashape")
    background = pygame.Surface(K_WINDOW_DIM)
    b = elements.player_box([255, 0, 0], 
                   [0, 0])
    game_m.add_player(b)
    game_m.set_triple_weapon()
    game_m.add_enemy()
    
    while not END:
        clock.tick(45)
        for e in pygame.event.get():
            if e.type == QUIT:
                END = True
            else:
                b.give(e)
        b.update()
        bullets.update()
        enemies.update()
        junkie.update()
        en_bullets.update()
        if pygame.sprite.spritecollide(b, enemies, 0) != []:
            b.die()
            END = True
        if pygame.sprite.spritecollide(b, en_bullets, 0) != []:
            b.die()
            END = True
        pygame.sprite.groupcollide(bullets, en_bullets, 0, 1)
        pygame.sprite.groupcollide(bullets, enemies, 1, 1)
        screen.blit(background, [0,0])
        screen.blit(b.image, b.rect)
        rectlist = bullets.draw(screen)
        rectlist += enemies.draw(screen)
        rectlist += junkie.draw(screen)
        rectlist += en_bullets.draw(screen)
        pygame.display.update(rectlist)
        pygame.display.update()

if __name__ == '__main__':
    main()
        
    