import pygame
import sys
import random
import math

pygame.init()

WIDTH_DISPLAY = 1280
HEIGHT_DISPLAY = 960
ball_size = 30
clock = pygame.time.Clock()

score_font = pygame.font.Font(None, 64)
input_font = pygame.font.Font(None, 48)

# Colors

bg_color = (26, 32, 40)
WHITE = (255, 255, 255)
GREY = (125, 125, 125)

# Elements
player = pygame.Rect(10, HEIGHT_DISPLAY * 0.4, WIDTH_DISPLAY * 0.01, HEIGHT_DISPLAY * 0.2)
opponent = pygame.Rect(WIDTH_DISPLAY - 20, HEIGHT_DISPLAY * 0.4, WIDTH_DISPLAY * 0.01, HEIGHT_DISPLAY * 0.2)
ball = pygame.Rect(WIDTH_DISPLAY / 2 - ball_size / 2, HEIGHT_DISPLAY / 2 - ball_size / 2, ball_size, ball_size)

# Ball speeds
ball_speed_x = 7
ball_speed_y = 7
ball_speed = 7
player_speed = 0
opponent_speed = 0
increment_speed = 1.009

player_points = 0
opponent_points = 0

# Set display
screen = pygame.display.set_mode((WIDTH_DISPLAY, HEIGHT_DISPLAY), pygame.RESIZABLE)

# Title
pygame.display.set_caption('Nebunu\' la Pong')

def get_player_name(prompt):
    name = ""
    while True:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_RETURN and name != "":
                    return name
                elif ev.key == pygame.K_BACKSPACE:
                    name = name[:-1]
                else:
                    # only add printable characters
                    if ev.unicode.isprintable():
                        name += ev.unicode

        # draw the prompt + current name
        screen.fill(bg_color)
        txt = input_font.render(prompt, True, WHITE)
        screen.blit(
            txt,
            txt.get_rect(center=(WIDTH_DISPLAY//2, HEIGHT_DISPLAY//3))
        )
        name_surf = input_font.render(name, True, WHITE)
        screen.blit(
            name_surf,
            name_surf.get_rect(center=(WIDTH_DISPLAY // 2, HEIGHT_DISPLAY // 2))
        )
        pygame.display.flip()
        clock.tick(30)
        
first_time = True

def reset_ball():
    global ball, ball_speed, ball_speed_x, ball_speed_y, first_time
    first_time = True
    ball.x = WIDTH_DISPLAY / 2 - ball_size / 2
    ball.y = HEIGHT_DISPLAY / 2 - ball_size / 2
    random_x = []
    random_y = []
    for i in range(-7, 7):
        if i != 0:
            random_x.append(i)
            random_y.append(i)
            

    angle = random.choice([-7, 7])
    
    ball_speed_x = angle
    ball_speed_y = angle
    ball_speed = 7

def ball_movement():
    
    global ball_speed_x, ball_speed_y, ball, ball_speed, player_points, opponent_points, first_time
   
    
    if first_time == True:
        ball.x = ball.x + ball_speed_x / 2
        ball.y = ball.y + ball_speed_y / 2
    else:
        ball.x = ball.x + ball_speed_x
        ball.y = ball.y + ball_speed_y
    
    if ball.top <= 0 or ball.bottom >= HEIGHT_DISPLAY:
        ball_speed_y *= -1
        ball_speed_x *= increment_speed
        ball_speed_y *= increment_speed
        ball_speed *= increment_speed
        first_time = False
        
    if ball.left <= 0:
        opponent_points += 1;
        reset_ball()
    elif ball.right >= WIDTH_DISPLAY:
        player_points += 1;
        reset_ball()
        
    if ball_speed_x < 0:
        # Is the left edge of the ball at or past the right edge of the paddle
        if ball.left <= player.right:
            # And do they overlap vertically?
            if ball.bottom >= player.top and ball.top <= player.bottom:
                ball_speed_x *= -1
                ball.left = player.right
                ball_speed_x *= increment_speed
                ball_speed_y *= increment_speed
                ball_speed *= increment_speed
                first_time = False

    # Right paddle
    if ball_speed_x > 0:
        # Is the right edge of the ball at or past the left edge of the paddle?
        if ball.right >= opponent.left:
            # And vertical overlap?
            if ball.bottom >= opponent.top and ball.top <= opponent.bottom:
                ball_speed_x *= -1
                ball_speed_x *= increment_speed
                ball_speed_y *= increment_speed
                ball_speed *= increment_speed
                ball.right = opponent.left
                first_time = False


        
player_name   = get_player_name("Enter Player 1 name:")
opponent_name = get_player_name("Enter Player 2 name:")

while True:
    for event in pygame.event.get():
        # Check for quit
        event_type = event.type
        if event_type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            
        if event_type == pygame.KEYDOWN:
            if event.key == pygame.K_s:
                player_speed += ball_speed
            if event.key == pygame.K_w:
                player_speed -= ball_speed
            if event.key == pygame.K_DOWN:
                opponent_speed += ball_speed
            if event.key == pygame.K_UP:
                opponent_speed -= ball_speed
                
        if event_type == pygame.KEYUP:
            if event.key == pygame.K_s:
                player_speed -= ball_speed
            if event.key == pygame.K_w:
                player_speed += ball_speed
            if event.key == pygame.K_DOWN:
                opponent_speed -= ball_speed
            if event.key == pygame.K_UP:
                opponent_speed += ball_speed
                
    if player.top + player_speed >= 0 and player.bottom + player_speed <= HEIGHT_DISPLAY:
        player.y += player_speed
        
    if opponent.top + opponent_speed >= 0 and opponent.bottom + opponent_speed <= HEIGHT_DISPLAY:
        opponent.y += opponent_speed
    
    ball_movement()        
    
    # ------------ DRAWINGS ------------
    screen.fill(bg_color)
    pygame.draw.aaline(screen, GREY, (WIDTH_DISPLAY / 2, 0), (WIDTH_DISPLAY / 2, HEIGHT_DISPLAY))

    # Draw left paddle
    pygame.draw.rect(screen, WHITE, player)

    # Draw right paddle
    pygame.draw.rect(screen, WHITE, opponent)

    # Draw ball
    pygame.draw.ellipse(screen, WHITE, ball)
    
    letter1 = score_font.render(str(player_points), True, (255,255,255), bg_color)
    letter1_rect = letter1.get_rect()

    # 3) Center it on the paddle, and move its bottom just above the paddle top
    letter1_rect.left = WIDTH_DISPLAY / 4
    letter1_rect.top  = 10       # 10px above the paddle
    
    
    letter2 = score_font.render(str(opponent_points), True, (255,255,255), bg_color)
    letter2_rect = letter2.get_rect()

    # 3) Center it on the paddle, and move its bottom just above the paddle top
    letter2_rect.left = WIDTH_DISPLAY - (WIDTH_DISPLAY / 4)
    letter2_rect.top  = 10       # 10px above the paddle
    
    name1 = score_font.render(str(player_name), True, (255, 255, 255), bg_color)
    name1_rect = name1.get_rect()
    name1_rect.left = WIDTH_DISPLAY / 5
    name1_rect.top = HEIGHT_DISPLAY / 15
    
    name2 = score_font.render(str(opponent_name), True, (255, 255, 255), bg_color)
    name2_rect = name2.get_rect()
    name2_rect.left = WIDTH_DISPLAY - (WIDTH_DISPLAY / 3)
    name2_rect.top = HEIGHT_DISPLAY / 15
    
    

    # 4) Blit it
    screen.blit(letter1, letter1_rect)
    screen.blit(letter2, letter2_rect)
    screen.blit(name1, name1_rect)
    screen.blit(name2, name2_rect)

    # Update the game
    pygame.display.flip()
    fps = clock.get_fps()
    clock.tick(120)