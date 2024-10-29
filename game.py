import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Set up the display
window_size = (600, 800)
window = pygame.display.set_mode(window_size)
pygame.display.set_caption("Dinosaur Dodge")

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Constants
LANE_WIDTH = window_size[0] // 3
FPS = 60
OBSTACLE_DELAY = 60  # Delay for obstacle creation (in frames)
SLIDE_SPEED = 10  # Speed of the dinosaur sliding

# Set up the Dinosaur
class Dinosaur:
    def __init__(self):
        self.width = LANE_WIDTH // 2
        self.height = 50
        self.lane = 1  # Start in the middle lane
        self.x = (self.lane * LANE_WIDTH) + (LANE_WIDTH // 4)  # Initialize x position
        self.target_x = self.x  # Set the target_x to the current x position
        self.y = window_size[1] - self.height - 50

    def move_left(self):
        if self.lane > 0:
            self.lane -= 1
        self.target_x = (self.lane * LANE_WIDTH) + (LANE_WIDTH // 4)

    def move_right(self):
        if self.lane < 2:
            self.lane += 1
        self.target_x = (self.lane * LANE_WIDTH) + (LANE_WIDTH // 4)

    def move_middle(self):
        self.lane = 1  # Move to middle lane
        self.target_x = (self.lane * LANE_WIDTH) + (LANE_WIDTH // 4)

    def update_position(self):
        # Smoothly move towards the target position
        if self.x < self.target_x:
            self.x += SLIDE_SPEED
        elif self.x > self.target_x:
            self.x -= SLIDE_SPEED

    def draw(self, window):
        pygame.draw.rect(window, GREEN, (self.x, self.y, self.width, self.height))


# Set up the game clock
clock = pygame.time.Clock()

# Obstacle Class
class Obstacle:
    def __init__(self, lane):
        self.width = LANE_WIDTH // 2
        self.height = 50
        self.x = (lane * LANE_WIDTH) + (LANE_WIDTH // 4)
        self.y = 0  # Start at the top of the screen

    def fall(self):
        self.y += 5  # Speed of falling

    def draw(self, window):
        pygame.draw.rect(window, RED, (self.x, self.y, self.width, self.height))


# Main game loop
def main():
    dinosaur = Dinosaur()
    obstacles = []
    score = 0
    obstacle_timer = 0  # Timer for obstacle creation
    last_lane = -1  # Track the last lane used for spawning

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Get key presses and change the direction
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            dinosaur.move_left()
        if keys[pygame.K_RIGHT]:
            dinosaur.move_right()
        if keys[pygame.K_DOWN]:
            dinosaur.move_middle()  # Move to middle lane

        # Update dinosaur position smoothly
        dinosaur.update_position()

        # Manage obstacle spawning
        obstacle_timer += 1
        if obstacle_timer >= OBSTACLE_DELAY:  
            lane = random.randint(0, 2)  # Random lane (0, 1, or 2)

            # Ensure the new obstacle is not in the same lane as the last one
            while lane == last_lane:
                lane = random.randint(0, 2)

            new_obstacle = Obstacle(lane)
            obstacles.append(new_obstacle)
            last_lane = lane  # Update the last lane used
            obstacle_timer = 0  # Reset the timer

        for obstacle in obstacles:
            obstacle.fall()
            if obstacle.y > window_size[1]:
                obstacles.remove(obstacle)
                score += 1  # Increase score for dodging

            # Check for collision
            if (obstacle.x < dinosaur.x + dinosaur.width and
                obstacle.x + obstacle.width > dinosaur.x and
                obstacle.y < dinosaur.y + dinosaur.height and
                obstacle.y + obstacle.height > dinosaur.y):
                print("Game Over! Your score was:", score)
                running = False

        # Fill the screen with white
        window.fill(WHITE)

        # Draw the dinosaur and obstacles
        dinosaur.draw(window)
        for obstacle in obstacles:
            obstacle.draw(window)

        # Render the score
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Score: {score}", True, BLACK)
        window.blit(score_text, (10, 10))

        # Update the display
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
