import pygame
import random
import math
import sys
import pygame.gfxdraw
import time
# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (50, 50, 50)
SHADOW = (30, 30, 30, 128)  # Semi-transparent shadow

# Font
font = pygame.font.Font(None, 24)
# Load images
popup_image = pygame.image.load("popup.png")  # Replace with your image path
popup_image = pygame.transform.scale(popup_image, (600, 400))  # Adjust the size as needed
heart_spawned = False
player_image = pygame.image.load("player.png")
heart_image = pygame.image.load("love.png")
music_note_image = pygame.image.load("music.png")
strength_image = pygame.image.load("strength.png")
good_element_image = pygame.image.load("good.png")
evil_image = pygame.image.load("evil.png")

# Intro and end screen images
intro_image = pygame.image.load(".dist/assets/1.png")
# Colors
GREEN = (0, 255, 0)
ORANGE = (255, 165, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
SEMI_TRANSPARENT_BLACK = (0, 0, 0, 150)

title_font = pygame.font.SysFont(None, 25, bold=True)

# Load your custom icon image
icon = pygame.image.load("grape.png")  # Replace with your image path

# Set the window icon to your custom image
pygame.display.set_icon(icon)

# Gauge properties
min_value = -100
max_value = 100
center = (SCREEN_WIDTH - 690, SCREEN_HEIGHT - 20)
radius = 60

def draw_gauge(screen, value, min_value, max_value, center, radius):
    rect_width, rect_height = 210, 130  # Width and height of the rectangle
    rect_x = 7  # Bottom-left corner starts at x = 0
    rect_y = SCREEN_HEIGHT - rect_height - 5
    pygame.draw.rect(screen, (60, 60, 60), (rect_x, rect_y, rect_width, rect_height))


    # Normalize value to -1 to 1 range
    normalized_value = (value - min_value) / (max_value - min_value) * 2 - 1
    normalized_value = max(-1, min(1, normalized_value))  # Clamp between -1 and 1

    # Calculate angle for the needle based on the normalized value
    angle = math.pi - (normalized_value + 1) * (math.pi / 2)

    # Needle position
    needle_length = radius * 0.8
    needle_x = center[0] + needle_length * math.cos(angle)
    needle_y = center[1] - needle_length * math.sin(angle)

    # Draw gauge arcs
    pygame.draw.arc(screen, GREEN, 
                    (center[0] - radius, center[1] - radius, radius * 2, radius * 2), 
                    0, math.pi / 3, 6)
    pygame.draw.arc(screen, ORANGE, 
                    (center[0] - radius, center[1] - radius, radius * 2, radius * 2), 
                    math.pi / 3, 2 * math.pi / 3, 6)
    pygame.draw.arc(screen, RED, 
                    (center[0] - radius, center[1] - radius, radius * 2, radius * 2), 
                    2 * math.pi / 3, math.pi, 6)

    # Draw needle
    pygame.draw.line(screen, BLACK, center, (needle_x, needle_y), 3)

    # Draw center circle
    pygame.draw.circle(screen, BLACK, center, 5)

    # Draw labels
    good_label = font.render("Good", True, GREEN)
    bad_label = font.render("Evil", True, RED)
    screen.blit(good_label, (center[0] + radius - 10, center[1] - radius - 15))  # Good label at the green end
    screen.blit(bad_label, (center[0] - radius - 30, center[1] - radius - 15))  # Bad label at the red end

   # Draw title "Your Score" inside the gauge
    title_text = title_font.render("Societal Value", True, WHITE)
    screen.blit(title_text, (center[0] - title_text.get_width() // 2, center[1] - radius - 40))


# Load images and store in a list
og_images = [
    pygame.image.load(".dist/assets/2.png"),  # Image 1
    pygame.image.load(".dist/assets/3.png"),  # Image 2
    pygame.image.load(".dist/assets/4.png"),  # Image 3
    pygame.image.load(".dist/assets/5.png"),  # Image 4
    pygame.image.load(".dist/assets/6.png"),  # Image 4
    pygame.image.load(".dist/assets/howtoplay.png")   # Image 4
]

end_images = [
    pygame.image.load(".dist/assets/10.png"),  # Image 1
    pygame.image.load(".dist/assets/11.png"),  # Image 2
    pygame.image.load(".dist/assets/12.png"),  # Image 3
    pygame.image.load(".dist/assets/13.png"),  # Image 4
    pygame.image.load(".dist/assets/14.png")   # Image 4 
]

# Scale images to fit screen (optional)
for i in range(len(og_images)):
    og_images[i] = pygame.transform.scale(og_images[i], (SCREEN_WIDTH, SCREEN_HEIGHT))

# Scale images to fit screen (optional)
for i in range(len(end_images)):
    end_images[i] = pygame.transform.scale(end_images[i], (SCREEN_WIDTH, SCREEN_HEIGHT))



# Current image index
current_image_index = 0

# Function to shake the screen and display errors
def screen_shake_with_errors(duration=2000, intensity=10, error_messages=None):
    if error_messages is None:
        error_messages = [
            "Error: System Overload!",
            "Critical Failure Detected!",
            "Memory Leak Detected!",
            "Unknown Error Code 404!"
        ]
    
    shake_end_time = pygame.time.get_ticks() + duration  # Calculate end time for the effect
    
    while pygame.time.get_ticks() < shake_end_time:
        # Generate random offsets for screen shaking
        shake_x = random.randint(-intensity, intensity)
        shake_y = random.randint(-intensity, intensity)
        
        # Fill background with black
        screen.fill(BLACK)
        
        # Redraw the player and objects at the new screen position
        screen.blit(player_image, (player_pos[0] + shake_x, player_pos[1] + shake_y))
        for obj in objects:
            if not obj.collected:
                obj.draw()

        # Display random error messages
        font = pygame.font.SysFont(None, 36)
        error_text = font.render(random.choice(error_messages), True, (255, 0, 0))
        screen.blit(error_text, (random.randint(50, SCREEN_WIDTH - 200), random.randint(50, SCREEN_HEIGHT - 50)))
        
        pygame.display.flip()
        pygame.time.delay(50)  # Short delay for smoother shaking

# Function to display image with fade-out effect
def fade_out(image, fade_speed=5):
    for alpha in range(255, -1, -fade_speed):
        image.set_alpha(alpha)  # Change image transparency
        screen.fill(BLACK)  # Fill background with white
        screen.blit(image, (0, 0))  # Draw image
        pygame.display.flip()
        pygame.time.delay(10)

# Function to display the next image
def next_image():
    global current_image_index
    if current_image_index < len(og_images) - 1:
        current_image_index += 1
    else:
        current_image_index = 0  # Loop back to the first image if needed

# Popup function to display the image
def show_congratulations_popup():
    # Create a semi-transparent surface for the popup background
    popup_background = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    popup_background.fill((0, 0, 0, 128))  # Semi-transparent black background

    # Center the popup image
    popup_center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    popup_image_rect = popup_image.get_rect(center=popup_center)

    # Display the popup
    screen.blit(popup_background, (0, 0))  # Darkened background
    screen.blit(popup_image, popup_image_rect)  # Centered image
    pygame.display.flip()

    # Pause to show the popup or control display time in the game loop
    time.sleep(8)


def draw_dynamic_background():
    if music_meter > 0.2:
        # Create a temporary surface with the same size as the screen
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        # screen.fill(WHITE)
        # Generate a random color with opacity (0.5) when music meter is above 0.2
        color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255), 51)  # 128 for 50% opacity
        overlay.fill(color)

        # Blit the semi-transparent overlay onto the main screen
        screen.blit(overlay, (0, 0))
    else:
        screen.blit(background_image, (0, 0))  # Draw the background image
# Function to display storyline with fade-out and fade-in between images
def display_storyline():
    global current_image_index
    for _ in range(len(og_images)):
        # Display current image with fade-in
        fade_in(og_images[current_image_index], fade_speed=5)
        pygame.time.delay(4000)  # Pause for 2 seconds
    
        # Fade out the current image
        fade_out(og_images[current_image_index], fade_speed=5)
        
        # Move to the next image
        next_image()
# Scale images to fit game objects
player_size = 70
player_image = pygame.transform.scale(player_image, (player_size,player_size-5))
heart_size = 40
heart_image = pygame.transform.scale(heart_image, (heart_size, heart_size))
music_note_size = 40
music_note_image = pygame.transform.scale(music_note_image, (music_note_size, music_note_size))
strength_size = 45
strength_image = pygame.transform.scale(strength_image, (strength_size, strength_size))
good_element_size = 40
good_element_image = pygame.transform.scale(good_element_image, (good_element_size, good_element_size))
evil_size = 40
evil_image = pygame.transform.scale(evil_image, (evil_size, evil_size+20))

# Game setup
background_image = pygame.image.load(".dist/assets/9.png")
background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Nietzsche's Quest")
clock = pygame.time.Clock()

# Player setup
player_pos = [SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2]
player_speed = 3

# Initialize game variables
hearts_collected = 0
music_meter = 0
societal_value = 0
evil_score = 0
game_duration = 80000  # Game lasts for 60 seconds (in milliseconds)
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
        self.angle = 0  # For rotation
        self.rotation_speed = 5 # Degrees per frame

    def rotate(self):
        self.angle += self.rotation_speed
        if self.angle >= 360:
            self.angle = 0  # Reset rotation after one full turn

    def resize_heart(self):
        if self.type == "heart" and music_meter > 2:  # If music is playing above a threshold
            self.size = int(40 * 1.5)  # Increase size by 50%
        else:
            self.size = 40  # Reset to original size if condition not met

        # Update the scaled heart image
        self.image = pygame.transform.scale(heart_image, (self.size, self.size))

    def move(self):
        # Check if music volume is above 0.5 (adjust based on your audio analysis)
       
        if music_meter > 2 and self.type != "heart":  # If the volume is above the threshold, sync the movement
            print("Music",music_meter)
            
                # Sync all objects in a similar way (e.g., move in a pattern)
            self.rotate()
        else:
            self.angle = 0
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
            if self.type == "heart":
                self.resize_heart()
            rotated_image = pygame.transform.rotate(self.image, self.angle)
           # screen.blit(self.image, (self.pos[0], self.pos[1]))
            # Draw the rotated image
            rect = rotated_image.get_rect(center=(self.pos[0] + self.size // 2, self.pos[1] + self.size // 2))
            screen.blit(rotated_image, rect.topleft)


# Function to spawn objects
def spawn_object():
    global heart_spawned
    obj_types = ["music_note", "strength", "good_element", "evil", "heart"]
    obj_weights = [0.3, 0.2, 0.2, 0.2, 0.2]
    obj_type = random.choices(obj_types, weights=obj_weights, k=1)[0]
    speed = [random.choice([-2, 2]), random.choice([-2, 2])]
    if obj_type == "heart" and heart_spawned == False:
        objects.append(GameObject("heart", heart_image, heart_size, speed))
        heart_spawned = True  # Set flag to True after spawning
    # if obj_type == "heart":
    #     objects.append(GameObject("heart", heart_image, heart_size, speed))
    elif obj_type == "music_note":
        objects.append(GameObject("music_note", music_note_image, music_note_size, speed))
    elif obj_type == "strength":
        objects.append(GameObject("strength", strength_image, strength_size, speed))
    elif obj_type == "good_element":
        objects.append(GameObject("good_element", good_element_image, good_element_size, speed))
    elif obj_type == "evil":
        objects.append(GameObject("evil", evil_image, evil_size, speed))

# Function to display image with fade-in effect
def fade_in(image, fade_speed=5):
    temp_image = image.copy()  # Create a copy of the image to manipulate
    for alpha in range(0, 256, fade_speed):  # Increment alpha from 0 to 255
        temp_image.set_alpha(alpha)  # Set transparency
        screen.fill(BLACK)  # Clear the screen with a black background
        screen.blit(temp_image, (0, 0))  # Draw the image
        pygame.display.flip()
        pygame.time.delay(10)

# Intro screen
def show_intro():
    fade_in(intro_image, fade_speed=5)  # Intro image fades in
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                waiting = False
    display_storyline()  # Start the storyline sequence


# Function to play music
def play_music(filename):
    pygame.mixer.music.load(filename)
    pygame.mixer.music.play(-1, 0.0)  # Play music indefinitely

def end_game():
    print("Game ended!")
    stop_music()  # Stop current music
    pygame.mixer.music.set_volume(0.8)  # Set volume to 50% (default is 1.0)
    play_music("endmusic.mp3")  # Play the new music after game ends

def show_scores():
    # Clear the screen
    screen.fill(WHITE)

    # Load scoreboard image (ensure the path is correct)
    scoreboard_image = pygame.image.load(".dist/assets/scoreboard.png")

    # Display the scoreboard image
    screen.blit(scoreboard_image, (0, 0))  # Position it as needed on the screen
    pygame.display.flip()  # Update the display to show the image

    # Set the font size and make it bold
    font = pygame.font.SysFont(None, 36, bold=True)  # Smaller font size for better spacing

    # Create the result text with the final scores, splitting the text into multiple lines
    result_lines = [
        f"Hearts: {hearts_collected}",
        # f"Music Meter: {music_meter}",
        f"Societal Value: {societal_value}"
        # f"Evil Score: {evil_score}"
    ]

    # Calculate the height of the text block
    text_height = len(result_lines) * 50  # Line height for spacing between lines

    # Calculate the position to center the text block vertically
    y_offset = (350) - (text_height // 2)

    # Draw each line of the result text
    for i, line in enumerate(result_lines):
        result_text = font.render(line, True, WHITE)
        text_width, _ = result_text.get_size()

        # Center each line horizontally and position it vertically with a 10-pixel gap
        screen.blit(result_text, (SCREEN_WIDTH // 2 - text_width // 2, y_offset + i * 50))

    pygame.display.flip()  # Update the display to show the result text

    # Wait for 3 seconds to display the final score
    pygame.time.delay(5000)

def stop_music():
    pygame.mixer.music.stop()
# End screen
def show_end():
    screen.fill(WHITE)  # Clear the screen

    # Loop through each image in the end sequence
    for image in end_images:
        fade_in(image, fade_speed=5)  # Fade in the image
        pygame.time.delay(8000)       # Display the image for 1 second
        fade_out(image, fade_speed=5) # Fade out the image

    # After all images, show final score text
    font = pygame.font.SysFont(None, 36)
    result_text = font.render(
        f"Final Score - Hearts: {hearts_collected}, Societal Value: {societal_value}",
        True, BLACK
    )
    screen.blit(result_text, (50, SCREEN_HEIGHT - 50))
    pygame.display.flip()
    pygame.time.delay(3000)  # Display final score for 3 seconds

# Define the scoreboard dimensions and position
scoreboard_width = 250
scoreboard_height = 100
scoreboard_padding = 10
scoreboard_x = screen.get_width() - scoreboard_width - 30
scoreboard_y = screen.get_height() - scoreboard_height - 30

# Function to draw the styled scoreboard
def draw_scoreboard():
    # Draw shadow
    shadow_rect = pygame.Rect(scoreboard_x + 5, scoreboard_y + 5, scoreboard_width, scoreboard_height)
    pygame.gfxdraw.box(screen, shadow_rect, SHADOW)

    # Draw background box with rounded corners
    background_rect = pygame.Rect(scoreboard_x, scoreboard_y, scoreboard_width, scoreboard_height)
    pygame.gfxdraw.box(screen, background_rect, GREY)
    pygame.gfxdraw.rectangle(screen, background_rect, BLACK)  # Border around the box

    # Render text for each item in the scoreboard
    text_y_offset = scoreboard_y + scoreboard_padding
    scoreboard_texts = [
        f"Hearts: {hearts_collected}",
        # f"Music Meter: {music_meter}",
        f"Societal Value: {societal_value}"
        # f"Evil Score: {evil_score}"
    ]

    for text in scoreboard_texts:
        text_surface = font.render(text, True, WHITE)
        screen.blit(text_surface, (scoreboard_x + scoreboard_padding, text_y_offset))
        text_y_offset += text_surface.get_height() + 5  # Space between lines



# Game loop
last_music_decrement = pygame.time.get_ticks()
music_decrement_interval = 1000  # Decrease music meter every second
last_spawn_time = pygame.time.get_ticks()

pygame.font.init()
font = pygame.font.Font(None, 24)  # Default font with size 24

# Function to draw the volume meter with purple color and label
def draw_volume_meter():
    max_meter_height = 150  # Max height for the volume meter bar
    meter_width = 20  # Width of the volume meter bar
    x_pos = SCREEN_WIDTH - 50  # X-position of the volume meter bar
    y_pos = (SCREEN_HEIGHT - max_meter_height) // 2  # Y-position of the volume meter bar

    # Calculate the height of the filled portion of the meter based on music_meter
    meter_fill_height = int((music_meter / 20) * max_meter_height)  # Assuming music_meter max is 10

    # Draw the meter background (light purple)
    pygame.draw.rect(screen, (180, 150, 255), (x_pos, y_pos, meter_width, max_meter_height))

    # Draw the filled portion of the meter (darker purple)
    pygame.draw.rect(screen, (100, 0, 180), (x_pos, y_pos + (max_meter_height - meter_fill_height), meter_width, meter_fill_height))

    # Render and draw the "Music Meter" text label
    label_text = font.render("Music", True, (100, 0, 180))  # Purple text color
    label_x = x_pos - (label_text.get_width() // 2) + (meter_width // 2)  # Center text over the meter
    label_y = y_pos - 30  # Position above the meter bar
    screen.blit(label_text, (label_x, label_y))


# Main game loop
def main():
    global hearts_collected, music_meter, societal_value, evil_score, player_speed, start_time
    # Initialize the mixer for sound
    pygame.mixer.init()

    # Load the music file
    
    pygame.mixer.music.load('.dist/assets/bananashake.mp3')

    # Play the music (loop=True will loop the music indefinitely)
    pygame.mixer.music.play(-1, 0.0)  # Loop music indefinitely, starting from the beginning
    pygame.mixer.music.set_volume(0.5)  # Set volume to 50% (default is 1.0)


    # Display intro screen
    show_intro()

    # Initialize game start time
    start_time = pygame.time.get_ticks()
    last_spawn_time = pygame.time.get_ticks()
    last_music_decrement = pygame.time.get_ticks()
    music_decrement_interval = 1000  # Decrease music meter every second

    running = True
    show_popup = False
       
    while running:
       
        screen.blit(background_image, (0, 0))  # Draw the background image
        current_time = pygame.time.get_ticks()

        # Set the music volume based on music_meter (higher music_meter = louder music)
        min_volume = 0.2 # Set a minimum threshold for the volume when the meter is zero
        volume = min(music_meter / 20, 1.0)  # Scale to keep volume in the range [0.0, 1.0]
        volume = max(0.05,music_meter / 20)
        pygame.mixer.music.set_volume(volume)

        # Create a semi-transparent overlay
        dim_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))  # Same size as the screen
        dim_surface.set_alpha(128)  # Set opacity level (0 is fully transparent, 255 is fully opaque)
        dim_surface.fill((0, 0, 0))  # Fill with black or any color for the dimming effect

        # Blit the dimming overlay on top of the background
        screen.blit(dim_surface, (0, 0))
        # Check if game time has expired
        if current_time - start_time >= game_duration:
            running = False
            continue  # Exit game loop and show end screen

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Draw the dynamic colorful background if music is above 0.2
        draw_dynamic_background()


        

        # Spawn objects at random intervals
        if current_time - last_spawn_time > random.randint(1000, 5000):
            spawn_object()
            last_spawn_time = current_time

        # Decrease music meter over time
        if current_time - last_music_decrement >= music_decrement_interval:
            if music_meter > 0:
                music_meter -= 1
                # heart_size -= 1
            last_music_decrement = current_time

        # Call the draw_scoreboard function to display the scoreboard
        # draw_scoreboard()
        draw_volume_meter()
        # Move and draw objects
        for obj in objects:
            obj.move()
            obj.draw()


   
            # Check collision with player
            if not obj.collected and math.hypot(
                    player_pos[0] + player_size // 2 - (obj.pos[0] + obj.size // 2),
                    player_pos[1] + player_size // 2 - (obj.pos[1] + obj.size // 2)
                ) <= (player_size // 2 + obj.size // 2):
                if obj.type == "heart":
                    hearts_collected += 1
                    show_popup = True
                    heart_spawned = False
                elif obj.type == "music_note":
                    music_meter += 5
                    # heart_size += 5
                elif obj.type == "strength":
                    player_speed += 2
                    screen_shake_with_errors(duration=2000, intensity=10)  # Shake the screen for 2 seconds
                    # if player_speed <= 9:
                    #     player_speed += 2
                elif obj.type == "good_element":
                    societal_value += 10
                elif obj.type == "evil":
                    societal_value -= 5
                    evil_score += 1
                obj.collected = True
                
        draw_gauge(screen, societal_value, min_value, max_value, center, radius)
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

        # Update HUD
        font = pygame.font.SysFont(None, 24)
           # Display the popup once if triggered
        if show_popup:
            show_congratulations_popup()
            show_popup = False  # Only show once

        # Update screen and tick the clock
        pygame.display.flip()
        clock.tick(60)

 
    end_game()  # Trigger music change after the game ends
    show_scores()
    # Show end screen after the game loop exits
    show_end()

pygame.mixer.music.stop()
# Run the game
if __name__ == "__main__":
    main()
