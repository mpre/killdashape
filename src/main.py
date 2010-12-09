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
    from elements import *
    from global_vars import *
    from sound_master import *
except:
    print "cazzo non ha importato bene pippo"
   

def main():
    pygame.init()    
    END = False
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode(K_WINDOW_DIM)
    pygame.display.set_caption("killdashape")
    background = pygame.Surface(K_WINDOW_DIM)
    b = player_box([255, 0, 0], 
                   [0, 0])
    b.add_weapons((base_weapon((1,0), K_d),
                   base_weapon((0,1), K_s),
                   base_weapon((0,-1), K_a),
                   base_weapon((-1,0), K_w)))
    b.add_weapon((triple_directed_weapon((1,0), K_z)))
    for _ in range(30):
        en = enemy_box([random.randint(1,255),
                        random.randint(1,255),
                        random.randint(1,255)],                       
                       [random.randint(30,640 - K_BOX_DIMENSION[0]),
                        random.randint(30,320 - K_BOX_DIMENSION[1])])
        enemies.add(en)
    
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
        if pygame.sprite.spritecollide(b, enemies, 0) != []:
            b.die()
            END = True
        pygame.sprite.groupcollide(bullets, enemies, 1, 1)
        screen.blit(background, [0,0])
        screen.blit(b.image, b.rect)
        rectlist = bullets.draw(screen)
        rectlist += enemies.draw(screen)
        rectlist += junkie.draw(screen)
        pygame.display.update(rectlist)
        pygame.display.update()

if __name__ == '__main__':
    main()
        
    