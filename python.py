import pygame
import random # For random enemy and fuel spawn

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
BROWN = (139, 69, 19)  # Color for the bridge
YELLOW = (255, 255, 0)  # Color for the side target

# Clock to control frame rate
clock = pygame.time.Clock()

# Player properties
player_width = 65
player_height = 65
player_x = WIDTH // 2 - player_width // 2
player_y = HEIGHT - player_height - 10
player_speed = 5
is_immune = False
immune_time = 0
immune_duration = 2000  # in milliseconds

# Enemy properties
enemy_width = 120
enemy_height = 60
enemy_speed = 5
enemies = []

# Fuel properties
fuel_width = 50
fuel_height = 100
fuel_speed = 5
fuels = []

# Sideways-moving target properties
side_target_width = 50
side_target_height = 30
side_target_speed = 3
side_targets = []

# Score, fuel, and lives
score = 0
fuel_level = 100
lives = 3

# Font for score, fuel, lives, and game over display
font = pygame.font.Font(None, 36)
game_over_font = pygame.font.Font(None, 72)

# Load player image
player_img = pygame.Surface((player_width, player_height))
player_img.fill(GREEN)
player_img = pygame.transform.scale(pygame.image.load("assets/plane.png"), (65, 65))


# Load enemy image
enemy_img = pygame.Surface((enemy_width, enemy_height))
enemy_img.fill(RED)
enemy_img = pygame.transform.scale(pygame.image.load("assets/boat.png"), (120, 60))


# Load fuel image
fuel_img = pygame.Surface((fuel_width, fuel_height))
fuel_img = pygame.transform.scale(pygame.image.load("assets/fuel.png"), (50, 100))



# Sideways target class
# Load the side target image
side_target_img = pygame.transform.scale(pygame.image.load("assets/plane2.png"), (50, 30))

class SideTarget:
    def __init__(self):
        self.rect = pygame.Rect(random.randint(0, WIDTH - side_target_width), 0, side_target_width, side_target_height)
        self.horizontal_speed = side_target_speed
        self.vertical_speed = enemy_speed  # Same as the red enemies
        self.direction = random.choice([-1, 1])  # Start moving either left or right

    def move(self):
        self.rect.x += self.horizontal_speed * self.direction
        self.rect.y += self.vertical_speed

        # Bounce back when hitting the left or right edge
        if self.rect.left <= 0 or self.rect.right >= WIDTH:
            self.direction *= -1

    def draw(self, screen):
        screen.blit(side_target_img, (self.rect.x, self.rect.y))


# Bullet class
class Bullet:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 5, 10)
        self.speed = -10

    def move(self):
        self.rect.y += self.speed

    def draw(self, screen):
        pygame.draw.rect(screen, RED, self.rect)

# Bridge class
class Bridge:
    def __init__(self):
        self.rect = pygame.Rect(0, 0, WIDTH, 20)
        self.y = 0
        self.speed = 5

    def move(self):
        self.y += self.speed
        self.rect.y = self.y

    def draw(self, screen):
        pygame.draw.rect(screen, BROWN, self.rect)

# Game Over screen
def game_over_screen():
    game_over_text = game_over_font.render("GAME OVER", True, RED)
    screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - game_over_text.get_height() // 2))
    pygame.display.flip()

    # Wait for the player to press the "X" button to close the game
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                waiting = False

# Initialize variables
bridge_spawned = False
bridges = []
side_target_spawned = False  # Track if a side target is currently active
next_bridge_score = 1000  # Next score at which to spawn a bridge

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

    # Spawn a sideways target every 500 points (adjust as desired)
    if score >= 500 and not side_target_spawned:
        side_targets.append(SideTarget())
        side_target_spawned = True

    # Spawn a bridge at every multiple of 1000 points
    if score >= next_bridge_score and not bridge_spawned:
        bridges.append(Bridge())
        bridge_spawned = True
        next_bridge_score += 1000  # Update the next score threshold for the next bridge

    # Move and draw bullets, and check collisions with enemies, fuel, and bridges
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

        # Check for collision with bridges
        for bridge in bridges[:]:
            if bullet.rect.colliderect(bridge.rect):
                bridges.remove(bridge)  # Remove the bridge if hit
                if bullet in bullets:
                    bullets.remove(bullet)

        # Check for collision with side targets
        for target in side_targets[:]:
            if bullet.rect.colliderect(target.rect):
                side_targets.remove(target)  # Remove the target if hit
                if bullet in bullets:
                    bullets.remove(bullet)
                side_target_spawned = False  # Allow spawning a new side target

        # Remove bullet if it goes off the screen
        if bullet.rect.y < 0:
            bullets.remove(bullet)

    # Move and draw sideways targets
    for target in side_targets:
        target.move()
        target.draw(screen)

    # Move bridges and check for collision with the player
    for bridge in bridges[:]:
        bridge.move()
        bridge.draw(screen)
        if pygame.Rect(player_x, player_y, player_width, player_height).colliderect(bridge.rect):
            running = False  # End the game if the player crashes into the bridge

    # Move enemies and fuels, check collisions with player
    for enemy in enemies[:]:
        enemy.y += enemy_speed
        if enemy.y > HEIGHT:
            enemies.remove(enemy)
        if pygame.Rect(player_x, player_y, player_width, player_height).colliderect(enemy) and not is_immune:
            lives -= 1  # Decrease lives on collision
            enemies.remove(enemy)  # Remove the enemy after collision
            if lives <= 0:
                running = False  # End the game if no lives left
            else:
                is_immune = True  # Start the immunity period
                immune_time = pygame.time.get_ticks()  # Record the time when hit

    # Increase fuel level when player is on fuel
    for fuel in fuels[:]:
        fuel.y += fuel_speed
        if fuel.y > HEIGHT:
            fuels.remove(fuel)
        if pygame.Rect(player_x, player_y, player_width, player_height).colliderect(fuel):
            fuel_level = min(fuel_level + 0.5, 100)  # Increase fuel gradually while on fuel

    # Update fuel level (slower rate)
    fuel_level -= 0.05  # Slower decrease rate for fuel
    if fuel_level <= 0:
        running = False  # End the game if fuel runs out

    # Handle immunity and "glitching" effect
    if is_immune:
        # Calculate the elapsed time since hit
        elapsed_time = pygame.time.get_ticks() - immune_time
        if elapsed_time < immune_duration:
            # Make the player "glitch" by flashing (alternating visibility)
            if elapsed_time // 100 % 2 == 0:
                screen.blit(player_img, (player_x, player_y))
        else:
            is_immune = False  # End immunity after the duration is over
            # Render player normally when not flashing
            screen.blit(player_img, (player_x, player_y))
    else:
        # Regular player rendering when not immune
        screen.blit(player_img, (player_x, player_y))

    # Reset bridge spawn flag after the bridge has moved off screen
    if bridges and bridges[0].y > HEIGHT:
        bridges.pop(0)
        bridge_spawned = False  # Allow spawning a new bridge at the next 1000 points

    # Draw everything else (enemies, fuel, bridges)
    for enemy in enemies:
        screen.blit(enemy_img, (enemy.x, enemy.y))
    for fuel in fuels:
        screen.blit(fuel_img, (fuel.x, fuel.y))
    for bridge in bridges:
        bridge.draw(screen)

    # Draw player on top of the fuel
    screen.blit(player_img, (player_x, player_y))

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

# Show the Game Over screen
game_over_screen()

pygame.quit()
