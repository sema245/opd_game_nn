import pygame

class Projectile(pygame.sprite.Sprite):
    def __init__(self, x, y, direct, config):
        super().__init__()
        self.config = config
        self.direct = direct
        self.image = pygame.Surface((self.config.PROJECTILE_WIDTH, self.config.PROJECTILE_HEIGHT))
        self.image.fill(self.config.PROJECTILE_COLOR)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.y = y

    def update(self):
        self.rect.y += self.config.PROJECTILE_SPEED * self.direct
        if self.rect.bottom < 0 or self.rect.top > self.config.HEIGHT:
            self.kill()