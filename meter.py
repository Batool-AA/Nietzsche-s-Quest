

min_value = -100
max_value = 100
center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100)
radius = 50

def draw_gauge(value, min_value, max_value, center, radius):
    normalized_value = (value - min_value) / (max_value - min_value) * 2 - 1
    normalized_value = max(-1, min(1, normalized_value))  # Clamp between -1 and 1

    # Calculate angle for the needle based on the normalized value
    # Angle ranges from pi (left) to 0 (center) to -pi (right)
    angle = math.pi - (normalized_value + 1) * (math.pi / 2)


    # Calculate needle position
    needle_length = radius * 0.8
    needle_x = center[0] + needle_length * math.cos(angle)
    needle_y = center[1] - needle_length * math.sin(angle)

    # Draw arcs for the gauge
    pygame.draw.arc(screen, GREEN, 
                    (center[0] - radius, center[1] - radius, radius * 2, radius * 2), 
                    0, math.pi / 3, 10)

    # Orange Arc: covers the next 60 degrees (from pi/3 to 2pi/3)
    pygame.draw.arc(screen, ORANGE, 
                    (center[0] - radius, center[1] - radius, radius * 2, radius * 2), 
                    math.pi / 3, 2 * math.pi / 3, 10)

    # Green Arc: covers the last 60 degrees (from 2pi/3 to pi)
    pygame.draw.arc(screen, RED, 
                    (center[0] - radius, center[1] - radius, radius * 2, radius * 2), 
                2 * math.pi / 3, math.pi, 10)

    # Draw the needle
    pygame.draw.line(screen, BLACK, center, (needle_x, needle_y), 5)

    # Draw center circle
    pygame.draw.circle(screen, BLACK, center, 10)


#good element
if (societal_value > max_value):
    societal_value = max_value

#evil element
if societal_value < min_value:
    societal_value = min_value

#before defining font
draw_gauge(societal_value, min_value, max_value, center, radius)