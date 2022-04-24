import pygame
from sys import exit
from random import randint

def display_score():
    current_time = int(pygame.time.get_ticks() / 1000) - start_time
    score_surf = test_font.render(f'Score: {current_time}',False,(64,64,64))
    score_rect = score_surf.get_rect(center = (400,50))
    screen.blit(score_surf,score_rect)
    return current_time

def obstacle_movement(obstacle_list):
    if obstacle_list:
        for obstacle_rect in obstacle_list:
            obstacle_rect.x -= 5

            if obstacle_rect.bottom == 300:
                screen.blit(snail_surface,obstacle_rect)
            else:
                screen.blit(flie_surface,obstacle_rect)

        obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.x > -100]

        return obstacle_list
    else: return []

def collisions(player, obstacles):
    if obstacles:
        for obstacle_rect in obstacles:
            if player.colliderect(obstacle_rect): return False
    return True



pygame.init()
screen = pygame.display.set_mode((800,400))
pygame.display.set_caption('My first pygame')
clock = pygame.time.Clock()
test_font = pygame.font.Font(None, 50)
game_active = False
start_time = 0

sky_surface = pygame.Surface((800,400)).convert()
sky_surface.fill('deepskyblue1'),False, ((64,64,64))
#score_rect = score_surf.get_rect(center = (400,50))

snail_surface = pygame.Surface((50,50)).convert_alpha()
snail_surface.fill('Red')


flie_surface = pygame.Surface((50,50)).convert_alpha()
flie_surface.fill('darkorchid4')

menu_surf = test_font.render('Press space to play', False, (64, 64, 64))
menu_rect = menu_surf.get_rect(center = (400,320))

square_runner_surf = test_font.render('SQUARE RUNNER', False, (64, 64, 64))
square_runner_rect = square_runner_surf.get_rect(center=(400, 75))
score = 0

obstacle_rect_list = []

player_surf = pygame.Surface((50,50)).convert_alpha()
player_surf.fill('gold1')
player_rect = player_surf.get_rect(topleft = (80,250))

player_gravity = 0
player_stand = pygame.Surface((100,100)).convert_alpha()
player_stand.fill('gold1')
player_stand_rect = player_stand.get_rect(center = (400,200))

ground_surface = pygame.Surface((800,100)).convert()
ground_surface.fill('green')

obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer,1500)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if game_active:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if player_rect.collidepoint(event.pos):
                    player_gravity = -20

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player_rect.bottom >= 300:
                    player_gravity = -20
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True

                start_time = int(pygame.time.get_ticks() / 1000)

        if event.type == obstacle_timer and game_active:
            if randint(0,2):
                obstacle_rect_list.append(snail_surface.get_rect(bottomright = (randint(900,1100),300)))
            else:
                obstacle_rect_list.append(flie_surface.get_rect(bottomright=(randint(900, 1100), 210)))


    if game_active:
        screen.blit(sky_surface,(0, 0))
        screen.blit(ground_surface,(0,300))
        #pygame.draw.rect(screen,'#c0e8ec',score_rect)
        #pygame.draw.rect(screen, '#c0e8ec', score_rect, 10)
        ##pygame.draw.ellipse(screen,'Brown',pygame.Rect(50,200,100,100))
        #screen.blit(score_surf,score_rect)
        score = display_score()

        #snail_rect.x -= 4
        #if snail_rect.right <= 0: snail_rect.left = 800
        #screen.blit(snail_surface,snail_rect)

        #Player
        player_gravity += 1
        player_rect.y += player_gravity
        if player_rect.bottom >= 300: player_rect.bottom = 300
        screen.blit(player_surf,player_rect)

        obstacle_rect_list = obstacle_movement(obstacle_rect_list)


        game_active = collisions(player_rect,obstacle_rect_list)

    else:
        screen.fill((94,129,162))
        screen.blit(player_stand,player_stand_rect)
        screen.blit(square_runner_surf, square_runner_rect)
        obstacle_rect_list.clear()
        player_rect.midbottom = (80,300)
        player_gravity = 0

        score_message = test_font.render(f'Your score: {score}', False, (64, 64, 64))
        score_message_rect = score_message.get_rect(center=(400, 330))

        if score == 0:
            screen.blit(menu_surf, menu_rect)
        else:
            screen.blit(score_message,score_message_rect)

    pygame.display.update()
    clock.tick(60)