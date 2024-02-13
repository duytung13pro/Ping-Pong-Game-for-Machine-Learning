import pygame
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions and initial setup
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
paddle_width, paddle_height = 10, 100
paddle_speed = 10
ball_speed_initial = [5, 5]
ball_size = 10
score_font = pygame.font.Font(None, 36)
high_score = 0

pygame.display.set_caption('Ping Pong')

def draw_text(surface, text, size, x, y):
    font = pygame.font.Font(None, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.center = (x, y)
    surface.blit(text_surface, text_rect)

def ball_reset():
    return SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, ball_speed_initial[0] * -1, ball_speed_initial[1]

def game_over_screen(score1, score2):
    screen.fill(BLACK)
    draw_text(screen, "Game Over", 64, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50)
    draw_text(screen, "Press SPACE to play again or ESC to exit", 24, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    draw_text(screen, f"Final Score: {score1} - {score2}", 36, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50)
    pygame.display.flip()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    waiting = False
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

def game_loop():
    global high_score
    
    paddle1_x, paddle1_y = 10, (SCREEN_HEIGHT - paddle_height) // 2
    paddle2_x, paddle2_y = SCREEN_WIDTH - 10 - paddle_width, (SCREEN_HEIGHT - paddle_height) // 2
    ball_x, ball_y, ball_speed_x, ball_speed_y = ball_reset()
    
    score1, score2 = 0, 0

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] and paddle1_y > 0:
            paddle1_y -= paddle_speed
        if keys[pygame.K_s] and paddle1_y < SCREEN_HEIGHT - paddle_height:
            paddle1_y += paddle_speed
        if keys[pygame.K_UP] and paddle2_y > 0:
            paddle2_y -= paddle_speed
        if keys[pygame.K_DOWN] and paddle2_y < SCREEN_HEIGHT - paddle_height:
            paddle2_y += paddle_speed

        ball_x += ball_speed_x
        ball_y += ball_speed_y

        if ball_y <= 0 or ball_y >= SCREEN_HEIGHT - ball_size:
            ball_speed_y *= -1

        if ball_x <= paddle1_x + paddle_width and paddle1_y < ball_y + ball_size < paddle1_y + paddle_height or \
           ball_x + ball_size >= paddle2_x and paddle2_y < ball_y + ball_size < paddle2_y + paddle_height:
            ball_speed_x *= -1

        if ball_x < 0:
            score2 += 1
            ball_x, ball_y, ball_speed_x, ball_speed_y = ball_reset()
        elif ball_x > SCREEN_WIDTH - ball_size:
            score1 += 1
            ball_x, ball_y, ball_speed_x, ball_speed_y = ball_reset()

        screen.fill(BLACK)
        pygame.draw.rect(screen, WHITE, (paddle1_x, paddle1_y, paddle_width, paddle_height))
        pygame.draw.rect(screen, WHITE, (paddle2_x, paddle2_y, paddle_width, paddle_height))
        pygame.draw.ellipse(screen, WHITE, (ball_x, ball_y, ball_size, ball_size))
        draw_text(screen, f"{score1} - {score2}", 36, SCREEN_WIDTH // 2, 20)

        pygame.display.flip()
        pygame.time.Clock().tick(60)

        if score1 >= 10 or score2 >= 10:  # Example game over condition
            running = False
            game_over_screen(score1, score2)

    # Update high score after game over
    if score1 > high_score:
        high_score = score1
    if score2 > high_score:
        high_score = score2

if __name__ == "__main__":
    while True:
        game_loop()
