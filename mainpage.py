import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up the display
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Start Button Screen")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Load background image
background = pygame.image.load(".dist/assets/3.png")  # Replace with your image
second_screen_bg = pygame.Surface((screen_width, screen_height))  # Create a solid background for the second screen
second_screen_bg.fill((100, 100, 255))  # You can change the color or use another image

# Define font
font = pygame.font.SysFont(None, 48)

# Start button
button_color = (0, 200, 0)
button_rect = pygame.Rect(300, 400, 200, 60)
button_text = font.render("Start", True, WHITE)

# Function to draw the main screen
def draw_main_screen():
    # Draw background image
    screen.blit(background, (0, 0))

    # Draw button
    pygame.draw.rect(screen, button_color, button_rect)
    screen.blit(button_text, (button_rect.x + 60, button_rect.y + 10))

    # Update the display
    pygame.display.update()

# Function to draw the second screen
def draw_second_screen():
    # Draw second screen background
    screen.blit(second_screen_bg, (0, 0))
    # Add more elements to the second screen here if you want
    second_screen_text = font.render("Second Screen", True, BLACK)
    screen.blit(second_screen_text, (screen_width//2 - second_screen_text.get_width()//2, screen_height//2 - second_screen_text.get_height()//2))

    pygame.display.update()

# Main loop
running = True
on_main_screen = True  # Flag to check if we're on the main screen

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Check if the mouse click is on the start button
            if on_main_screen and button_rect.collidepoint(event.pos):
                print("Start Button Clicked!")
                on_main_screen = False  # Switch to the second screen

    # Draw appropriate screen
    if on_main_screen:
        draw_main_screen()
    else:
        draw_second_screen()

# Quit Pygame
pygame.quit()
sys.exit()
