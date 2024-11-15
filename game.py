import pygame
import random
import math
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Load images
player_image = pygame.image.load("player.png")
heart_image = pygame.image.load("love.png")
music_note_image = pygame.image.load("music.png")
strength_image = pygame.image.load("strength.png")
good_element_image = pygame.image.load("good.png")
evil_image = pygame.image.load("evil.png")

# Intro and end screen images
intro_image = pygame.image.load("s.png")
end_image = pygame.image.load("s.png")

# Scale images to fit game objects
player_size = 50
player_image = pygame.transform.scale(player_image, (player_size, player_size))
heart_size = 30
heart_image = pygame.transform.scale(heart_image, (heart_size, heart_size))
music_note_size = 20
music_note_image = pygame.transform.scale(music_note_image, (music_note_size, music_note_size))
strength_size = 25
strength_image = pygame.transform.scale(strength_image, (strength_size, strength_size))
good_element_size = 20
good_element_image = pygame.transform.scale(good_element_image, (good_element_size, good_element_size))
evil_size = 20
evil_image = pygame.transform.scale(evil_image, (evil_size, evil_size))

# Game setup
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Object Collection Game")
clock = pygame.time.Clock()

# Player setup
player_pos = [SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2]
player_speed = 5

# Initialize game variables
hearts_collected = 0
music_meter = 0
societal_value = 0
evil_score = 0
game_duration = 60000  # Game lasts for 60 seconds (in milliseconds)
start_time = None

# Object list
objects = []

# Define GameObject class
class GameObject:
    def __init__(self, type, image, size, speed=(0, 0)):
        self.type = type
        self.image = image
        self.size = size
        self.pos = [random.randint(0, SCREEN_WIDTH - size), random.randint(0, SCREEN_HEIGHT - size)]
        self.speed = speed
        self.collected = False

    def move(self):
        if self.type == "heart" and not self.collected:
            dx, dy = player_pos[0] - self.pos[0], player_pos[1] - self.pos[1]
            distance = math.hypot(dx, dy)
            if distance < 150:
                self.pos[0] -= dx / distance * 2
                self.pos[1] -= dy / distance * 2
            else:
                self.pos[0] += dx / distance * 1.5
                self.pos[1] += dy / distance * 1.5
        elif not self.collected:
            self.pos[0] += self.speed[0]
            self.pos[1] += self.speed[1]
            if self.pos[0] <= 0 or self.pos[0] >= SCREEN_WIDTH - self.size:
                self.speed[0] = -self.speed[0]
            if self.pos[1] <= 0 or self.pos[1] >= SCREEN_HEIGHT - self.size:
                self.speed[1] = -self.speed[1]

    def draw(self):
        if not self.collected:
            screen.blit(self.image, (self.pos[0], self.pos[1]))

# Function to spawn objects
def spawn_object():
    obj_types = ["music_note", "strength", "good_element", "evil", "heart"]
    obj_weights = [0.3, 0.2, 0.2, 0.2, 0.1]
    obj_type = random.choices(obj_types, weights=obj_weights, k=1)[0]
    speed = [random.choice([-2, 2]), random.choice([-2, 2])]
    if obj_type == "heart":
        objects.append(GameObject("heart", heart_image, heart_size, speed))
    elif obj_type == "music_note":
        objects.append(GameObject("music_note", music_note_image, music_note_size, speed))
    elif obj_type == "strength":
        objects.append(GameObject("strength", strength_image, strength_size, speed))
    elif obj_type == "good_element":
        objects.append(GameObject("good_element", good_element_image, good_element_size, speed))
    elif obj_type == "evil":
        objects.append(GameObject("evil", evil_image, evil_size, speed))

# Intro screen
def show_intro():
    screen.blit(intro_image, (0, 0))
    pygame.display.flip()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                waiting = False

# End screen
def show_end():
    screen.fill(WHITE)
    screen.blit(end_image, (0, 0))
    font = pygame.font.SysFont(None, 36)
    result_text = font.render(f"Final Score - Hearts: {hearts_collected}, Music Meter: {music_meter}, Societal Value: {societal_value}, Evil Score: {evil_score}", True, BLACK)
    screen.blit(result_text, (50, SCREEN_HEIGHT - 50))
    pygame.display.flip()
    pygame.time.delay(3000)  # Display end screen for 3 seconds

# Main game loop
def main():
    global hearts_collected, music_meter, societal_value, evil_score, player_speed, start_time

    # Display intro screen
    show_intro()

    # Initialize game start time
    start_time = pygame.time.get_ticks()
    last_spawn_time = pygame.time.get_ticks()
    last_music_decrement = pygame.time.get_ticks()
    music_decrement_interval = 1000  # Decrease music meter every second

    running = True
    while running:
        screen.fill(WHITE)
        current_time = pygame.time.get_ticks()

        # Check if game time has expired
        if current_time - start_time >= game_duration:
            running = False
            continue  # Exit game loop and show end screen

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Player movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            player_pos[0] -= player_speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            player_pos[0] += player_speed
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            player_pos[1] -= player_speed
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            player_pos[1] += player_speed

        # Keep the player within screen boundaries
        player_pos[0] = max(0, min(SCREEN_WIDTH - player_size, player_pos[0]))
        player_pos[1] = max(0, min(SCREEN_HEIGHT - player_size, player_pos[1]))

        # Draw player
        screen.blit(player_image, (player_pos[0], player_pos[1]))

        # Spawn objects at random intervals
        if current_time - last_spawn_time > random.randint(1000, 5000):
            spawn_object()
            last_spawn_time = current_time

        # Decrease music meter over time
        if current_time - last_music_decrement >= music_decrement_interval:
            if music_meter > 0:
                music_meter -= 1
            last_music_decrement = current_time

        # Move and draw objects
        for obj in objects:
            obj.move()
            obj.draw()
            # Check collision with player
            if not obj.collected and math.hypot(player_pos[0] - obj.pos[0], player_pos[1] - obj.pos[1]) < (player_size + obj.size) // 2:
                if obj.type == "heart":
                    hearts_collected += 1
                    music_meter += 1
                elif obj.type == "music_note":
                    music_meter += 5
                elif obj.type == "strength":
                    player_speed = 2
                    pygame.time.delay(500)
                    player_speed = 7
                elif obj.type == "good_element":
                    societal_value += 10
                elif obj.type == "evil":
                    societal_value -= 5
                    evil_score += 1
                obj.collected = True

        # Update HUD
        font = pygame.font.SysFont(None, 24)
        text = font.render(f"Hearts: {hearts_collected}  Music Meter: {music_meter}  Societal Value: {societal_value}  Evil Score: {evil_score}", True, BLACK)
        screen.blit(text, (10, 10))

        # Update screen and tick the clock
        pygame.display.flip()
        clock.tick(60)

    # Show end screen after the game loop exits
    show_end()

# Run the game
if __name__ == "__main__":
    main()
