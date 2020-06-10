import os
from json import load
import pygame

import scenes.game.functions
import scenes.game.objects


def main():
    pygame.init()

    base_dir = os.path.dirname(os.path.abspath(__file__))

    with open(f'{base_dir}/config/config.json', 'r') as file:
        config = load(file)

    screen = pygame.display.set_mode(config['mode'])
    pygame.display.set_caption(config['caption'])

    clock = pygame.time.Clock()

    tick = 0

    # Scenes init
    bg, plate = scenes.game.functions.init(screen, base_dir)


    while True:
        tick += 1

        if config['location'] == 'game':
            scenes.game.functions.update(screen, bg, plate, tick)
            scenes.game.functions.check_events(config, plate)



        if tick >= config['FPS']:
            tick = 0

        pygame.display.update()
        clock.tick(config['FPS'])


if __name__ == '__main__':
    main()