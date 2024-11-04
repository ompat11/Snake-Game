import pygame
import random
import math
from pygame import mixer

# pygame setup
pygame.init()
square_width = 800
screen = pygame.display.set_mode([square_width] * 2)
clock = pygame.time.Clock()
icon = pygame.image.load("icon.png")
pygame.display.set_icon(icon)
pygame.display.set_caption("Snake Game")
running = True
game_over = False

# Define Colors
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)

# Define Font
font = pygame.font.Font('freesansbold.ttf', 32)  # For displaying score
over_font = pygame.font.Font('freesansbold.ttf', 64)  # For displaying "Game Over"

# Playground settings
pixel_width = 50

def generate_starting_position():
    position_range = (pixel_width // 2, square_width - pixel_width // 2, pixel_width)
    return [random.randrange(*position_range), random.randrange(*position_range)]

# Snake settings
snake_pixel = pygame.Rect(0, 0, pixel_width, pixel_width)
snake_pixel.center = generate_starting_position()
snake = [pygame.Rect(snake_pixel)]
snake_direction = (0, 0)
snake_length = 1

# Target settings
target = pygame.Rect(0, 0, pixel_width, pixel_width)
target.center = generate_starting_position()

# Background music
mixer.music.load('snake_game_music.mp3')
mixer.music.play(-1)


def reset():
    target.center = generate_starting_position()
    snake_pixel.center = generate_starting_position()
    return [pygame.Rect(snake_pixel)]

def is_out_of_bounds():
    return (snake_pixel.bottom > square_width or snake_pixel.top < 0 or
            snake_pixel.left < 0 or snake_pixel.right > square_width)

def check_collision(rect_list):
    for rect in rect_list[:-1]:  # Check if the snake collides with itself
        if rect.colliderect(snake_pixel):
            return True
    return False

def show_score(score):
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

def game_over_screen(score):
    game_over_text = over_font.render("Game Over", True, WHITE)
    score_text = font.render(f"Final Score: {score}", True, WHITE)
    restart_text = font.render("Press R to Restart or Q to Quit", True, WHITE)
    screen.fill(BLACK)
    screen.blit(game_over_text, (square_width // 2 - game_over_text.get_width() // 2, square_width // 2 - game_over_text.get_height() * 2))
    screen.blit(score_text, (square_width // 2 - score_text.get_width() // 2, square_width // 2 - score_text.get_height() // 2))
    screen.blit(restart_text, (square_width // 2 - restart_text.get_width() // 2, square_width // 2 + score_text.get_height()))
    pygame.display.flip()

def handle_game_over():
    global running, game_over
    while game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                game_over = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:  # Restart the game
                    reset_game()
                    return
                elif event.key == pygame.K_q:  # Quit the game
                    running = False
                    game_over = False

def reset_game():
    global snake, snake_pixel, snake_direction, snake_length, target, game_over
    snake_pixel = pygame.Rect(0, 0, pixel_width, pixel_width)
    snake_pixel.center = generate_starting_position()
    snake = [pygame.Rect(snake_pixel)]
    snake_direction = (0, 0)
    snake_length = 1
    target = pygame.Rect(0, 0, pixel_width, pixel_width)
    target.center = generate_starting_position()
    game_over = False

# Main game loop
while running:
    if game_over:
        game_over_screen(snake_length - 1)
        handle_game_over()
        continue

    # Poll for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Fill the screen with a color to wipe away anything from last frame
    screen.fill(BLACK)

    # Check for out-of-bounds or self-collision
    if is_out_of_bounds() or check_collision(snake):
        game_over = True

    # Handle input for snake direction
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP] and snake_direction != (0, pixel_width):
        snake_direction = (0, - pixel_width)
    if keys[pygame.K_DOWN] and snake_direction != (0, -pixel_width):
        snake_direction = (0, pixel_width)
    if keys[pygame.K_LEFT] and snake_direction != (pixel_width, 0):
        snake_direction = (- pixel_width, 0)
    if keys[pygame.K_RIGHT] and snake_direction != (- pixel_width, 0):
        snake_direction = (pixel_width, 0)

    # Move the snake
    if snake_direction != (0, 0):
        # Create a new head position
        new_head = pygame.Rect(snake_pixel.move(snake_direction))
        snake_pixel = new_head

        # Add new head to the snake
        snake.append(pygame.Rect(snake_pixel))

        # Keep the length of the snake
        if len(snake) > snake_length:
            snake.pop(0)  # Remove the oldest part of the snake

    # Check for eating the target
    if snake_pixel.center == target.center:
        target.center = generate_starting_position()
        snake_length += 1

    # Render the snake and the target
    for snake_part in snake:
        pygame.draw.rect(screen, GREEN, snake_part)
    pygame.draw.rect(screen, RED, target)

    # Display score
    show_score(snake_length - 1)  # Score is snake_length - 1

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(9)  # Adjust the FPS as needed

pygame.quit()
