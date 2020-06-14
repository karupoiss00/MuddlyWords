import pygame
from sys import exit

from .objects import *


def init(screen, base_dir, config):
    play = PlayButton(screen, base_dir, config)
    table = TableButton(screen, base_dir, config)
    settings = SettingsButton(screen, base_dir, config)
    caption = Caption(screen, base_dir)

    return play, table, settings, caption


def check_events(config, base_dir, play, table, back, settings):
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            exit()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()

            if play._rect.collidepoint((x, y)):
                print('click play!')
                play.change_scene = True
                play.to_top = True
                table.to_bottom = True
                settings.to_bottom = True

            elif table._rect.collidepoint((x, y)):
                print('click table!')
                play.to_top = True
                table.change_scene = True
                table.to_bottom = True
                back.to_top = True
                settings.to_bottom = True

            elif settings._rect.collidepoint((x, y)):
                print('click settings!')
                play.to_top = True
                table.to_bottom = True
                back.to_top = True
                settings.to_bottom = True
                settings.change_scene = True



def update(bg, play, table, settings, caption):
    bg.blit()

    play.update()
    play.blit()
    
    table.update()
    table.blit()

    settings.update()
    settings.blit()

    caption.blit()
