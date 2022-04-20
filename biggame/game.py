from cmath import rect
from random import randint
from tracemalloc import start
from turtle import Screen
import pygame
import os, sys


#importar 
dirpath  = os.getcwd()
sys.path.append(dirpath)

if getattr(sys, 'frozen', False):
    os.chdir(sys._MEIPASS)

def display_score():
    current_time = pygame.time.get_ticks()//1000 - start_time
    score_surf = game_font.render(
        f'Score: {current_time}', False, (64, 64, 64))
    score_rect = score_surf.get_rect(center=(400, 50))
    screen.blit(score_surf, score_rect)

    return current_time

# animacao do big
def kadmus_animation():
    global kadmus_surf, kadmus_index

    if kadmus_rect.bottom < 300:
        kadmus_surf = kadmus_jump
    else:
        kadmus_index += 0.1
        if kadmus_index >= len(kadmus_walk):
            kadmus_index = 0
        kadmus_surf = kadmus_walk[int(kadmus_index)]

# move obstacles


def move_obstacles(obstacles_list):
    if obstacles_list:
        for obstacle_rect in obstacles_list:
            obstacle_rect.x -= 5

            if obstacle_rect.bottom == 300:
                screen.blit(granada_surf, obstacle_rect)
            elif obstacle_rect.bottom == 320:
                screen.blit(vanguard_surf, obstacle_rect)
            else:
                screen.blit(nancy_surf, obstacle_rect)

        obstacles_list = [
            obstacle for obstacle in obstacles_list if obstacle.x > -100]
        return obstacles_list
    else:
        return []


def game_collision(player, obstacles):
    if obstacles:
        for obstacle_rect in obstacles:
            if player.colliderect(obstacle_rect):
                return False

    return True


# geral do pygame
pygame.init()
screen = pygame.display.set_mode((800,  400))
pygame.display.set_caption('Big Game')
clock = pygame.time.Clock()

game_font = pygame.font.Font("data/font/Pixeltype.ttf", 50)

# score
score = 0
start_time = 0
the_crews = 0

# game
game_active = False

# ceu  e chao
sky_surf = pygame.image.load('data/imgs/sky/sky.png').convert()
pista_surf = pygame.image.load("data/imgs/pista.png").convert()


# kadmus
kadmus_walk_2 = pygame.image.load(
    "data/imgs/kadmus/kadmus_walk_2.png").convert_alpha()
kadmus_walk_1 = pygame.image.load(
    "data/imgs/kadmus/kadmus_walk_1.png").convert_alpha()
kadmus_walk = [kadmus_walk_2, kadmus_walk_1]
kadmus_index = 0
kadmus_jump = pygame.image.load('data/imgs/kadmus/kadmus_jump.png').convert_alpha()
kadmus_surf = kadmus_walk[kadmus_index]
kadmus_rect = kadmus_surf.get_rect(midbottom=(80, 300))
kadmus_gravity = 0

# obstacles
obstacles_rect_list = []
what_obstacle = []

# granada
granada_frame_1 = pygame.image.load('data/imgs/obs/granada_1.png').convert_alpha()
granada_frame_2 = pygame.image.load('data/imgs/obs/granada_2.png').convert_alpha()
granada_frame_3 = pygame.image.load('data/imgs/obs/granada_3.png').convert_alpha()
granada_frames = [granada_frame_1, granada_frame_2, granada_frame_3]
granada_frame_index = 0
granada_surf = granada_frames[granada_frame_index]
granada_rect = granada_surf.get_rect(bottomright=(600, 300))

# nancy
nancy_surf = pygame.image.load('data/imgs/obs/nancy.png').convert_alpha()

# vanguard
vanguard_surf = pygame.image.load('data/imgs/obs/vanguard.png').convert_alpha()

# the crew 2
the_crew_surf = pygame.image.load(
    "data/imgs/sky/the_crew_2_gratis.png").convert_alpha()
the_crew_rect = the_crew_surf.get_rect(center=(900, 130))

# timer
kadmus_delay = 500
jump = False

obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1500)

granada_animation_timer = pygame.USEREVENT + 2
pygame.time.set_timer(granada_animation_timer, 500)


# loop do jogo
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if game_active:
            if event.type == pygame.KEYDOWN and kadmus_rect.bottom == 300:
                if event.key == pygame.K_SPACE:
                    kadmus_gravity =  -20
                    last = pygame.time.get_ticks()
                    jump = True

            # obstacle  respawn
            if event.type == obstacle_timer:
                if randint(0, 3):
                    obstacles_rect_list.append(granada_surf.get_rect(
                        bottomright=(randint(900,  1100),  300)))
                    what_obstacle.append(granada_surf)
                elif randint(0, 3) == 1:
                    obstacles_rect_list.append(nancy_surf.get_rect(
                        bottomright=(randint(900,  1100),  210)))
                    what_obstacle.append(nancy_surf)
                else:
                    obstacles_rect_list.append(vanguard_surf.get_rect(
                        bottomright=(randint(900,  1100),  320)))
                    what_obstacle.append(vanguard_surf)

            # granada animation
            if event.type == granada_animation_timer:
                if granada_frame_index == 0:
                    granada_frame_index = 1
                elif granada_frame_index == 1:
                    granada_frame_index = 2
                else:
                    granada_frame_index = 0
                granada_surf = granada_frames[granada_frame_index]
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            game_active = True
            the_crews  = 0
            start_time = pygame.time.get_ticks()//1000

    # if jump:
    #     now = pygame.time.get_ticks()
    #     if now >= last + kadmus_delay:
    #         kadmus_gravity = -20
    #         jump = False

    if game_active:
        screen.blit(sky_surf, (0, -100))
        screen.blit(pista_surf, (0, 300))
        screen.blit(the_crew_surf, the_crew_rect)
        score = display_score()

        # animando o player
        kadmus_gravity += 1
        kadmus_rect.y += kadmus_gravity
        if kadmus_rect.bottom >= 300:
            kadmus_rect.bottom = 300
        kadmus_animation()
        screen.blit(kadmus_surf, kadmus_rect)

        # the crew
        if the_crew_rect.x > -100:
            the_crew_rect.x -= 4
        else:
            the_crew_rect.x = 900

        if kadmus_rect.colliderect(the_crew_rect):
            the_crews += 1
            the_crew_rect.x = 900

        # obstacles
        obstacles_rect_list = move_obstacles(obstacles_rect_list)

        # collision
        game_active = game_collision(kadmus_rect,  obstacles_rect_list)
    else:
        screen.fill((94, 129, 162))
        obstacles_rect_list.clear()
        kadmus_rect.midbottom = (80, 300)

        score_messege = game_font.render(
            f'Sua pontuacao: {score}', False, (64, 64, 64))
        score_messege_rect = score_messege.get_rect(center=(220, 330))
        crw_messege = game_font.render(
            f'Voce coletou {the_crews} the Crew', False, (64, 64, 64))
        crw_messege_rect = crw_messege.get_rect(center=(550, 330))

        game_over_text = game_font.render('Big Runner',  False, (64, 64, 64))
        game_over_text_rect = game_over_text.get_rect(center=(400, 50))
        screen.blit(game_over_text, game_over_text_rect)

        kadmus_over = pygame.image.load(
            "data/imgs/obs/nancy.png").convert_alpha()
        kadmus_over = pygame.transform.scale2x(kadmus_over)
        kadmus_over_rect = kadmus_over.get_rect(center=(400, 200))
        screen.blit(kadmus_over,  kadmus_over_rect)

        game_continue_text = game_font.render(
            'Aperte ESPACO para continuar',  False, (64, 64, 64))
        game_continue_text_rect = game_continue_text.get_rect(
            center=(400, 350))

        if score == 0:
            screen.blit(game_continue_text, game_continue_text_rect)
        else:
            screen.blit(score_messege, score_messege_rect)
            screen.blit(crw_messege,  crw_messege_rect)

    pygame.display.update()
    clock.tick(60)
