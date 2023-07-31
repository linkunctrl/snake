import pygame 
from pygame.locals import *
import random



pygame.init()

screen_width = 600
screen_height = 600

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("SNAKE")

# game variables
cell_size = 10 
direction = 1 # 1 = up, 2 = right, 3 = down, 4 = left
update_snake = 0
food = [0,0] 
new_food = True
new_piece = [0,0]
score = 0
game_over = False
clicked = False
highscore = 0

# define font 
font = pygame.font.SysFont(None, 40)


# create snake (segments)
snake_position = [[int(screen_width/2), int(screen_height/2)]] # will be in the middle
snake_position.append([int(screen_width/2), int(screen_height/2) + cell_size])
snake_position.append([int(screen_width/2), int(screen_height/2) + cell_size * 2])
snake_position.append([int(screen_width/2), int(screen_height/2) + cell_size * 3])

# colours
bg = (245, 210, 158)
body_inner = (50, 175, 25)
body_outer = (100, 100, 200)
green = (0, 255, 0)
food_colour = (200, 50, 53)
black = (0, 0, 0)
grey = (96, 96, 96)
blue = (10, 32, 250)

again_rect = Rect(screen_width // 2 - 80, screen_height // 2, 160, 50)



def draw_screen():
    screen.fill(bg)

def draw_score():
    score_txt = "SCORE: " + str(score)
    score_img = font.render(score_txt, True, black)
    screen.blit(score_img, (0,0)) # top left
   
def draw_highcore():
    highscore_txt = "HIGHSCORE: " + str(highscore)
    highscore_img = font.render(highscore_txt, True, black)
    screen.blit(highscore_img, (0,30))

def check_game_over(game_over):
    # if snake has eaten itself
    head_count = 0
    for segment in snake_position:
        if snake_position[0] == segment and head_count > 0:
            game_over = True
        head_count += 1 
    return game_over

def draw_game_over():
    over_txt = "Game over!"
    over_img = font.render(over_txt,True, black)
    pygame.draw.rect(screen, grey, (screen_width // 2 - 80, screen_height // 2 - 60, 160, 50))
    screen.blit(over_img, (screen_width // 2 - 80, screen_height // 2 - 50))

    again_txt = "Play again."
    again_img = font.render(again_txt, True, black)
    pygame.draw.rect(screen, grey, again_rect)
    screen.blit(again_img, (screen_width // 2 - 80, screen_height // 2 + 10))



run = True
while run:
    draw_screen()
    draw_score()
    draw_highcore()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w and direction != 3:
                direction = 1
            elif event.key == pygame.K_d and direction != 4:
                direction = 2
            elif event.key == pygame.K_s and direction != 1:
                direction = 3
            elif event.key == pygame.K_a and direction != 2:
                direction = 4

    if game_over == False:
        if update_snake > 99:
            update_snake = 0
            snake_position = snake_position[-1:] + snake_position[:-1]

            if direction == 1:
                snake_position[0][0] = snake_position[1][0]
                snake_position[0][1] = snake_position[1][1] - cell_size

            if direction == 3:
                snake_position[0][0] = snake_position[1][0]
                snake_position[0][1] = snake_position[1][1] + cell_size

            if direction == 2:
                snake_position[0][1] = snake_position[1][1]
                snake_position[0][0] = snake_position[1][0] + cell_size

            if direction == 4:
                snake_position[0][1] = snake_position[1][1]
                snake_position[0][0] = snake_position[1][0] - cell_size
            
            game_over = check_game_over(game_over)

    if game_over == True:
        draw_game_over()
        if event.type == pygame.MOUSEBUTTONDOWN and clicked == False:
            clicked = True
        if event.type == pygame.MOUSEBUTTONDOWN and clicked == True:
            clicked = False
            pos = pygame.mouse.get_pos()
            if again_rect.collidepoint(pos):
                direction = 1 # 1 = up, 2 = right, 3 = down, 4 = left
                update_snake = 0
                food = [0,0] 
                new_food = True
                new_piece = [0,0]
                score = 0
                game_over = False

                # create snake (segments)
                snake_position = [[int(screen_width/2), int(screen_height/2)]] # will be in the middle
                snake_position.append([int(screen_width/2), int(screen_height/2) + cell_size])
                snake_position.append([int(screen_width/2), int(screen_height/2) + cell_size * 2])
                snake_position.append([int(screen_width/2), int(screen_height/2) + cell_size * 3])



    if score > highscore:
        score = highscore
    
    if new_food == True:
        new_food = False
        food[0] = cell_size * random.randint(0, (screen_width / cell_size) - 1)    
        food[1] = cell_size * random.randint(0, (screen_height / cell_size) - 1)   

    # draw food
    pygame.draw.rect(screen, food_colour, (food[0], food[1], cell_size, cell_size))
     
    # if food has been eaten
    if snake_position[0] == food: # snake_pos[0] is the head of the snake
        new_food = True
        # increase the snake's length 
        new_piece = list(snake_position[-1])
        if direction == 1:
            new_piece[1] += cell_size
        if direction == 3:
            new_piece[1] -= cell_size
        if direction == 2:
            new_piece[0] -= cell_size
        if direction == 4:
            new_piece[0] += cell_size
        snake_position.append(new_piece)
# update score
        score += 1
        highscore += 1 



    # draw snake
    head = 1
    for x in snake_position:
        if head == 0:
           pygame.draw.rect(screen, body_outer, (x[0], x[1], cell_size, cell_size))
           pygame.draw.rect(screen, body_inner, (x[0] + 1, x[1] + 1, cell_size - 2, cell_size - 2))
        if head == 1:
           pygame.draw.rect(screen, body_outer, (x[0], x[1], cell_size, cell_size))
           pygame.draw.rect(screen, green, (x[0] + 1, x[1] + 1, cell_size - 2, cell_size - 2))
           head = 0


    pygame.display.update()

    update_snake += 1 #speed

pygame.quit()
