import pygame
from Projectile import Projectile
class Agent(pygame.sprite.Sprite):
    agent_id = 0
    def __init__(self, x, y, config):
        super().__init__()
        self.shoot_cooldown = config.SHOOT_COOLDOWN
        self.config = config
        self.direction = 0
        self.image = pygame.Surface((self.config.PLAYER_WIDTH, self.config.PLAYER_HEIGHT))
        self.image.fill(self.config.PLAYER_COLOR)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.name = Agent.agent_id +1
        Agent.agent_id += 1

    def move(self, direction):
        self.direction = direction

    def update(self):
        if self.shoot_cooldown>0:
            self.shoot_cooldown -= 1
        self.rect.x += self.direction * self.config.PLAYER_SPEED
        self.rect.x = max(0, min(self.config.WIDTH - self.rect.width, self.rect.x))

    def get_shoot_cooldown(self):
        return self.shoot_cooldown

    def shoot(self, direct):
        self.shoot_cooldown = self.config.SHOOT_COOLDOWN
        if direct == -1:
            y = self.rect.top - self.config.PROJECTILE_HEIGHT
        else:
            y = self.rect.bottom
        return Projectile(self.rect.centerx, y, direct, self.config)
    def get_name(self):
        return self.name
