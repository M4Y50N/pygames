from tracemalloc import start
import pygame
from sys import exit
from random import randint


def display_score():
    current_time = pygame.time.get_ticks()//1000 - start_time
    score_surf = game_font.render(
        f'Score: {current_time}', False, (64, 64, 64))
    score_rect = score_surf.get_rect(center=(400, 50))
    screen.blit(score_surf, score_rect)

    return current_time


def game_over_screen():
    screen.fill((94, 129, 162))
    obstacle_rect_list.clear()
    player_rect.midbottom = (80, 300)

    score_messege = game_font.render(
        f'Sua pontuacao: {score}', False, (64, 64, 64))
    score_messege_rect = score_messege.get_rect(center=(400, 330))

    game_over_text = game_font.render('Big Runner',  False, (64, 64, 64))
    game_over_text_rect = game_over_text.get_rect(center=(400, 50))
    screen.blit(game_over_text, game_over_text_rect)

    player_over = pygame.image.load(
        "graphics/player/player_stand.png").convert_alpha()
    player_over = pygame.transform.scale2x(player_over)
    player_over_rect = player_over.get_rect(center=(400, 200))
    screen.blit(player_over,  player_over_rect)

    game_continue_text = game_font.render(
        'Aperte ESPACO para continuar',  False, (64, 64, 64))
    game_continue_text_rect = game_continue_text.get_rect(center=(400, 350))

    if score == 0:
        screen.blit(game_continue_text, game_continue_text_rect)
    else:
        screen.blit(score_messege, score_messege_rect)


def obstacle_move(obstacle_list):
    if obstacle_list:
        for obstacle_rect in obstacle_list:
            obstacle_rect.x -= 5

            if obstacle_rect.bottom  == 300: screen.blit(snail_surf, obstacle_rect)
            else: screen.blit(fly_surf, obstacle_rect)

        obstacle_list  = [obstacle for obstacle in obstacle_list if  obstacle.x  > -100 ]
        return obstacle_list
    else: return []

def game_collision(player, obstacles):
    if  obstacles:
        for obstacle_rect in obstacles:
            if player.colliderect(obstacle_rect): return False

    return True

def player_animation():
    global player_surf, player_index

    if player_rect.bottom < 300:
        player_surf  = player_jump
    else:
        player_index += 0.1
        if  player_index >= len(player_walk): player_index = 0
        player_surf = player_walk[int(player_index)]

pygame.init()
screen = pygame.display.set_mode((800,  400))
pygame.display.set_caption('Jumper')
clock = pygame.time.Clock()

game_state = False
start_time = 0
score = 0

game_font = pygame.font.Font("font/Pixeltype.ttf", 50)

sky_surf = pygame.image.load("graphics/sky.png").convert_alpha()
ground_surf = pygame.image.load("graphics/ground.png").convert_alpha()

#snail
snail_frame_1 = pygame.image.load("graphics/snail/snail1.png").convert_alpha()
snail_frame_2 = pygame.image.load("graphics/snail/snail2.png").convert_alpha()
snail_frames= [snail_frame_1,  snail_frame_2]
snail_frame_index = 0
snail_surf = snail_frames[snail_frame_index]

#fly
fly_frame_1 = pygame.image.load('graphics/fly/fly1.png').convert_alpha()
fly_frame_2 = pygame.image.load('graphics/fly/fly2.png').convert_alpha()
fly_frames= [fly_frame_1,  fly_frame_2]
fly_frame_index = 0
fly_surf = fly_frames[fly_frame_index]

player_walk_1 = pygame.image.load(
    "graphics/player/player_walk_1.png").convert_alpha()
player_walk_2 = pygame.image.load(
    "graphics/player/player_walk_2.png").convert_alpha()
player_walk = [player_walk_2, player_walk_1]
player_index = 0
player_jump = pygame.image.load('graphics/player/jump.png').convert_alpha()

player_surf = player_walk[player_index]
player_rect = player_surf.get_rect(midbottom=(80, 300))
player_gravity = 0

obstacle_rect_list = []

# timer
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1300)

snail_animation_timer =  pygame.USEREVENT + 2
pygame.time.set_timer(snail_animation_timer, 500)
fly_animation_timer =  pygame.USEREVENT + 3
pygame.time.set_timer(fly_animation_timer, 200)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if game_state:
            if event.type == pygame.MOUSEBUTTONDOWN and player_rect.bottom == 300:
                if pygame.mouse.get_pressed()[0]:
                    player_gravity = -20

            if event.type == pygame.KEYDOWN and player_rect.bottom == 300:
                if event.key == pygame.K_SPACE:
                    player_gravity = -20

            if event.type == obstacle_timer:
                if randint(0,2):
                    obstacle_rect_list.append(snail_surf.get_rect(bottomright = (randint(900,  1100),  300)))
                else:
                    obstacle_rect_list.append(fly_surf.get_rect(bottomright = (randint(900, 1100), 210)))

            if  event.type == snail_animation_timer:
                if snail_frame_index ==  0: snail_frame_index = 1
                else: snail_frame_index = 0
                snail_surf = snail_frames[snail_frame_index]

                if fly_frame_index ==  0: fly_frame_index = 1
                else: fly_frame_index = 0
                fly_surf = fly_frames[fly_frame_index]

        elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            game_state = True
            start_time = pygame.time.get_ticks()//1000



    if game_state:
        screen.blit(sky_surf, (0, 0))
        screen.blit(ground_surf, (0, 300))
        score = display_score()

        # PLayer
        player_gravity += 1
        player_rect.y += player_gravity
        if player_rect.bottom >= 300:
            player_rect.bottom = 300
        player_animation()
        screen.blit(player_surf,  player_rect)

        # Obstacle move
        obstacle_rect_list = obstacle_move(obstacle_rect_list)

        # Collision
        game_state  = game_collision(player_rect, obstacle_rect_list)
            
    else:
        game_over_screen()

    pygame.display.update()
    clock.tick(60)
