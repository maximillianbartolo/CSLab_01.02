# CS_Gamedesign_Lab01.02
__author__ = "Max Bartolo"
__version__ = "02/12/2025"

import pygame
import random

#create class to load and scale images
class ResourceManager:
    def __init__(self):
        self.images = {}

    def load_image(self, name, path, size=None):
        image = pygame.image.load(path)
        if size:
            image = pygame.transform.scale(image, size)
        self.images[name] = image
        return image

    def get_image(self, name):
        return self.images.get(name)

#create obstacle class
class Obstacle:
    def __init__(self, image, x, y):
        self.image = image
        self.x = x
        self.y = y
        # Make hitbox 80% of the image size
        hitbox_width = int(image.get_width() * 0.8)
        hitbox_height = int(image.get_height() * 0.8)
        # Center the hitbox in the image
        hitbox_x = x + (image.get_width() - hitbox_width) // 2
        hitbox_y = y + (image.get_height() - hitbox_height) // 2
        self.rect = pygame.Rect(hitbox_x, hitbox_y, hitbox_width, hitbox_height)

    def update(self, speed):
        self.y += speed
        # Update rectangle position to match image position
        # Keep the hitbox centered on the image
        self.rect.centerx = self.x + self.image.get_width() // 2
        self.rect.centery = self.y + self.image.get_height() // 2

#create player class
class Player:
    def __init__(self, image, x, y):
        self.image = image
        self.x = x
        self.y = y
        # Make hitbox 80% of the image size
        hitbox_width = int(image.get_width() * 0.8)
        hitbox_height = int(image.get_height() * 0.8)
        # Center the hitbox in the image
        hitbox_x = x + (image.get_width() - hitbox_width) // 2
        hitbox_y = y + (image.get_height() - hitbox_height) // 2
        self.rect = pygame.Rect(hitbox_x, hitbox_y, hitbox_width, hitbox_height)

    def update(self):
        # Keep the hitbox centered on the image
        self.rect.centerx = self.x + self.image.get_width() // 2
        self.rect.centery = self.y + self.image.get_height() // 2


# Initialize Pygame
pygame.init()

# Set up the display
WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Highwayrider')

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Initialize resource manager + set up resources
resources = ResourceManager()
player_image = resources.load_image('player', 'img/Car1.png', (50, 50))
obstacle_images = [
    resources.load_image(f'car{i}', f'img/cars copy {i}.png', (50, 50))
    for i in range(1, 9)
]

# Create player
player = Player(player_image, WIDTH // 2, HEIGHT - 100)

# Create list to store active obstacles
active_obstacles = []

# Player movement speed
speed = 1

# Initialize score and high score
score = 0
high_score = 0

# Debug mode for showing hitboxes (set to True to see them)
DEBUG_HITBOXES = False

# Game state
game_over = False

# Game loop
running = True
while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # Add restart capability when game is over
        elif event.type == pygame.KEYDOWN and game_over:
            if event.key == pygame.K_r:  # Press 'R' to restart
                game_over = False
                player.x = WIDTH // 2
                player.y = HEIGHT - 100
                active_obstacles.clear()
                score = 0  # Reset score when restarting

    if not game_over:
        # Get keyboard input
        keys = pygame.key.get_pressed()

        # Move player in all directions
        if keys[pygame.K_LEFT]:
            player.x -= speed
        if keys[pygame.K_RIGHT]:
            player.x += speed
        if keys[pygame.K_UP]:
            player.y -= .5
        if keys[pygame.K_DOWN]:
            player.y += speed

        # Keep player within screen bounds
        player.x = max(0, min(player.x, WIDTH - player.image.get_width()))
        player.y = max(0, min(player.y, HEIGHT - player.image.get_height()))

        # Update player rectangle position
        player.update()

        # Randomly add new obstacles
        if len(active_obstacles) < (score/1000) and random.random() < 0.02:
            new_obstacle = Obstacle(
                random.choice(obstacle_images),
                random.randint(0, WIDTH - 50),
                -50
            )
            active_obstacles.append(new_obstacle)

        # Update obstacle positions and check collisions
        for obstacle in active_obstacles[:]:
            obstacle.update(speed)
            if player.rect.colliderect(obstacle.rect):
                if score > high_score:
                    high_score = score
                game_over = True
                break
            if obstacle.y > HEIGHT:
                active_obstacles.remove(obstacle)

        # Increment score
        score += 1

    # Clear screen
    screen.fill(WHITE)

    # Draw score
    font = pygame.font.Font(None, 36)
    score_text = font.render(f'Score: {score}', True, BLACK)
    score_rect = score_text.get_rect(topleft=(10, 10))
    screen.blit(score_text, score_rect)

    # Draw high score
    high_score_text = font.render(f'High Score: {high_score}', True, BLACK)
    high_score_rect = high_score_text.get_rect(topleft=(10, 50))
    screen.blit(high_score_text, high_score_rect)

    # Draw obstacles
    for obstacle in active_obstacles:
        screen.blit(obstacle.image, (obstacle.x, obstacle.y))
        # Draw hitboxes in debug mode
        if DEBUG_HITBOXES:
            pygame.draw.rect(screen, RED, obstacle.rect, 1)

    # Draw player
    screen.blit(player.image, (player.x, player.y))
    # Draw player hitbox in debug mode
    if DEBUG_HITBOXES:
        pygame.draw.rect(screen, RED, player.rect, 1)

    # Draw game over screen
    if game_over:
        font = pygame.font.Font(None, 74)
        text = font.render('Game Over!', True, RED)
        text_rect = text.get_rect(center=(WIDTH / 2, HEIGHT / 2))
        screen.blit(text, text_rect)

        font = pygame.font.Font(None, 36)
        text = font.render('Press R to restart', True, RED)
        text_rect = text.get_rect(center=(WIDTH / 2, HEIGHT / 2 + 50))
        screen.blit(text, text_rect)

    # Update display
    pygame.display.flip()

# Quit game
pygame.quit()