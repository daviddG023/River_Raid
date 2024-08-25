import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 400, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("River Raid")

# Colors
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Clock to control frame rate
clock = pygame.time.Clock()

# Player properties
player_width = 50
player_height = 60
player_x = WIDTH // 2 - player_width // 2
player_y = HEIGHT - player_height - 10
player_speed = 5

# Enemy properties
enemy_width = 40
enemy_height = 60
enemy_speed = 5
enemies = []

# Fuel properties
fuel_width = 30
fuel_height = 50
fuel_speed = 5
fuels = []

# Score, fuel, and lives
score = 0
fuel_level = 100
lives = 3

# Font for score, fuel, and lives display
font = pygame.font.Font(None, 36)

# Load player image
player_img = pygame.Surface((player_width, player_height))
player_img.fill(GREEN)

# Load enemy image
enemy_img = pygame.Surface((enemy_width, enemy_height))
enemy_img.fill(RED)

# Load fuel image
fuel_img = pygame.Surface((fuel_width, fuel_height))
fuel_img.fill(BLUE)

# Bullet class
class Bullet:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 5, 10)
        self.speed = -10

    def move(self):
        self.rect.y += self.speed

    def draw(self, screen):
        pygame.draw.rect(screen, RED, self.rect)

# Main game loop
running = True
bullets = []

while running:
    screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                # Create a new bullet and add it to the bullets list
                bullet_x = player_x + player_width // 2 - 2.5
                bullet_y = player_y
                bullets.append(Bullet(bullet_x, bullet_y))

    # Player movement with added up and down controls
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_x > 0:
        player_x -= player_speed
    if keys[pygame.K_RIGHT] and player_x < WIDTH - player_width:
        player_x += player_speed
    if keys[pygame.K_UP] and player_y > 0:
        player_y -= player_speed
    if keys[pygame.K_DOWN] and player_y < HEIGHT - player_height:
        player_y += player_speed

    # Add new enemies
    if random.randint(1, 50) == 1:
        enemy_x = random.randint(0, WIDTH - enemy_width)
        enemies.append(pygame.Rect(enemy_x, 0, enemy_width, enemy_height))

    # Add new fuel pickups
    if random.randint(1, 200) == 1:
        fuel_x = random.randint(0, WIDTH - fuel_width)
        fuels.append(pygame.Rect(fuel_x, 0, fuel_width, fuel_height))

    # Move and draw bullets, and check collisions with enemies and fuel
    for bullet in bullets[:]:
        bullet.move()
        bullet.draw(screen)

        # Check for collision with enemies
        for enemy in enemies[:]:
            if bullet.rect.colliderect(enemy):
                enemies.remove(enemy)
                if bullet in bullets:
                    bullets.remove(bullet)

        # Check for collision with fuel
        for fuel in fuels[:]:
            if bullet.rect.colliderect(fuel):
                fuels.remove(fuel)
                if bullet in bullets:
                    bullets.remove(bullet)

        # Remove bullet if it goes off the screen
        if bullet.rect.y < 0:
            bullets.remove(bullet)

    # Move enemies and fuels, check collisions with player
    for enemy in enemies[:]:
        enemy.y += enemy_speed
        if enemy.y > HEIGHT:
            enemies.remove(enemy)
        if pygame.Rect(player_x, player_y, player_width, player_height).colliderect(enemy):
            lives -= 1  # Decrease lives on collision
            enemies.remove(enemy)  # Remove the enemy after collision
            if lives <= 0:
                running = False  # End the game if no lives left

    for fuel in fuels[:]:
        fuel.y += fuel_speed
        if fuel.y > HEIGHT:
            fuels.remove(fuel)
        if pygame.Rect(player_x, player_y, player_width, player_height).colliderect(fuel):
            fuel_level = min(fuel_level + 20, 100)
            fuels.remove(fuel)

    # Update fuel level
    fuel_level -= 0.1
    if fuel_level <= 0:
        running = False  # End the game if fuel runs out

    # Draw everything
    screen.blit(player_img, (player_x, player_y))
    for enemy in enemies:
        screen.blit(enemy_img, (enemy.x, enemy.y))
    for fuel in fuels:
        screen.blit(fuel_img, (fuel.x, fuel.y))

    # Draw score, fuel level, and lives
    score_text = font.render(f"Score: {score}", True, BLUE)
    fuel_text = font.render(f"Fuel: {int(fuel_level)}", True, BLUE)
    lives_text = font.render(f"Lives: {lives}", True, BLUE)
    screen.blit(score_text, (10, 10))
    screen.blit(fuel_text, (10, 40))
    screen.blit(lives_text, (10, 70))

    # Update the display
    pygame.display.flip()
    clock.tick(60)

    # Increase score
    score += 1

pygame.quit()
