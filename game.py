import pygame
import sys 
import random
import os
import firebase_admin
from firebase_admin import credentials, db

# Initialize Pygame
pygame.init()

# Set up the display
window_size = (600, 800)
window = pygame.display.set_mode(window_size)
pygame.display.set_caption("Knight Dodge")
current_directory = os.path.dirname(__file__)

#initalize firebase database
cred = credentials.Certificate(os.path.join(current_directory, 'game-85891-firebase-adminsdk-nvzq0-fe69045bc7.json'))
firebase_admin.initialize_app(cred, {
    "databaseURL": "https://game-85891-default-rtdb.firebaseio.com/"
})

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Constants
LANE_WIDTH = window_size[0] // 3
FPS = 60
ENEMY_SPAWN_DELAY = 60  # Delay for enemy creation (in frames)
SLIDE_SPEED = 10  # Speed of the knight sliding

# Sprites
knight_directory = os.path.join(current_directory, 'sprites', 'knight', 'knight-front.png')
enemy_directory = os.path.join(current_directory, 'sprites', 'enemy', 'soldier-front.png')

knight_sprite_folder = os.path.join(current_directory, 'sprites', 'knight', 'knight-animation')


knight_size = (96, 108)
enemy_sprite = pygame.image.load(enemy_directory)
enemy_size = (96, 96)
enemy_sprite = pygame.transform.scale(enemy_sprite, enemy_size)  # New width and height


knight_hitbox_size = (30, 50)  # Smaller hitbox for the knight
enemy_hitbox_size = (30, 120)   # Smaller hitbox for enemies





# Set up the Knight
class Knight:
    def __init__(self):

        # Adds sprite frames into list
        self.sprites = []
        self.sprites.append(pygame.image.load(os.path.join(knight_sprite_folder, 'frame0000.png')))
        self.sprites.append(pygame.image.load(os.path.join(knight_sprite_folder, 'frame0002.png')))
        self.sprites.append(pygame.image.load(os.path.join(knight_sprite_folder, 'frame0004.png')))
        self.sprites.append(pygame.image.load(os.path.join(knight_sprite_folder, 'frame0006.png')))
        self.current_sprite = 0
        self.image = self.sprites[self.current_sprite]
        
        
        self.animation_timer = 0 # Keeps track of current frame
        self.animation_rate = 10 # Animation Framerate
        
        
        self.width = 96
        self.height = 108
        self.hitbox_width = knight_hitbox_size[0]
        self.hitbox_height = knight_hitbox_size[1]
        self.lane = 1  # Start in the middle lane
        self.x = (self.lane * LANE_WIDTH) + ((LANE_WIDTH - self.width) // 2)  # Initialize x position
        self.target_x = self.x  # Set the target_x to the current x position
        self.y = window_size[1] - self.height - 20
        
    def update(self, window):

        self.animation_timer += 1
        if self.animation_timer >= self.animation_rate:
            self.current_sprite += 1
            self.animation_timer = 0
        
            if self.current_sprite >= 4:
                self.current_sprite = 0
                
        self.image = self.sprites[self.current_sprite]
        self.image = pygame.transform.scale(self.image, knight_size)
        window.blit(self.image, (self.x, self.y))

    def move_left(self):
        if self.lane > 0:
            self.lane -= 1
        self.target_x = (self.lane * LANE_WIDTH) + ((LANE_WIDTH - self.width) // 2)

    def move_right(self):
        if self.lane < 2:
            self.lane += 1
        self.target_x = (self.lane * LANE_WIDTH) + ((LANE_WIDTH - self.width) // 2)

    def move_middle(self):
        self.lane = 1  # Move to middle lane
        self.target_x = (self.lane * LANE_WIDTH) + ((LANE_WIDTH - self.width) // 2)

    def update_position(self):
        # Smoothly move towards the target position
        if self.x < self.target_x:
            self.x += SLIDE_SPEED
        elif self.x > self.target_x:
            self.x -= SLIDE_SPEED

    def draw(self, window):
        #window.blit(self.image, (self.x, self.y))
        pass
        

    def get_hitbox(self):
        # Return the hitbox rectangle
        return pygame.Rect(self.x + (self.width - self.hitbox_width) // 2, self.y + (self.height - self.hitbox_height) // 2, self.hitbox_width, self.hitbox_height)


# Set up the game clock
clock = pygame.time.Clock()

# Enemy Class
class Enemy:
    def __init__(self, lane):
        self.width = enemy_size[0]
        self.height = enemy_size[1]
        self.hitbox_width = enemy_hitbox_size[0]
        self.hitbox_height = enemy_hitbox_size[1]
        self.x = (lane * LANE_WIDTH) + ((LANE_WIDTH - self.width) // 2)  # Center align the enemy
        self.y = 0  # Start at the top of the screen
        self.base_speed = 2  # Base speed of falling
        self.speed_increase_rate = 0.02  # Speed increase per pixel fallen

    def fall(self):
        self.speed = self.base_speed + (self.y * self.speed_increase_rate)
        self.y += self.speed  # Update position

    def draw(self, window):
        window.blit(enemy_sprite, (self.x, self.y))

    def get_hitbox(self):
        # Return the hitbox rectangle
        return pygame.Rect(self.x + (self.width - self.hitbox_width) // 2, self.y + (self.height - self.hitbox_height) // 2, self.hitbox_width, self.hitbox_height)


# Function to draw the play again button
def draw_play_again_button(window):
    button_width = 200
    button_height = 50
    button_x = (window_size[0] - button_width) // 2
    button_y = window_size[1] // 2 + 50  # Position it below the game over message
    pygame.draw.rect(window, BLUE, (button_x, button_y, button_width, button_height))
    font = pygame.font.Font(None, 36)
    text = font.render("Play Again", True, WHITE)
    text_rect = text.get_rect(center=(button_x + button_width // 2, button_y + button_height // 2))
    window.blit(text, text_rect)

def draw_quit_button(window):
    button_width = 200
    button_height = 50
    button_x = (window_size[0] - button_width) // 2
    button_y = window_size[1] // 2 + 120  # Position it below the game over message
    pygame.draw.rect(window, RED, (button_x, button_y, button_width, button_height))
    font = pygame.font.Font(None, 36)
    text = font.render("Quit", True, WHITE)
    text_rect = text.get_rect(center=(button_x + button_width // 2, button_y + button_height // 2))
    window.blit(text, text_rect)

def start_menu():
    font = pygame.font.Font(None, 72)
    title_text = font.render("Knight Run", True, BLACK)
    title_rect = title_text.get_rect(center=(window_size[0] // 2, window_size[1] // 2 - 100))
    
    start_button_width = 200
    start_button_height = 50
    start_button_x = (window_size[0] - start_button_width) // 2
    start_button_y = window_size[1] // 2 + 50

    while True:
        window.fill(WHITE)  # Clear the screen
        window.blit(title_text, title_rect)
        pygame.draw.rect(window, BLUE, (start_button_x, start_button_y, start_button_width, start_button_height))
        text = font.render("Start", True, WHITE)
        text_rect = text.get_rect(center=(start_button_x + start_button_width // 2, start_button_y + start_button_height // 2))
        window.blit(text, text_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                if (start_button_x < mouse_x < start_button_x + start_button_width and
                        start_button_y < mouse_y < start_button_y + start_button_height):
                    return True  # Indicate that the game should start

        pygame.display.flip()
        clock.tick(FPS)


def save_high_score(score):
    ref = db.reference('highscores')  # Points to the 'highscores' node
    ref.push({                         # Adds a new score
        'score': score
    })
    print(f"High score saved: {score}")

def fetch_high_scores(limit=5):
    ref = db.reference('highscores')
    scores = ref.order_by_child('score').limit_to_last(limit).get()
    if not scores:
        return 0
    sorted_scores = sorted(scores.values(), key=lambda x: -x['score'])  # Sort descending
    return sorted_scores[0]['score'] if sorted_scores else 0  # Return the highest score


# Main game loop
def main():
    knight = Knight()
    enemies = []
    score = 0
    enemy_timer = 0  # Timer for enemy creation
    last_lane = -1  # Track the last lane used for spawning
    font = pygame.font.Font(None, 36)  # Initialize font for rendering text
    high_score = fetch_high_scores()
    
    # Creates instances of background paths and sets initial positions
    background_directory = os.path.join(current_directory, 'sprites', 'background-path.png')
    background_paths_image = pygame.image.load(background_directory)
    background_paths_image = pygame.transform.scale(background_paths_image, window_size)
    background_height = window_size[1]
    scroll_speed = 5 
    background_1_position = 0 # First image starts in the window
    background_2_position = window_size[1] # Second image starts below the first image, off screen
    

    game_over = False  # New variable to track game state

    if start_menu():
        running = True
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Handle mouse clicks to play again or quit
            if game_over and event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                # Check if "Play Again" button was clicked
                if (window_size[0] // 2 - 100 < mouse_x < window_size[0] // 2 + 100 and
                    window_size[1] // 2 + 50 < mouse_y < window_size[1] // 2 + 100):
                    # Reset game variables
                    knight = Knight()
                    enemies.clear()
                    score = 0
                    enemy_timer = 0
                    last_lane = -1
                    game_over = False
                        
                    high_score = fetch_high_scores()
                
                # Check if "Quit" button was clicked
                if (window_size[0] // 2 - 100 < mouse_x < window_size[0] // 2 + 100 and
                    window_size[1] // 2 + 120 < mouse_y < window_size[1] // 2 + 170):
                    running = False  # Exit the game

        if not game_over:
            # Get key presses and change the direction
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                knight.move_left()
            if keys[pygame.K_RIGHT]:
                knight.move_right()
            if keys[pygame.K_DOWN]:
                knight.move_middle()  # Move to middle lane

            # Update knight position smoothly
            knight.update_position()

            # Manage enemy spawning
            enemy_timer += 1
            if enemy_timer >= ENEMY_SPAWN_DELAY:  
                lane = random.randint(0, 2)  # Random lane (0, 1, or 2)

                # Ensure the new enemy is not in the same lane as the last one
                while lane == last_lane:
                    lane = random.randint(0, 2)

                new_enemy = Enemy(lane)
                enemies.append(new_enemy)
                last_lane = lane  # Update the last lane used
                enemy_timer = 0  # Reset the timer

            for enemy in enemies:
                enemy.fall()
                if enemy.y > window_size[1]:
                    enemies.remove(enemy)
                    score += 1  # Increase score for dodging

                # Check for collision
                if knight.get_hitbox().colliderect(enemy.get_hitbox()):
                    final_score = font.render(f"Game Over! Your score was: {score}", True, BLACK)
                    save_high_score(score)
                    window.fill(WHITE)  # Fill window to clear previous drawings
                    window.blit(final_score, (100, 400))  # Draw the game over text
                    pygame.display.flip()  # Update the display
                    pygame.time.wait(3000)  # Wait for 3 seconds
                    game_over = True  # Set game over state

        # Fill the screen with white if the game is not over
        if not game_over:
            window.fill(WHITE)
            
            # Moves the image positions by the scroll speed value
            background_1_position += scroll_speed
            background_2_position += scroll_speed
        
            # If the image is completely off screen, it is moved to above the other image
            if background_1_position >= window_size[1]:
                background_1_position = background_2_position - background_height
            if background_2_position >= window_size[1]:
                background_2_position = background_1_position - background_height

            # Draws images in the game window
            window.blit(background_paths_image, (0, background_1_position))
            window.blit(background_paths_image, (0, background_2_position))
            
            

            # Draw the knight and enemies
            knight.update(window)
            for enemy in enemies:
                enemy.draw(window)

            # Render the score and high score
            score_text = font.render(f"Score: {score}", True, BLACK)
            high_score_text = font.render(f"High Score: {high_score}", True, BLACK)
            window.blit(score_text, (10, 10))
            window.blit(high_score_text, (200, 10))

        else:
            # Draw the Play Again and Quit buttons when game is over
            draw_play_again_button(window)
            draw_quit_button(window)

        


        # Update the display
        pygame.display.flip()
        clock.tick(FPS)
        
        
        
        
        

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
