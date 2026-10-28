import random
import pygame

WIDTH, HEIGHT = 800, 500
WHITE, BLACK, RED, BLUE = (255, 255, 255), (0, 0, 0), (200, 0, 0), (0, 100, 255)


class Bullet:
    def __init__(self, x, y, speed=10, damage=1):
        self.x, self.y, self.speed, self.damage = x, y, speed, damage

    def update(self):
        self.x += self.speed

    @property
    def rect(self):
        return pygame.Rect(self.x, self.y, 10, 5)

    def draw(self, screen):
        pygame.draw.rect(screen, BLACK, self.rect)


class Player:
    def __init__(self):
        self.x, self.y, self.speed = 50, 220, 5
        self.shoot_delay, self._last_shot, self.score = 150, 0, 0

    def move(self, dy):
        self.y = max(0, min(HEIGHT - 30, self.y + dy * self.speed))

    def shoot(self, now):
        if now - self._last_shot > self.shoot_delay:
            self._last_shot = now
            return Bullet(self.x + 40, self.y + 15)

    @property
    def rect(self):
        return pygame.Rect(self.x, self.y, 40, 30)

    def draw(self, screen):
        pygame.draw.rect(screen, BLUE, self.rect)


class Monster:
    def __init__(self):
        self.x, self.y, self.speed = 700, 220, 3

    def update(self):
        self.y += self.speed
        if self.y <= 0 or self.y >= HEIGHT - 30:
            self.speed = -self.speed

    def respawn(self):
        self.y = random.randint(0, HEIGHT - 30)

    @property
    def rect(self):
        return pygame.Rect(self.x, self.y, 40, 30)

    def draw(self, screen):
        pygame.draw.rect(screen, RED, self.rect)


class GameBoard:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Shooting Monster Game")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.player, self.monster, self.bullets = Player(), Monster(), []
        self.running = True

    def handle_input(self):
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                self.running = False
        k = pygame.key.get_pressed()
        if k[pygame.K_UP]:
            self.player.move(-1)
        if k[pygame.K_DOWN]:
            self.player.move(1)
        if k[pygame.K_SPACE]:
            b = self.player.shoot(pygame.time.get_ticks())
            if b:
                self.bullets.append(b)

    def update(self):
        self.monster.update()
        for b in self.bullets[:]:
            b.update()
            if b.x > WIDTH:
                self.bullets.remove(b)
            elif b.rect.colliderect(self.monster.rect):
                self.player.score += b.damage
                self.bullets.remove(b)
                self.monster.respawn()

    def draw(self):
        self.screen.fill(WHITE)
        self.player.draw(self.screen)
        self.monster.draw(self.screen)
        for b in self.bullets:
            b.draw(self.screen)
        self.screen.blit(self.font.render(f"Score: {self.player.score}", True, BLACK), (10, 10))
        pygame.display.update()

    def run(self):
        while self.running:
            self.handle_input()
            self.update()
            self.draw()
            self.clock.tick(60)
        pygame.quit()


if __name__ == "__main__":
    GameBoard().run()