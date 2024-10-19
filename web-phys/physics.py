import pygame
import numpy as np
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 1200, 900  # Increased screen size
CELL_SIZE = 5

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (50, 50, 50)
POWDER_COLOR = (210, 180, 140)
WATER_COLOR = (0, 100, 255)
FIRE_COLOR = (255, 69, 0)
BUTTON_COLOR = (60, 60, 60)
BUTTON_HOVER_COLOR = (100, 100, 100)

# UI settings
UI_HEIGHT = 100  # Height of the bottom UI panel
UI_PADDING = 20

# Pen sizes (1x1, 3x3, 5x5)
PEN_SIZES = [1, 3, 5]
selected_pen_size = 1

# Constants
GRAVITY = 1
FIRE_LIFETIME = 100  # Number of frames fire exists

# Grid dimensions
GRID_WIDTH = WIDTH // CELL_SIZE
GRID_HEIGHT = (HEIGHT - UI_HEIGHT) // CELL_SIZE  # Adjust for the UI height

# Create the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Physics Simulation Game")

# Create a 2D grid (0: empty, 1: powder, 2: water, 3: fire)
grid = np.zeros((GRID_HEIGHT, GRID_WIDTH), dtype=int)
fire_lifetimes = np.zeros((GRID_HEIGHT, GRID_WIDTH), dtype=int)  # Track fire lifetimes

# Clock for controlling frame rate
clock = pygame.time.Clock()

# Currently selected resource (1: powder, 2: water, 3: fire)
selected_resource = 1

# UI Button Rectangles
buttons = {
    "powder": pygame.Rect(UI_PADDING, HEIGHT - UI_HEIGHT + UI_PADDING, 100, 50),
    "water": pygame.Rect(UI_PADDING + 120, HEIGHT - UI_HEIGHT + UI_PADDING, 100, 50),
    "fire": pygame.Rect(UI_PADDING + 240, HEIGHT - UI_HEIGHT + UI_PADDING, 100, 50),
    "pen_size_1": pygame.Rect(WIDTH - 320, HEIGHT - UI_HEIGHT + UI_PADDING, 50, 50),
    "pen_size_3": pygame.Rect(WIDTH - 240, HEIGHT - UI_HEIGHT + UI_PADDING, 50, 50),
    "pen_size_5": pygame.Rect(WIDTH - 160, HEIGHT - UI_HEIGHT + UI_PADDING, 50, 50),
}


def draw_grid():
    """Draw the particles on the screen."""
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            if grid[y, x] == 1:
                pygame.draw.rect(screen, POWDER_COLOR, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
            elif grid[y, x] == 2:
                pygame.draw.rect(screen, WATER_COLOR, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
            elif grid[y, x] == 3:
                pygame.draw.rect(screen, FIRE_COLOR, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))


def update_powder():
    """Apply gravity and displacement behavior to powder particles."""
    for y in range(GRID_HEIGHT - 2, -1, -1):
        for x in range(GRID_WIDTH):
            if grid[y, x] == 1:  # Powder
                if grid[y + 1, x] == 0:  # Move down if empty
                    grid[y + 1, x] = 1
                    grid[y, x] = 0
                elif grid[y + 1, x] == 2:  # Displace water (if powder is above water)
                    grid[y + 1, x] = 1
                    grid[y, x] = 2
                elif x > 0 and grid[y + 1, x - 1] == 0:
                    grid[y + 1, x - 1] = 1
                    grid[y, x] = 0
                elif x < GRID_WIDTH - 1 and grid[y + 1, x + 1] == 0:
                    grid[y + 1, x + 1] = 1
                    grid[y, x] = 0


def update_water():
    """Apply gravity and fluid behavior to water particles."""
    for y in range(GRID_HEIGHT - 2, -1, -1):
        for x in range(GRID_WIDTH):
            if grid[y, x] == 2:  # Water
                if grid[y + 1, x] == 0:  # Move down
                    grid[y + 1, x] = 2
                    grid[y, x] = 0
                elif grid[y + 1, x] == 3:  # Water extinguishes fire
                    grid[y + 1, x] = 2  # Water remains
                    grid[y, x] = 0  # Extinguish the fire
                else:
                    # Try moving left or right
                    directions = []
                    if x > 0 and grid[y, x - 1] == 0:  # Check left
                        directions.append(-1)
                    if x < GRID_WIDTH - 1 and grid[y, x + 1] == 0:  # Check right
                        directions.append(1)

                    if directions:
                        direction = random.choice(directions)
                        grid[y, x + direction] = 2
                        grid[y, x] = 0


def update_fire():
    """Fire particles move randomly upwards and eventually disappear, and burn powder."""
    for y in range(GRID_HEIGHT - 1):
        for x in range(GRID_WIDTH):
            if grid[y, x] == 3:  # Fire
                fire_lifetimes[y, x] -= 1
                if fire_lifetimes[y, x] <= 0:  # Fire extinguishes
                    grid[y, x] = 0
                else:
                    # Burn powder if above or around
                    if y > 0 and grid[y - 1, x] == 1:  # Burn powder above
                        grid[y - 1, x] = 3  # Turn powder to fire
                        fire_lifetimes[y - 1, x] = fire_lifetimes[y, x]  # Spread fire

                    direction = random.choice([-1, 0, 1])  # Random movement
                    if y > 0 and grid[y - 1, x + direction] == 0:
                        grid[y - 1, x + direction] = 3
                        fire_lifetimes[y - 1, x + direction] = fire_lifetimes[y, x]
                        grid[y, x] = 0
                    elif y > 0 and grid[y - 1, x + direction] == 1:  # Fire burns powder
                        grid[y - 1, x + direction] = 3
                        fire_lifetimes[y - 1, x + direction] = fire_lifetimes[y, x]
                        grid[y, x] = 0


def add_particle(pos):
    """Add particles at the mouse position based on the selected resource and pen size."""
    mouse_x, mouse_y = pos
    grid_x = mouse_x // CELL_SIZE
    grid_y = mouse_y // CELL_SIZE

    pen_offset = (selected_pen_size - 1) // 2

    for dy in range(-pen_offset, pen_offset + 1):
        for dx in range(-pen_offset, pen_offset + 1):
            new_x = grid_x + dx
            new_y = grid_y + dy
            if 0 <= new_x < GRID_WIDTH and 0 <= new_y < GRID_HEIGHT:
                if grid[new_y, new_x] == 0:  # Add particle only if the cell is empty
                    grid[new_y, new_x] = selected_resource
                    if selected_resource == 3:  # Set fire lifetime
                        fire_lifetimes[new_y, new_x] = FIRE_LIFETIME


def draw_ui():
    """Draw the UI for resource selection and pen size."""
    font = pygame.font.SysFont("Arial", 20)

    # Draw buttons for Powder, Water, Fire
    for button, label in [("powder", "Powder"), ("water", "Water"), ("fire", "Fire")]:
        rect = buttons[button]
        color = BUTTON_HOVER_COLOR if rect.collidepoint(pygame.mouse.get_pos()) else BUTTON_COLOR
        pygame.draw.rect(screen, color, rect)
        text = font.render(label, True, WHITE)  # Always white text
        screen.blit(text, (rect.x + 10, rect.y + 10))

    # Draw buttons for pen sizes
    for i, size in enumerate(PEN_SIZES):
        button_key = f"pen_size_{size}"
        rect = buttons[button_key]
        color = BUTTON_HOVER_COLOR if rect.collidepoint(pygame.mouse.get_pos()) else BUTTON_COLOR
        pygame.draw.rect(screen, color, rect)
        text = font.render(f"{size}x{size}", True, WHITE)  # Always white text
        screen.blit(text, (rect.x + 5, rect.y + 10))


def handle_ui_click():
    """Handle clicks on the UI buttons."""
    global selected_resource, selected_pen_size

    mouse_pos = pygame.mouse.get_pos()

    # Check if any of the resource buttons are clicked
    if buttons["powder"].collidepoint(mouse_pos):
        selected_resource = 1
    elif buttons["water"].collidepoint(mouse_pos):
        selected_resource = 2
    elif buttons["fire"].collidepoint(mouse_pos):
        selected_resource = 3

    # Check if any of the pen size buttons are clicked
    for size in PEN_SIZES:
        button_key = f"pen_size_{size}"
        if buttons[button_key].collidepoint(mouse_pos):
            selected_pen_size = size


def main():
    global selected_resource
    running = True
    while running:
        screen.fill(BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                handle_ui_click()  # Handle UI click events

        # Add particles on mouse click (outside the UI area)
        if pygame.mouse.get_pressed()[0]:
            mouse_pos = pygame.mouse.get_pos()
            if mouse_pos[1] < HEIGHT - UI_HEIGHT:  # Only add particles outside the UI area
                add_particle(mouse_pos)

        # Update particles
        update_powder()
        update_water()
        update_fire()

        # Draw everything
        draw_grid()
        draw_ui()

        pygame.display.flip()
        clock.tick(60)  # Limit the frame rate to 60 FPS

    pygame.quit()


if __name__ == "__main__":
    main()
