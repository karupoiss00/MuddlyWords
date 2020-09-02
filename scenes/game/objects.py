import pygame
import sys
sys.path.append('../../')
from random import randint
from mixins import BoostMixin, CaptionMixin, ButtonMixin


pygame.font.init()


class Background:
    def __init__(self, screen, base_dir, x, y):
        self.screen = screen

        self.bg = pygame.image.load(f'{base_dir}/assets/images/bg/background.bmp')
        self.rect = self.bg.get_rect()

        self.rect.x = x
        self.rect.y = y

    def update(self):
        self.rect.x -= 1

        if self.rect.x <= -840:
            self.rect.x = 0

    def blit(self):
        self.screen.blit(self.bg, self.rect)


class SpacePlate(pygame.sprite.Sprite):
    def __init__(self, screen, base_dir, config):
        super().__init__()

        self.screen = screen
        self.screen_rect = self.screen.get_rect()

        self.config = config

        self.imgs = [[pygame.image.load(f'{base_dir}/assets/images/plate/blue_idle.bmp'),
                      pygame.image.load(f'{base_dir}/assets/images/plate/blue_fly.bmp')],
                     [pygame.image.load(f'{base_dir}/assets/images/plate/pink_idle.bmp'),
                      pygame.image.load(f'{base_dir}/assets/images/plate/pink_fly.bmp')],
                     [pygame.image.load(f'{base_dir}/assets/images/plate/green_idle.bmp'),
                      pygame.image.load(f'{base_dir}/assets/images/plate/green_fly.bmp')]]

        self.img = self.imgs[self.config['user']['color']][0]
        self.rect = self.img.get_rect()

        self.rect.x = 5
        self.rect.centery = self.screen_rect.centery

        self.gravity = 7

        self.is_jump = False
        self.jump = 10
        self.sounds = {'jump': f'{base_dir}/assets/sounds/jump.wav',
                       'bang': f'{base_dir}/assets/sounds/bang.wav',
                       'score': f'{base_dir}/assets/sounds/score.wav'}

    def reset(self):
        self.img = self.imgs[self.config['user']['color']][0]
        self.rect.centery = self.screen_rect.centery
        self.is_jump = False
        self.jump = 10

    def update(self):
        if self.img not in self.imgs[self.config['user']['color']]:
            self.img = self.imgs[self.config['user']['color']][0]

        if not self.is_jump:
            self.rect.y += self.gravity
        else:     

            if self.jump >= -5:
                if self.jump < 0:
                    self.rect.y += (self.jump ** 2) // 3
                else:
                    self.img = self.imgs[self.config['user']['color']][1]
                    self.rect.y -= (self.jump ** 2) // 3
                self.jump -= 1
            else:
                self.img = self.imgs[self.config['user']['color']][0]
                self.is_jump = False
                self.jump = 10

    def blit(self):
        self.screen.blit(self.img, self.rect)


class Asrteroid(pygame.sprite.Sprite):
    def __init__(self, screen, base_dir, config):
        super().__init__()

        self.name = 'simple'

        self.screen = screen
        self.screen_rect = self.screen.get_rect()

        self.config = config

        self.img_idle = pygame.image.load(f'{base_dir}/assets/images/asteroid/idle.bmp')
        self.img = self.img_idle

        self.rect = self.img.get_rect()
        self.rect.y = randint(1, config['mode'][1] - 56)
        self.rect.left = self.screen_rect.right

    def blit(self):
        self.screen.blit(self.img, self.rect)

    def update(self):
        self.rect.x -= self.config['speed']


class FlyingAsrteroid(pygame.sprite.Sprite):
    def __init__(self, screen, base_dir, config):
        super().__init__()

        self.name = 'flying'

        self.screen = screen
        self.screen_rect = self.screen.get_rect()

        self.config = config

        self.imgs = [pygame.image.load(f'{base_dir}/assets/images/asteroid/red_idle.bmp'),
                     pygame.image.load(f'{base_dir}/assets/images/asteroid/blue_idle.bmp')]

        self.img = self.imgs[randint(0, 1)]

        self.rect = self.img.get_rect()
        self.rect.bottom = self.screen_rect.top
        self.rect.left = self.screen_rect.right

    def blit(self):
        self.screen.blit(self.img, self.rect)

    def update(self):
        self.rect.x -= self.config['speed'] * 1.5
        self.rect.y += self.config['speed']



class TimeBoost(BoostMixin, pygame.sprite.Sprite):
    def __init__(self, screen, base_dir, config, y):
        pygame.sprite.Sprite.__init__(self)

        self.name = 'time'

        self.screen = screen
        self.screen_rect = self.screen.get_rect()

        self.config = config

        self.speed = 2

        self.img_idle = pygame.image.load(f'{base_dir}/assets/images/boosts/time_idle.bmp')
        self.img = self.img_idle

        self.img_small = pygame.image.load(f'{base_dir}/assets/images/boosts/time_small.bmp')
        self.img_3 = self.img_small

        self.rect = self.img.get_rect()
        self.rect.y = y
        self.rect.left = self.screen_rect.right

        self.rect_3 = self.img_3.get_rect()
        self.rect_3.top = self.screen_rect.top + 2
        self.rect_3.left = self.screen_rect.left + 2

        BoostMixin.__init__(self, base_dir, config)

    def update(self):
        self._update()

    def blit(self):
        self._blit()


class DoubleBoost(BoostMixin, pygame.sprite.Sprite):
    def __init__(self, screen, base_dir, config, y):
        pygame.sprite.Sprite.__init__(self)

        self.name = 'double'

        self.screen = screen
        self.screen_rect = self.screen.get_rect()

        self.img_idle = pygame.image.load(f'{base_dir}/assets/images/boosts/double_idle.bmp')
        self.img = self.img_idle

        self.img_small = pygame.image.load(f'{base_dir}/assets/images/boosts/double_small.bmp')
        self.img_3 = self.img_small

        self.rect = self.img.get_rect()
        self.rect.y = y
        self.rect.left = self.screen_rect.right

        self.rect_3 = self.img_3.get_rect()
        self.rect_3.top = self.screen_rect.top + 2
        self.rect_3.left = self.screen_rect.left + 2

        BoostMixin.__init__(self, base_dir, config)

    def update(self):
        self._update()

    def blit(self):
        self._blit()


class ShieldBoost(BoostMixin, pygame.sprite.Sprite):
    def __init__(self, screen, base_dir, config, plate, y):
        pygame.sprite.Sprite.__init__(self)

        self.name = 'shield'

        self.screen = screen
        self.screen_rect = self.screen.get_rect()

        self.plate = plate

        self.img_idle = pygame.image.load(f'{base_dir}/assets/images/boosts/shield_idle.bmp')
        self.img = self.img_idle

        self.img_small = pygame.image.load(f'{base_dir}/assets/images/boosts/shield_small.bmp')
        self.img_3 = self.img_small

        self.img_activate = pygame.image.load(f'{base_dir}/assets/images/boosts/shield_activate.bmp')
        self.img_4 = self.img_activate

        self.rect = self.img.get_rect()
        self.rect.y = y
        self.rect.left = self.screen_rect.right

        self.rect_3 = self.img_3.get_rect()
        self.rect_3.top = self.screen_rect.top + 2
        self.rect_3.left = self.screen_rect.left + 2

        self.rect_4 = self.img_4.get_rect()

        BoostMixin.__init__(self, base_dir, config)

    def update(self):
        self._update()

        if self.is_active:
            self.rect_4.center = self.plate.rect.center

    def blit(self):
        self._blit()

        if self.is_active:
            self.screen.blit(self.img_4, self.rect_4)


class Score:
    def __init__(self, screen, base_dir, msg):
        self.screen = screen
        self.screen_rect = self.screen.get_rect()

        self.msg = msg
        self.color = (255, 255, 255)
        self.font = pygame.font.Font(f'{base_dir}/assets/fonts/pixeboy.ttf', 22)

        self.img = self.font.render(self.msg, True, self.color)
        self.rect = self.img.get_rect()

        self.rect.top = self.screen_rect.top + 2
        self.rect.right = self.screen_rect.right - 2

    def update(self):
        self.img = self.font.render(self.msg, True, self.color)
        self.rect = self.img.get_rect()

        self.rect.top = self.screen_rect.top + 2
        self.rect.right = self.screen_rect.right - 2

    def blit(self):
        self.screen.blit(self.img, self.rect)


class End(CaptionMixin):
    def __init__(self, screen, base_dir, config):
        CaptionMixin.__init__(self, base_dir, config, "Your score: {[0]}", ['self.config["score"]'])

        self.screen = screen
        self.screen_rect = self.screen.get_rect()

        self._screen = pygame.Surface((self.config['mode']), pygame.SRCALPHA)

        self._rect = pygame.Rect(0, 0, self.config['mode'][0], self.config['mode'][1])
        self._rect.x = 0
        self._rect.y = 0

        self.buttons = pygame.sprite.Group()
        self.buttons.add(LobbyButton(screen, base_dir))
        self.buttons.add(AgainButton(screen, base_dir))

    def update(self):
        self._update()

        self.rect.centerx = self.screen_rect.centerx
        self.rect.y = 125

        width = 63
        space = 7
        x = (self.config['mode'][0] - (len(self.buttons) * width + (len(self.buttons) - 1) * space)) // 2
        
        for button in self.buttons.sprites():
            button.rect.x = x
            button.update()
            x += width + space

    def blit(self):
        self.screen.blit(self._screen, self._rect)
        self._screen.fill((0, 0, 0, 0))
        self._blit()

        for button in self.buttons.sprites(): button.blit()


class LobbyButton(ButtonMixin, pygame.sprite.Sprite):
    def __init__(self, screen, base_dir):
        pygame.sprite.Sprite.__init__(self)

        self.width = self.height = 63

        self.img = pygame.image.load(f'{base_dir}/assets/images/buttons/lobby.bmp')

        ButtonMixin.__init__(self, screen, base_dir, [], False)


class AgainButton(ButtonMixin, pygame.sprite.Sprite):
    def __init__(self, screen, base_dir):
        pygame.sprite.Sprite.__init__(self)

        self.width = self.height = 63

        self.img = pygame.image.load(f'{base_dir}/assets/images/buttons/again.bmp')

        ButtonMixin.__init__(self, screen, base_dir, [], False)


class Pause(CaptionMixin):
    def __init__(self, screen, base_dir, config):
        CaptionMixin.__init__(self, base_dir, config, 'Pause')

        self.screen = screen
        self.screen_rect = self.screen.get_rect()

        self.rect.centerx = self.screen_rect.centerx
        self.rect.y = 125

        self._screen = pygame.Surface((self.config['mode']), pygame.SRCALPHA)

        self._rect = pygame.Rect(0, 0, self.config['mode'][0], self.config['mode'][1])
        self._rect.x = 0
        self._rect.y = 0

        self.buttons = pygame.sprite.Group()
        self.buttons.add(LobbyButton(screen, base_dir))
        self.buttons.add(ResumeButton(screen, base_dir))

    def update(self):
        width = 63
        space = 7
        x = (self.config['mode'][0] - (len(self.buttons) * width + (len(self.buttons) - 1) * space)) // 2
        
        for button in self.buttons.sprites():
            button.rect.x = x
            button.update()
            x += width + space

    def blit(self):
        self.screen.blit(self._screen, self._rect)
        self._screen.fill((0, 0, 0, 0))
        self._blit()

        for button in self.buttons.sprites(): button.blit()


class ResumeButton(ButtonMixin, pygame.sprite.Sprite):
    def __init__(self, screen, base_dir):
        pygame.sprite.Sprite.__init__(self)

        self.width = self.height = 63

        self.img = pygame.image.load(f'{base_dir}/assets/images/buttons/resume.bmp')

        ButtonMixin.__init__(self, screen, base_dir, [], False)
