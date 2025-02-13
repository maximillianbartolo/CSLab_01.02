# CS_Gamedesign_Lab01.02
__author__ = "Max Bartolo"
__version__ = "02/12/2025"
#flint sessions:
#https://app.flintk12.com/activity/pygame-debug-le-1fe068/session/0e6e09e0-6165-4941-8a3e-5faf963ae27b
#https://app.flintk12.com/activity/pygame-debug-le-1fe068/session/1280406c-9824-425f-a67a-627d7298c339
#https://app.flintk12.com/activity/pygame-debug-le-1fe068/session/b9f30cf2-2d84-4a8e-a594-dc941b8586bd


import pygame
import random


# create class to load and scale images
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


# create obstacle class
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

    def is_colliding_with(self, other_obstacle):
        # Check both horizontal and vertical distance
        horizontal_distance = abs(self.x - other_obstacle.x)
        vertical_distance = abs(self.y - other_obstacle.y)
        return horizontal_distance < 60 and vertical_distance < 60  # Minimum spacing between obstacles


# create player class
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


def find_safe_spawn_position(width, active_obstacles):
    # Define lanes
    lane_width = width // 10
    lanes = [i * lane_width + lane_width // 2 for i in range(10)]

    # Try each lane in random order
    random.shuffle(lanes)
    for lane_x in lanes:
        # Check if position is safe
        is_safe = True
        for obstacle in active_obstacles:
            # Only check obstacles near the spawn area
            if obstacle.y < 100:  # Only check obstacles near the top
                if abs(obstacle.x - lane_x) < 60:  # Minimum horizontal spacing
                    is_safe = False
                    break
        if is_safe:
            return lane_x - 25  # Center the car in the lane (car width is 50)
    return None


def main():
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
    GRAY = (50, 50, 50)
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

    # Clock for controlling spawn rate
    clock = pygame.time.Clock()
    spawn_timer = 0
    SPAWN_DELAY = score*100  # Milliseconds between spawn attempts

    # Game loop
    running = True
    while running:
        # Get delta time
        dt = clock.tick(500)  # Limit to 60 FPS
        spawn_timer += dt

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
                    spawn_timer = 0

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

            # Try to spawn new obstacles
            if spawn_timer >= SPAWN_DELAY:
                spawn_timer = 0  # Reset timer
                if len(active_obstacles) < (score / 1000 + 5):
                    # Try to find a safe spawn position
                    spawn_x = find_safe_spawn_position(WIDTH, active_obstacles)
                    if spawn_x is not None:
                        new_obstacle = Obstacle(
                            random.choice(obstacle_images),
                            spawn_x,
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
        screen.fill(GRAY)

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


if __name__ == '__main__':
    main()
