import pygame
import random
import os

from pygame.sprite import Group, spritecollide
from GameConfig import GameConfig
from Agent import Agent
from Projectile import Projectile

class Game:
    def __init__(self, render = True):
        pygame.init()
        self.config = GameConfig()
        self.WHITE = self.config.WHITE
        self.BLACK = self.config.BLACK
        self.GREEN = self.config.GREEN
        self.YELLOW = self.config.YELLOW
        self.RED = self.config.RED
        if render:
            self.screen = pygame.display.set_mode((self.config.WIDTH, self.config.HEIGHT))
            pygame.display.set_caption("Space Battle")
        else:
            os.environ["SDL_VIDEODRIVER"] = "dummy"
            pygame.display.set_mode((1, 1))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        
        # Состояние игры
        self.game_state = "menu"  # "menu", "playing", "game_over"
        self.winner = None
        
        # Группы спрайтов pygame
        self.all_sprites = Group()
        self.projectiles = Group()
        
        # Игроки
        self.player = None

    def start_game(self):
        self.all_sprites.empty()
        self.projectiles.empty()

        # Создать игрока внизу (стреляет вверх)
        player_x = self.config.WIDTH // 2 - self.config.PLAYER_WIDTH // 2
        player_y = self.config.HEIGHT - self.config.PLAYER_HEIGHT - 10
        self.player = Agent(player_x, player_y, self.config)
        self.all_sprites.add(self.player)

        # Создать бота вверху (стреляет вниз)
        bot_x = self.config.WIDTH // 2 - self.config.PLAYER_WIDTH // 2
        bot_y = 10
        self.bot = Agent(bot_x, bot_y, self.config)
        self.all_sprites.add(self.bot)

        self.bot_action_duration = 0
        self.bot_action = 0

        pygame.event.clear()
        pygame.key.set_repeat(0)

        self.game_state = "playing"

    def handle_events(self):
        """Обработка событий"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if self.game_state == "menu":
                        self.start_game()
                    elif self.game_state == "game_over":
                        self.game_state = "menu"
        
        return True

    def handle_player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.player.move(-1)
        elif keys[pygame.K_RIGHT]:
            self.player.move(1)

        if keys[pygame.K_SPACE] and self.player.get_shoot_cooldown() <= 0:
            self.shoot_projectile(self.player, -1)  # Стреляет вверх

    def handle_agent_logic(self, agent, direction):
        """Обработка логики поведения агента (например, ИИ-бота)"""
        if not agent:
            return

        if not hasattr(agent, "action_duration"):
            agent.action_duration = 0
            agent.action = 0

        if agent.action_duration <= 0:
            agent.action = random.choice([-1, 0, 1])
            agent.action_duration = random.randint(20, 60)

            if random.random() < 0.5 and agent.get_shoot_cooldown() <= 0:
                self.shoot_projectile(agent, direction)

        agent.move(agent.action)
        agent.action_duration -= 1

    def check_collisions(self):
        for proj in self.projectiles:
            if self.player and proj.rect.colliderect(self.player.rect) and proj.rect.centery < self.player.rect.centery:
                proj.kill()
                self.player.kill()
                self.winner = self.player.get_name()
                self.game_state = "game_over"
                break
            elif self.bot and proj.rect.colliderect(self.bot.rect) and proj.rect.centery > self.bot.rect.centery:
                proj.kill()
                self.bot.kill()
                self.winner = self.bot.get_name()
                self.game_state = "game_over"
                break

    def shoot_projectile(self, agent, direction):
        projectile = agent.shoot(direction)
        self.projectiles.add(projectile)
        self.all_sprites.add(projectile)

    def update(self):
        """Обновление игры"""
        if self.game_state == "playing":
            # Обновить счетчики


            if self.game_state == "playing":
                self.handle_agent_logic(self.bot, 1)
                self.handle_agent_logic(self.player, -1)
            # Обработка ввода
            
            # Обновить все спрайты (pygame автоматически вызовет update() для каждого)
            self.all_sprites.update()
            
            # Проверить столкновения
            self.check_collisions()

    def draw_menu(self):
        """Отрисовка меню"""
        self.screen.fill(self.BLACK)
        
        title = self.font.render("SPACE BATTLE", True, self.WHITE)
        title_rect = title.get_rect(center=(self.config.WIDTH // 2, 200))
        self.screen.blit(title, title_rect)
        
        instruction = self.font.render("Press SPACE to start", True, self.GREEN)
        instruction_rect = instruction.get_rect(center=(self.config.WIDTH // 2, 300))
        self.screen.blit(instruction, instruction_rect)
        
        controls = self.font.render("Arrow keys to move, SPACE to shoot", True, self.YELLOW)
        controls_rect = controls.get_rect(center=(self.config.WIDTH // 2, 400))
        self.screen.blit(controls, controls_rect)

    def draw_game(self):
        """Отрисовка игры"""
        self.screen.fill(self.BLACK)
        
        # Отрисовываем все спрайты (pygame автоматически использует image и rect)
        self.all_sprites.draw(self.screen)

    def draw_game_over(self):
        """Отрисовка экрана окончания игры"""
        self.screen.fill(self.BLACK)
        
        if self.winner:
            result = str(self.winner)+" WIN"
            color = self.WHITE
        
        result_text = self.font.render(result, True, color)
        result_rect = result_text.get_rect(center=(self.config.WIDTH // 2, 250))
        self.screen.blit(result_text, result_rect)
        
        restart = self.font.render("Press SPACE to return to menu", True, self.WHITE)
        restart_rect = restart.get_rect(center=(self.config.WIDTH // 2, 350))
        self.screen.blit(restart, restart_rect)

    def draw(self):
        """Основная отрисовка"""
        if self.game_state == "menu":
            self.draw_menu()
        elif self.game_state == "playing":
            self.draw_game()
        elif self.game_state == "game_over":
            self.draw_game_over()
        
        pygame.display.flip()


    def run(self):
        """Основной игровой цикл"""
        running = True
        while running:
            running = self.handle_events()  # <<< нужно, иначе окно "виснет"

            self.update()
            self.draw()

        
        pygame.quit()

if __name__ == "__main__":
    print("Игра загружается — Game.__init__()")
    game = Game()
    game.run()
