import pygame
from sys import exit

from .objects import *


def init(screen, base_dir, config):
    effects = EffectsButton(screen, base_dir, config)
    full_screen = FullScreenButton(screen, base_dir, config)
    nick = NickInput(screen, base_dir, config)

    return effects, full_screen, nick


def check_events(back, play, table, settings, effects, full_screen, nick):
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            exit()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()

            if back._rect.collidepoint((x, y)):
                print('click back!')
                back.change_scene = True
                back.to_bottom = True
                play.to_bottom = True
                table.to_top = True
                settings.to_top = True

            elif effects._rect.collidepoint((x, y)):
                print('click effects!')
                effects.config['user']['effects'] = not effects.config['user']['effects']
                effects.is_save = True

            elif full_screen._rect.collidepoint((x, y)):
                print('click full screen!')
                full_screen.config['user']['full_screen'] = not full_screen.config['user']['full_screen']
                full_screen.is_save = True

            if nick._rect.collidepoint((x, y)):
                print('click nick!')
                nick.is_enable = True
            else:
                nick.is_enable = False

        elif event.type == pygame.KEYDOWN and nick.is_enable:
            if event.key == pygame.K_BACKSPACE:
                nick.config['user']['nick'] = nick.config['user']['nick'][:len(nick.config['user']['nick']) - 1]
            else:
                nick.config['user']['nick'] += event.unicode
            
            nick.save()


def update(bg, config, back, settings, nick):
    bg.blit()

    back.update()
    back.blit()

    width = 63
    space = 7

    x = (config['mode'][0] - (len(settings) * width + (len(settings) - 1) * space)) // 2

    for button in settings.sprites():
        button.rect.x = x
        button.update()
        button.blit()
        x += width + space

    nick.update()
    nick.blit()