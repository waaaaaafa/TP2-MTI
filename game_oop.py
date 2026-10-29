import pygame
import random
import sys

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
COLOR_BG = (20, 24, 35)
COLOR_PLAYER = (50, 150, 255)
COLOR_MONSTER = (230, 60, 60)
COLOR_BULLET = (255, 215, 0)
COLOR_TEXT = (255, 255, 255)

class Bullet:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 12, 6)
        self.speed = 10

    def update(self):
        self.rect.x += self.speed

    def draw(self, surface):
        pygame.draw.rect(surface, COLOR_BULLET, self.rect)

class Player:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 40, 40)
        self.speed = 6

    def move(self, dy):
        self.rect.y += dy * self.speed
        if self.rect.top < 0: self.rect.top = 0
        if self.rect.bottom > SCREEN_HEIGHT: self.rect.bottom = SCREEN_HEIGHT

    def shoot(self):
        return Bullet(self.rect.right, self.rect.centery - 3)

    def draw(self, surface):
        pygame.draw.rect(surface, COLOR_PLAYER, self.rect)

class Monster:
    def __init__(self):
        self.rect = pygame.Rect(SCREEN_WIDTH - 60, random.randint(50, SCREEN_HEIGHT - 90), 40, 40)
        self.speed = 3
        self.direction = random.choice([-1, 1])

    def update(self):
        self.rect.y += self.speed * self.direction
        if self.rect.top <= 0 or self.rect.bottom >= SCREEN_HEIGHT:
            self.direction *= -1

    def reset(self):
        self.rect.x = SCREEN_WIDTH - 60
        self.rect.y = random.randint(50, SCREEN_HEIGHT - 90)
        self.direction = random.choice([-1, 1])

    def draw(self, surface):
        pygame.draw.rect(surface, COLOR_MONSTER, self.rect)

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("2D Shooting Game - Object-Oriented Design")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Arial", 22)
        self.player = Player(50, SCREEN_HEIGHT // 2)
        self.monster = Monster()
        self.bullets = []
        self.score = 0
        self.running = True

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.bullets.append(self.player.shoot())

        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.player.move(-1)
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.player.move(1)

    def update(self):
        self.monster.update()
        for bullet in self.bullets[:]:
            bullet.update()
            if bullet.rect.left > SCREEN_WIDTH:
                self.bullets.remove(bullet)
            elif bullet.rect.colliderect(self.monster.rect):
                self.bullets.remove(bullet)
                self.monster.reset()
                self.score += 1

    def draw(self):
        self.screen.fill(COLOR_BG)
        self.player.draw(self.screen)
        self.monster.draw(self.screen)
        for bullet in self.bullets:
            bullet.draw(self.screen)
        score_surface = self.font.render(f"Score: {self.score}", True, COLOR_TEXT)
        self.screen.blit(score_surface, (20, 20))
        pygame.display.flip()

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(60)
        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.run()