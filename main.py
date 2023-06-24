# Importing the Modules

import pygame
from pygame import mixer
import math
import random

# Variables for spawning the enemies

min_x = 1200
max_x = 2000

min_y = 30
max_y = 500

# Variables for the health powerup spawning

health_min_x, health_max_x = 3500, 6000


def enemy_behavior(enemy_rect, enemy_mask_image, bullet_mask_image, enemy_bullet_rect, enemy_bullet, enemy_surface,
                   bullet_speed, ship_speed, player_health_inside, score_inside, enemy_hit, bullet_stop, bullet_x,
                   bullet_y, player_bullet_shot, player_bullet_follow_player):

    # Drawing the enemies

    screen.blit(bullet_mask_image, enemy_bullet_rect)
    screen.blit(enemy_bullet, enemy_bullet_rect)

    screen.blit(enemy_mask_image, enemy_rect)
    screen.blit(enemy_surface, enemy_rect)

    true_bullet_speed = bullet_speed

    # Enemy 1 movement / enemy 1 bullet movement

    enemy_rect.x -= ship_speed

    if not enemy_hit:

        enemy_bullet_rect.x -= bullet_speed

    if enemy_hit:

        enemy_bullet_rect.x -= bullet_speed

        if enemy_bullet_rect.right < 0:

            bullet_speed = 0

            bullet_stop = True

    if bullet_stop:

        enemy_bullet_rect.x = enemy_rect.x + bullet_x

        enemy_bullet_rect.y = enemy_rect.y + bullet_y

        bullet_speed = true_bullet_speed

        bullet_stop = False

        enemy_hit = False

    # Checks if enemy 1 bullet goes off-screen

    if enemy_rect.x >= 500:

        if enemy_bullet_rect.x < -200:

            enemy_bullet_rect.x = enemy_rect.x + bullet_x

    else:

        if enemy_bullet_rect.x < -400:

            enemy_bullet_rect.x = enemy_rect.x + bullet_x

    # Checks if enemy 1 ship goes off-screen

    if enemy_rect.x < -100:

        enemy_rect.x = random.randint(min_x, max_x)

        enemy_rect.y = random.randint(min_y, max_y)

        enemy_bullet_rect.x = enemy_rect.x + bullet_x

        enemy_bullet_rect.y = enemy_rect.y + bullet_y

    # Checking for collisions with the player bullet and the enemy ship

    for ship in enemy_ship_list:

        if bullet_mask.overlap(ship, (enemy_rect.x - player_bullet_rect.x, enemy_rect.y - player_bullet_rect.y)):

            enemy_rect.x = random.randint(min_x, max_x)

            enemy_rect.y = random.randint(min_y, max_y)

            score_inside += 1

            player_hitting_enemy.play()

            enemy_hit = True

            player_bullet_rect.x = player_rect.x + 17

            player_bullet_rect.y = player_rect.y + 17

            player_bullet_shot = False

            player_bullet_follow_player = True

            if enemy_bullet_rect.x > enemy_rect.x:

                enemy_bullet_rect.x = enemy_rect.x + bullet_x

                enemy_bullet_rect.y = enemy_rect.y + bullet_y

    # Checking for collisions with the player ship and the enemy ship

    for ship in enemy_ship_list:

        if player_mask.overlap(ship, (enemy_rect.x - player_rect.x, enemy_rect.y - player_rect.y)):

            enemy_rect.x = random.randint(min_x, max_x)

            enemy_rect.y = random.randint(min_y, max_y)

            player_health_inside -= 25

            player_getting_hit.play()

            enemy_hit = True

            if enemy_bullet_rect.x > enemy_rect.x:

                enemy_bullet_rect.x = enemy_rect.x + bullet_x

                enemy_bullet_rect.y = enemy_rect.y + bullet_y

    # Checking for collisions with the enemy bullet and the player

    for bullet in enemy_bullet_list:

        if bullet.overlap(player_mask, (player_rect.x - enemy_bullet_rect.x, player_rect.y - enemy_bullet_rect.y)):

            player_health_inside -= 25

            player_getting_hit.play()

            enemy_bullet_rect.x = enemy_rect.x + bullet_x

            enemy_bullet_rect.y = enemy_rect.y + bullet_y

    return player_health_inside, score_inside, bullet_speed, bullet_stop, enemy_hit, player_bullet_shot, player_bullet_follow_player


def display_score():  # Function to display scores

    player_score_surface = game_font.render(f' Score: {score}', False, color)
    player_score_rect = player_score_surface.get_rect(center=(75, 40))
    screen.blit(player_score_surface, player_score_rect)


def display_health():  # Function to display the player health

    player_health_surface = game_font.render(f' Health: {player_health}%', False, color)
    player_health_rect = player_health_surface.get_rect(center=(500, 40))
    screen.blit(player_health_surface, player_health_rect)


def title_screen():  # Function to display the title screen

    title_screen_title_surface = title_screen_font.render(f' Space Shooter', False, color)
    title_screen_title_rect = title_screen_title_surface.get_rect(center=(500, 100))
    screen.blit(title_screen_title_surface, title_screen_title_rect)

    title_screen_play = title_screen_font_play_message.render(f' Press "Space" to Play!', False, color)
    title_screen_play_rect = title_screen_play.get_rect(center=(500, 500))
    screen.blit(title_screen_play, title_screen_play_rect)

    screen.blit(player_surface_rotated, ((screen_width / 2) - 500, screen_height / 2))


def game_over_screen():  # Function to display the game over screen

    game_over_screen_score = title_screen_font_play_message.render(f' You destroyed {score} ship(s)', False, color)
    game_over_screen_score_rect = game_over_screen_score.get_rect(center=(500, 100))
    screen.blit(game_over_screen_score, game_over_screen_score_rect)

    game_over_screen_play = title_screen_font_play_message.render(f' Press "Space" to Restart', False, color)
    game_over_screen_play_rect = game_over_screen_play.get_rect(center=(500, 500))
    screen.blit(game_over_screen_play, game_over_screen_play_rect)


pygame.init()  # Starts pygame

pygame.display.set_caption('Space Shooter')  # Sets the caption for the display screen

# Constant Variables

color = (255, 0, 0)  # Sets the color variable to red

clock = pygame.time.Clock()  # Part of managing FPS

screen_width = 1000
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))  # Creates the display screen

scroll = 0

# Background

background_image = pygame.image.load('Space/PNG/Space_Stars4.png').convert_alpha()

background_image_scaled = pygame.transform.scale(background_image, (screen_width, screen_height))

bg_width = background_image_scaled.get_width()

tiles = math.ceil((screen_width / bg_width)) + 1

# Player Assets #

# Full Health
player_surface = pygame.image.load('Foozle_2DS0011_Void_MainShip/Main Ship/Main Ship - Bases/PNGs/Main Ship - Base - '
                                   'Full health.png').convert_alpha()
player_surface_scaled = pygame.transform.scale(player_surface, (75, 75))
player_surface_rotated = pygame.transform.rotate(player_surface_scaled, 270)

# Slightly Damaged
player_surface_slight_damaged = pygame.image.load('Foozle_2DS0011_Void_MainShip/Main Ship/Main Ship - Bases/PNGs/Main '
                                                  'Ship - Base - Slight damage.png').convert_alpha()
player_surface_slight_damaged_scaled = pygame.transform.scale(player_surface_slight_damaged, (75, 75))
player_surface_slight_damaged_rotated = pygame.transform.rotate(player_surface_slight_damaged_scaled, 270)

# Damaged
player_surface_damaged = pygame.image.load('Foozle_2DS0011_Void_MainShip/Main Ship/Main Ship - Bases/PNGs/Main Ship - '
                                           'Base - Damaged.png').convert_alpha()
player_surface_damaged_scaled = pygame.transform.scale(player_surface_damaged, (75, 75))
player_surface_damaged_rotated = pygame.transform.rotate(player_surface_damaged_scaled, 270)

# Very Damaged
player_surface_very_damaged = pygame.image.load('Foozle_2DS0011_Void_MainShip/Main Ship/Main Ship - Bases/PNGs/Main '
                                                'Ship - Base - Very damaged.png').convert_alpha()
player_surface_very_damaged_scaled = pygame.transform.scale(player_surface_very_damaged, (75, 75))
player_surface_very_damaged_rotated = pygame.transform.rotate(player_surface_very_damaged_scaled, 270)

player_rect = player_surface_rotated.get_rect(center=((screen_width / 2) - 425, (screen_height / 2)))

player_mask = pygame.mask.from_surface(player_surface_rotated)
player_mask_image = player_mask.to_surface()
player_mask_image.set_colorkey((0, 0, 0))

player_movement = pygame.mixer.Sound('select_2-96163.mp3')
player_movement.set_volume(0.4)

player_health = 100

score = 0

player_speed = 25

# Bullet Assets

bullet_surface = pygame.image.load('Sprites - Lasers Bullets #1 [66]v2.5/Laser Sprites/11.png').convert_alpha()
bullet_surface_scaled = pygame.transform.scale(bullet_surface, (40, 40))
player_bullet_rect = bullet_surface_scaled.get_rect(center=((screen_width / 2) - 425, (screen_height / 2)))

bullet_mask = pygame.mask.from_surface(bullet_surface_scaled)
player_bullet_mask_image = bullet_mask.to_surface()
player_bullet_mask_image.set_colorkey((0, 0, 0))

player_bullet_speed = 10

# Collision related sounds

bullet_sound = pygame.mixer.Sound('laser-gun-81720.mp3')
bullet_sound.set_volume(0.3)

player_hitting_enemy = pygame.mixer.Sound('8-bit-fireball-81148.mp3')
player_hitting_enemy.set_volume(0.5)

player_getting_hit = pygame.mixer.Sound('vibrating-thud-39536.mp3')
player_getting_hit.set_volume(1.0)

# Health Powerup

health_powerup_x_pos = random.randint(health_min_x, health_max_x)
health_powerup_y_pos = random.randint(min_y, max_y)

health_powerup_surface = pygame.image.load('Item 3-1 copy.png.png').convert_alpha()
health_powerup_surface_scaled = pygame.transform.scale(health_powerup_surface, (85, 85))
health_powerup_surface_rect = health_powerup_surface_scaled.get_rect(center=(health_powerup_x_pos, health_powerup_y_pos))

health_powerup_mask = pygame.mask.from_surface(health_powerup_surface_scaled)
health_powerup_mask_image = health_powerup_mask.to_surface()
health_powerup_mask_image.set_colorkey((0, 0, 0))

powerup_sound = pygame.mixer.Sound('video-game-powerup-38065 copy.mp3')
powerup_sound.set_volume(0.4)

health_powerup_speed = 7.5

# Font assets

game_font = pygame.font.Font('Minecraft copy.ttf', 25)

title_screen_font_play_message = pygame.font.Font('Minecraft copy.ttf', 50)

title_screen_font = pygame.font.Font('Minecraft copy.ttf', 75)

# Enemy Assets #

# Enemy 1 #

# Enemy 1-1

enemy_1_x = random.randint(min_x, max_x)
enemy_1_y = random.randint(min_y, max_y)

enemy_1_surface = pygame.image.load('free-pixel-art-enemy-spaceship-2d-sprites/PNG_Parts&Spriter_Animation/Ship1'
                                    '/Ship1.png').convert_alpha()
enemy_1_surface_flipped = pygame.transform.flip(enemy_1_surface, True, False)
enemy_1_rect = enemy_1_surface_flipped.get_rect(center=(enemy_1_x, enemy_1_y))

enemy_1_mask = pygame.mask.from_surface(enemy_1_surface_flipped)
enemy_1_mask_image = enemy_1_mask.to_surface()
enemy_1_mask_image.set_colorkey((0, 0, 0))

enemy_1_bullet_surface = pygame.image.load('Sprites - Lasers Bullets #1 [66]v2.5/Laser Sprites/16.png').convert_alpha()
enemy_1_bullet_scaled = pygame.transform.scale(enemy_1_bullet_surface, (40, 40))
enemy_1_bullet_flipped = pygame.transform.flip(enemy_1_bullet_scaled, True, False)
enemy_1_bullet_rect = enemy_1_bullet_flipped.get_rect(center=(enemy_1_rect.x + 32, enemy_1_rect.y + 32))

enemy_1_bullet_mask = pygame.mask.from_surface(enemy_1_bullet_flipped)
enemy_1_bullet_mask_image = enemy_1_bullet_mask.to_surface()
enemy_1_bullet_mask_image.set_colorkey((0, 0, 0))

enemy_1_bullet_speed = 10
enemy_1_ship_speed = 4

enemy_1_bullet_x = 20
enemy_1_bullet_y = 13

enemy_1_hit = False

enemy_1_bullet_stop = False

# Enemy 1-2 (Enemy 7)

enemy_7_x = random.randint(min_x, max_x)
enemy_7_y = random.randint(min_y, max_y)

enemy_7_surface = pygame.image.load('free-pixel-art-enemy-spaceship-2d-sprites/PNG_Parts&Spriter_Animation/Ship1'
                                    '/Ship1.png').convert_alpha()
enemy_7_surface_flipped = pygame.transform.flip(enemy_7_surface, True, False)
enemy_7_rect = enemy_7_surface_flipped.get_rect(center=(enemy_7_x, enemy_7_y))

enemy_7_mask = pygame.mask.from_surface(enemy_7_surface_flipped)
enemy_7_mask_image = enemy_7_mask.to_surface()
enemy_7_mask_image.set_colorkey((0, 0, 0))

enemy_7_bullet_surface = pygame.image.load('Sprites - Lasers Bullets #1 [66]v2.5/Laser Sprites/16.png').convert_alpha()
enemy_7_bullet_scaled = pygame.transform.scale(enemy_7_bullet_surface, (40, 40))
enemy_7_bullet_flipped = pygame.transform.flip(enemy_7_bullet_scaled, True, False)
enemy_7_bullet_rect = enemy_7_bullet_flipped.get_rect(center=(enemy_7_rect.x + 32, enemy_7_rect.y + 32))

enemy_7_bullet_mask = pygame.mask.from_surface(enemy_7_bullet_flipped)
enemy_7_bullet_mask_image = enemy_7_bullet_mask.to_surface()
enemy_7_bullet_mask_image.set_colorkey((0, 0, 0))

enemy_7_bullet_speed = 9
enemy_7_ship_speed = 6

enemy_7_bullet_x = 20
enemy_7_bullet_y = 13

enemy_7_hit = False

enemy_7_bullet_stop = False

# Enemy 2 #

# Enemy 2-1

enemy_2_x = random.randint(min_x, max_x)
enemy_2_y = random.randint(min_y, max_y)

enemy_2_surface = pygame.image.load('free-pixel-art-enemy-spaceship-2d-sprites/PNG_Parts&Spriter_Animation/Ship2'
                                    '/Ship2.png').convert_alpha()
enemy_2_surface_flipped = pygame.transform.flip(enemy_2_surface, True, False)
enemy_2_rect = enemy_2_surface_flipped.get_rect(center=(enemy_2_x, enemy_2_y))

enemy_2_mask = pygame.mask.from_surface(enemy_2_surface_flipped)
enemy_2_mask_image = enemy_2_mask.to_surface()
enemy_2_mask_image.set_colorkey((0, 0, 0))

enemy_2_bullet_surface = pygame.image.load('Sprites - Lasers Bullets #1 [66]v2.5/Laser Sprites/12.png').convert_alpha()
enemy_2_bullet_scaled = pygame.transform.scale(enemy_2_bullet_surface, (40, 40))
enemy_2_bullet_flipped = pygame.transform.flip(enemy_2_bullet_scaled, True, False)
enemy_2_bullet_rect = enemy_2_bullet_flipped.get_rect(center=(enemy_2_rect.x + 32, enemy_2_rect.y + 63))

enemy_2_bullet_mask = pygame.mask.from_surface(enemy_2_bullet_flipped)
enemy_2_bullet_mask_image = enemy_2_bullet_mask.to_surface()
enemy_2_bullet_mask_image.set_colorkey((0, 0, 0))

enemy_2_bullet_speed = 9
enemy_2_ship_speed = 5

enemy_2_bullet_x = 30
enemy_2_bullet_y = 42

enemy_2_hit = False

enemy_2_bullet_stop = False

# Enemy 2-2 (Enemy 8)

enemy_8_x = random.randint(min_x, max_x)
enemy_8_y = random.randint(min_y, max_y)

enemy_8_surface = pygame.image.load('free-pixel-art-enemy-spaceship-2d-sprites/PNG_Parts&Spriter_Animation/Ship2'
                                    '/Ship2.png').convert_alpha()
enemy_8_surface_flipped = pygame.transform.flip(enemy_8_surface, True, False)
enemy_8_rect = enemy_8_surface_flipped.get_rect(center=(enemy_8_x, enemy_8_y))

enemy_8_mask = pygame.mask.from_surface(enemy_8_surface_flipped)
enemy_8_mask_image = enemy_8_mask.to_surface()
enemy_8_mask_image.set_colorkey((0, 0, 0))

enemy_8_bullet_surface = pygame.image.load('Sprites - Lasers Bullets #1 [66]v2.5/Laser Sprites/12.png').convert_alpha()
enemy_8_bullet_scaled = pygame.transform.scale(enemy_8_bullet_surface, (40, 40))
enemy_8_bullet_flipped = pygame.transform.flip(enemy_8_bullet_scaled, True, False)
enemy_8_bullet_rect = enemy_8_bullet_flipped.get_rect(center=(enemy_8_rect.x + 32, enemy_8_rect.y + 63))

enemy_8_bullet_mask = pygame.mask.from_surface(enemy_8_bullet_flipped)
enemy_8_bullet_mask_image = enemy_8_bullet_mask.to_surface()
enemy_8_bullet_mask_image.set_colorkey((0, 0, 0))

enemy_8_bullet_speed = 7
enemy_8_ship_speed = 4

enemy_8_bullet_x = 30
enemy_8_bullet_y = 42

enemy_8_hit = False

enemy_8_bullet_stop = False

# Enemy 3 #

# Enemy 3-1

enemy_3_x = random.randint(min_x, max_x)
enemy_3_y = random.randint(min_y, max_y)

enemy_3_surface = pygame.image.load('free-pixel-art-enemy-spaceship-2d-sprites/PNG_Parts&Spriter_Animation/Ship3'
                                    '/Ship3.png').convert_alpha()
enemy_3_surface_flipped = pygame.transform.flip(enemy_3_surface, True, False)
enemy_3_rect = enemy_3_surface_flipped.get_rect(center=(enemy_3_x, enemy_3_y))

enemy_3_mask = pygame.mask.from_surface(enemy_3_surface_flipped)
enemy_3_mask_image = enemy_3_mask.to_surface()
enemy_3_mask_image.set_colorkey((0, 0, 0))

enemy_3_bullet_surface = pygame.image.load('Sprites - Lasers Bullets #1 [66]v2.5/Laser Sprites/14.png').convert_alpha()
enemy_3_bullet_scaled = pygame.transform.scale(enemy_3_bullet_surface, (40, 40))
enemy_3_bullet_flipped = pygame.transform.flip(enemy_3_bullet_scaled, True, False)
enemy_3_bullet_rect = enemy_3_bullet_flipped.get_rect(center=(enemy_3_rect.x + 32, enemy_3_rect.y + 69))

enemy_3_bullet_mask = pygame.mask.from_surface(enemy_3_bullet_flipped)
enemy_3_bullet_mask_image = enemy_3_bullet_mask.to_surface()
enemy_3_bullet_mask_image.set_colorkey((0, 0, 0))

enemy_3_bullet_speed = 8
enemy_3_ship_speed = 4

enemy_3_bullet_x = 30
enemy_3_bullet_y = 49

enemy_3_hit = False

enemy_3_bullet_stop = False

# Enemy 3-2 (Enemy 9)

enemy_9_x = random.randint(min_x, max_x)
enemy_9_y = random.randint(min_y, max_y)

enemy_9_surface = pygame.image.load('free-pixel-art-enemy-spaceship-2d-sprites/PNG_Parts&Spriter_Animation/Ship3'
                                    '/Ship3.png').convert_alpha()
enemy_9_surface_flipped = pygame.transform.flip(enemy_9_surface, True, False)
enemy_9_rect = enemy_9_surface_flipped.get_rect(center=(enemy_9_x, enemy_9_y))

enemy_9_mask = pygame.mask.from_surface(enemy_9_surface_flipped)
enemy_9_mask_image = enemy_9_mask.to_surface()
enemy_9_mask_image.set_colorkey((0, 0, 0))

enemy_9_bullet_surface = pygame.image.load('Sprites - Lasers Bullets #1 [66]v2.5/Laser Sprites/14.png').convert_alpha()
enemy_9_bullet_scaled = pygame.transform.scale(enemy_9_bullet_surface, (40, 40))
enemy_9_bullet_flipped = pygame.transform.flip(enemy_9_bullet_scaled, True, False)
enemy_9_bullet_rect = enemy_9_bullet_flipped.get_rect(center=(enemy_9_rect.x + 32, enemy_9_rect.y + 69))

enemy_9_bullet_mask = pygame.mask.from_surface(enemy_9_bullet_flipped)
enemy_9_bullet_mask_image = enemy_9_bullet_mask.to_surface()
enemy_9_bullet_mask_image.set_colorkey((0, 0, 0))

enemy_9_bullet_speed = 9
enemy_9_ship_speed = 6

enemy_9_bullet_x = 30
enemy_9_bullet_y = 49

enemy_9_hit = False

enemy_9_bullet_stop = False

# Enemy 4 #

# Enemy 4-1

enemy_4_x = random.randint(min_x, max_x)
enemy_4_y = random.randint(min_y, max_y)

enemy_4_surface = pygame.image.load('free-pixel-art-enemy-spaceship-2d-sprites/PNG_Parts&Spriter_Animation/Ship4'
                                    '/Ship4.png').convert_alpha()
enemy_4_surface_flipped = pygame.transform.flip(enemy_4_surface, True, False)
enemy_4_rect = enemy_4_surface_flipped.get_rect(center=(enemy_4_x, enemy_4_y))

enemy_4_mask = pygame.mask.from_surface(enemy_4_surface_flipped)
enemy_4_mask_image = enemy_4_mask.to_surface()
enemy_4_mask_image.set_colorkey((0, 0, 0))

enemy_4_bullet_surface = pygame.image.load('Sprites - Lasers Bullets #1 [66]v2.5/Laser Sprites/18.png').convert_alpha()
enemy_4_bullet_scaled = pygame.transform.scale(enemy_4_bullet_surface, (40, 40))
enemy_4_bullet_flipped = pygame.transform.flip(enemy_4_bullet_scaled, True, False)
enemy_4_bullet_rect = enemy_4_bullet_flipped.get_rect(center=(enemy_4_rect.x + 32, enemy_4_rect.y + 67))

enemy_4_bullet_mask = pygame.mask.from_surface(enemy_4_bullet_flipped)
enemy_4_bullet_mask_image = enemy_4_bullet_mask.to_surface()
enemy_4_bullet_mask_image.set_colorkey((0, 0, 0))

enemy_4_bullet_speed = 8
enemy_4_ship_speed = 3

enemy_4_bullet_x = 30
enemy_4_bullet_y = 47

enemy_4_hit = False

enemy_4_bullet_stop = False

# Enemy 4-2 (Enemy 10)

enemy_10_x = random.randint(min_x, max_x)
enemy_10_y = random.randint(min_y, max_y)

enemy_10_surface = pygame.image.load('free-pixel-art-enemy-spaceship-2d-sprites/PNG_Parts&Spriter_Animation/Ship4'
                                     '/Ship4.png').convert_alpha()
enemy_10_surface_flipped = pygame.transform.flip(enemy_10_surface, True, False)
enemy_10_rect = enemy_10_surface_flipped.get_rect(center=(enemy_10_x, enemy_10_y))

enemy_10_mask = pygame.mask.from_surface(enemy_10_surface_flipped)
enemy_10_mask_image = enemy_10_mask.to_surface()
enemy_10_mask_image.set_colorkey((0, 0, 0))

enemy_10_bullet_surface = pygame.image.load('Sprites - Lasers Bullets #1 [66]v2.5/Laser Sprites/18.png').convert_alpha()
enemy_10_bullet_scaled = pygame.transform.scale(enemy_10_bullet_surface, (40, 40))
enemy_10_bullet_flipped = pygame.transform.flip(enemy_10_bullet_scaled, True, False)
enemy_10_bullet_rect = enemy_10_bullet_flipped.get_rect(center=(enemy_10_rect.x + 32, enemy_10_rect.y + 67))

enemy_10_bullet_mask = pygame.mask.from_surface(enemy_10_bullet_flipped)
enemy_10_bullet_mask_image = enemy_10_bullet_mask.to_surface()
enemy_10_bullet_mask_image.set_colorkey((0, 0, 0))

enemy_10_bullet_speed = 9
enemy_10_ship_speed = 5

enemy_10_bullet_x = 30
enemy_10_bullet_y = 47

enemy_10_hit = False

enemy_10_bullet_stop = False

# Enemy 5 #

# Enemy 5-1

enemy_5_x = random.randint(min_x, max_x)
enemy_5_y = random.randint(min_y, max_y)

enemy_5_surface = pygame.image.load('free-pixel-art-enemy-spaceship-2d-sprites/PNG_Parts&Spriter_Animation/Ship5'
                                    '/Ship5.png').convert_alpha()
enemy_5_surface_flipped = pygame.transform.flip(enemy_5_surface, True, False)
enemy_5_rect = enemy_5_surface_flipped.get_rect(center=(enemy_5_x, enemy_5_y))

enemy_5_mask = pygame.mask.from_surface(enemy_5_surface_flipped)
enemy_5_mask_image = enemy_5_mask.to_surface()
enemy_5_mask_image.set_colorkey((0, 0, 0))

enemy_5_bullet_surface = pygame.image.load('Sprites - Lasers Bullets #1 [66]v2.5/Laser Sprites/18.png').convert_alpha()
enemy_5_bullet_scaled = pygame.transform.scale(enemy_5_bullet_surface, (40, 40))
enemy_5_bullet_flipped = pygame.transform.flip(enemy_5_bullet_scaled, True, False)
enemy_5_bullet_rect = enemy_5_bullet_flipped.get_rect(center=(enemy_5_rect.x + 32, enemy_5_rect.y + 71))

enemy_5_bullet_mask = pygame.mask.from_surface(enemy_5_bullet_flipped)
enemy_5_bullet_mask_image = enemy_5_bullet_mask.to_surface()
enemy_5_bullet_mask_image.set_colorkey((0, 0, 0))

enemy_5_bullet_speed = 7
enemy_5_ship_speed = 2

enemy_5_bullet_x = 30
enemy_5_bullet_y = 51

enemy_5_hit = False

enemy_5_bullet_stop = False

# Enemy 5-2 (Enemy 11)

enemy_11_x = random.randint(min_x, max_x)
enemy_11_y = random.randint(min_y, max_y)

enemy_11_surface = pygame.image.load('free-pixel-art-enemy-spaceship-2d-sprites/PNG_Parts&Spriter_Animation/Ship5'
                                     '/Ship5.png').convert_alpha()
enemy_11_surface_flipped = pygame.transform.flip(enemy_11_surface, True, False)
enemy_11_rect = enemy_11_surface_flipped.get_rect(center=(enemy_11_x, enemy_11_y))

enemy_11_mask = pygame.mask.from_surface(enemy_11_surface_flipped)
enemy_11_mask_image = enemy_11_mask.to_surface()
enemy_11_mask_image.set_colorkey((0, 0, 0))

enemy_11_bullet_surface = pygame.image.load('Sprites - Lasers Bullets #1 [66]v2.5/Laser Sprites/18.png').convert_alpha()
enemy_11_bullet_scaled = pygame.transform.scale(enemy_11_bullet_surface, (40, 40))
enemy_11_bullet_flipped = pygame.transform.flip(enemy_11_bullet_scaled, True, False)
enemy_11_bullet_rect = enemy_11_bullet_flipped.get_rect(center=(enemy_11_rect.x + 32, enemy_11_rect.y + 71))

enemy_11_bullet_mask = pygame.mask.from_surface(enemy_11_bullet_flipped)
enemy_11_bullet_mask_image = enemy_11_bullet_mask.to_surface()
enemy_11_bullet_mask_image.set_colorkey((0, 0, 0))

enemy_11_bullet_speed = 7
enemy_11_ship_speed = 4

enemy_11_bullet_x = 30
enemy_11_bullet_y = 51

enemy_11_hit = False

enemy_11_bullet_stop = False

# Enemy 6 #

# Enemy 6-1

enemy_6_x = random.randint(min_x, max_x)
enemy_6_y = random.randint(min_y, max_y)

enemy_6_surface = pygame.image.load('free-pixel-art-enemy-spaceship-2d-sprites/PNG_Parts&Spriter_Animation/Ship6'
                                    '/Ship6.png').convert_alpha()
enemy_6_surface_flipped = pygame.transform.flip(enemy_6_surface, True, False)
enemy_6_rect = enemy_6_surface_flipped.get_rect(center=(enemy_6_x, enemy_6_y))

enemy_6_mask = pygame.mask.from_surface(enemy_6_surface_flipped)
enemy_6_mask_image = enemy_6_mask.to_surface()
enemy_6_mask_image.set_colorkey((0, 0, 0))

enemy_6_bullet_surface = pygame.image.load('Sprites - Lasers Bullets #1 [66]v2.5/Laser Sprites/13.png').convert_alpha()
enemy_6_bullet_scaled = pygame.transform.scale(enemy_6_bullet_surface, (40, 40))
enemy_6_bullet_flipped = pygame.transform.flip(enemy_6_bullet_scaled, True, False)
enemy_6_bullet_rect = enemy_6_bullet_flipped.get_rect(center=(enemy_6_rect.x + 32, enemy_6_rect.y + 64))

enemy_6_bullet_mask = pygame.mask.from_surface(enemy_6_bullet_flipped)
enemy_6_bullet_mask_image = enemy_6_bullet_mask.to_surface()
enemy_6_bullet_mask_image.set_colorkey((0, 0, 0))

enemy_6_bullet_speed = 10
enemy_6_ship_speed = 1

enemy_6_bullet_x = 30
enemy_6_bullet_y = 44

enemy_6_hit = False

enemy_6_bullet_stop = False

# Enemy 6-2 (Enemy 12)

enemy_12_x = random.randint(min_x, max_x)
enemy_12_y = random.randint(min_y, max_y)

enemy_12_surface = pygame.image.load('free-pixel-art-enemy-spaceship-2d-sprites/PNG_Parts&Spriter_Animation/Ship6'
                                     '/Ship6.png').convert_alpha()
enemy_12_surface_flipped = pygame.transform.flip(enemy_12_surface, True, False)
enemy_12_rect = enemy_12_surface_flipped.get_rect(center=(enemy_12_x, enemy_12_y))

enemy_12_mask = pygame.mask.from_surface(enemy_12_surface_flipped)
enemy_12_mask_image = enemy_12_mask.to_surface()
enemy_12_mask_image.set_colorkey((0, 0, 0))

enemy_12_bullet_surface = pygame.image.load('Sprites - Lasers Bullets #1 [66]v2.5/Laser Sprites/13.png').convert_alpha()
enemy_12_bullet_scaled = pygame.transform.scale(enemy_12_bullet_surface, (40, 40))
enemy_12_bullet_flipped = pygame.transform.flip(enemy_12_bullet_scaled, True, False)
enemy_12_bullet_rect = enemy_12_bullet_flipped.get_rect(center=(enemy_12_rect.x + 32, enemy_12_rect.y + 64))

enemy_12_bullet_mask = pygame.mask.from_surface(enemy_12_bullet_flipped)
enemy_12_bullet_mask_image = enemy_12_bullet_mask.to_surface()
enemy_12_bullet_mask_image.set_colorkey((0, 0, 0))

enemy_12_bullet_speed = 8
enemy_12_ship_speed = 3

enemy_12_bullet_x = 30
enemy_12_bullet_y = 44

enemy_12_hit = False

enemy_12_bullet_stop = False

# Flag Variables

bullet_shot = False

bullet_follow_player = True

game_active = False

end_screen_music = False

# List of all enemy ships

enemy_ship_list = [enemy_1_mask, enemy_2_mask, enemy_3_mask, enemy_4_mask, enemy_5_mask, enemy_6_mask, enemy_7_mask,
                   enemy_8_mask, enemy_9_mask, enemy_10_mask, enemy_11_mask, enemy_12_mask]

# List of all enemy bullet

enemy_bullet_list = [enemy_1_bullet_mask, enemy_2_bullet_mask, enemy_3_bullet_mask, enemy_4_bullet_mask,
                     enemy_5_bullet_mask, enemy_6_bullet_mask, enemy_7_bullet_mask, enemy_8_bullet_mask,
                     enemy_9_bullet_mask, enemy_10_bullet_mask, enemy_11_bullet_mask, enemy_12_bullet_mask]

# Playing the menu music

mixer.music.load('Space Music Pack/menu.wav')  # Loads the game music
pygame.mixer.music.play(-1)  # Plays the game music on loop
pygame.mixer.music.set_volume(0.3)  # Sets the music volume

while True:

    # Creating the background

    screen.fill((0, 0, 0))

    for i in range(0, tiles):

        screen.blit(background_image_scaled, (i * bg_width + scroll, 0))

    # Scrolling the background

    scroll -= 5

    if abs(scroll) > bg_width:

        scroll = 0

    # Event Loop

    for event in pygame.event.get():  # Checks if the user closes the game

        if event.type == pygame.QUIT:

            pygame.quit()

            exit()

        if game_active:

            # Checking for user input (other than exiting)

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_UP:

                    player_rect.y -= player_speed

                    player_movement.play()

                    if bullet_follow_player:

                        player_bullet_rect.y -= player_speed

                if event.key == pygame.K_DOWN:

                    player_rect.y += player_speed

                    player_movement.play()

                    if bullet_follow_player:

                        player_bullet_rect.y += player_speed

                if event.key == pygame.K_LEFT:

                    player_rect.x -= player_speed

                    player_movement.play()

                    if bullet_follow_player:

                        player_bullet_rect.x -= player_speed

                if event.key == pygame.K_RIGHT:

                    player_rect.x += player_speed

                    player_movement.play()

                    if bullet_follow_player:

                        player_bullet_rect.x += player_speed

                if event.key == pygame.K_SPACE:

                    if not bullet_shot:

                        bullet_sound.play()

                    bullet_shot = True

                    bullet_follow_player = False

        else:

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_SPACE:

                    pygame.mixer.music.stop()

                    mixer.music.load('beyond-video-game-soundtrack-side-scrolling-shooter-arcade-147696.mp3')
                    pygame.mixer.music.play(-1)  # Plays the game music on loop
                    pygame.mixer.music.set_volume(0.3)  # Sets the music volume

                    game_active = True

                    # Resetting the game #

                    # Resetting the player stats

                    score = 0

                    player_health = 100

                    # Resetting the player flags

                    bullet_shot = False

                    bullet_follow_player = True

                    end_screen_music = False

                    # Resetting the player position

                    player_rect.x = (screen_width / 2) - 500

                    player_rect.y = (screen_height / 2)

                    player_bullet_rect.x = (screen_width / 2) - 480

                    player_bullet_rect.y = (screen_height / 2) + 18

                    # Resetting the powerup position

                    health_powerup_surface_rect.x = random.randint(health_min_x, health_max_x)
                    health_powerup_surface_rect.y = random.randint(min_y, max_y)

                    # Resetting the enemy positions

                    enemy_1_rect.x = random.randint(min_x, max_x)
                    enemy_1_rect.y = random.randint(min_y, max_y)
                    enemy_1_bullet_rect.x = enemy_1_rect.x + 10
                    enemy_1_bullet_rect.y = enemy_1_rect.y + 12

                    enemy_7_rect.x = random.randint(min_x, max_x)
                    enemy_7_rect.y = random.randint(min_y, max_y)
                    enemy_7_bullet_rect.x = enemy_7_rect.x + 10
                    enemy_7_bullet_rect.y = enemy_7_rect.y + 12

                    enemy_2_rect.x = random.randint(min_x, max_x)
                    enemy_2_rect.y = random.randint(min_y, max_y)
                    enemy_2_bullet_rect.x = enemy_2_rect.x
                    enemy_2_bullet_rect.y = enemy_2_rect.y + 44

                    enemy_8_rect.x = random.randint(min_x, max_x)
                    enemy_8_rect.y = random.randint(min_y, max_y)
                    enemy_8_bullet_rect.x = enemy_8_rect.x
                    enemy_8_bullet_rect.y = enemy_8_rect.y + 44

                    enemy_3_rect.x = random.randint(min_x, max_x)
                    enemy_3_rect.y = random.randint(min_y, max_y)
                    enemy_3_bullet_rect.x = enemy_3_rect.x
                    enemy_3_bullet_rect.y = enemy_3_rect.y + 49

                    enemy_9_rect.x = random.randint(min_x, max_x)
                    enemy_9_rect.y = random.randint(min_y, max_y)
                    enemy_9_bullet_rect.x = enemy_9_rect.x
                    enemy_9_bullet_rect.y = enemy_9_rect.y + 49

                    enemy_4_rect.x = random.randint(min_x, max_x)
                    enemy_4_rect.y = random.randint(min_y, max_y)
                    enemy_4_bullet_rect.x = enemy_4_rect.x
                    enemy_4_bullet_rect.y = enemy_4_rect.y + 48

                    enemy_10_rect.x = random.randint(min_x, max_x)
                    enemy_10_rect.y = random.randint(min_y, max_y)
                    enemy_10_bullet_rect.x = enemy_10_rect.x
                    enemy_10_bullet_rect.y = enemy_10_rect.y + 48

                    enemy_5_rect.x = random.randint(min_x, max_x)
                    enemy_5_rect.y = random.randint(min_y, max_y)
                    enemy_5_bullet_rect.x = enemy_5_rect.x
                    enemy_5_bullet_rect.y = enemy_5_rect.y + 51

                    enemy_11_rect.x = random.randint(min_x, max_x)
                    enemy_11_rect.y = random.randint(min_y, max_y)
                    enemy_11_bullet_rect.x = enemy_11_rect.x
                    enemy_11_bullet_rect.y = enemy_11_rect.y + 51

                    enemy_6_rect.x = random.randint(min_x, max_x)
                    enemy_6_rect.y = random.randint(min_y, max_y)
                    enemy_6_bullet_rect.x = enemy_6_rect.x
                    enemy_6_bullet_rect.y = enemy_6_rect.y + 44

                    enemy_12_rect.x = random.randint(min_x, max_x)
                    enemy_12_rect.y = random.randint(min_y, max_y)
                    enemy_12_bullet_rect.x = enemy_12_rect.x
                    enemy_12_bullet_rect.y = enemy_12_rect.y + 44

    if game_active:

        # Health powerup positioning and movement

        screen.blit(health_powerup_mask_image, health_powerup_surface_rect)
        screen.blit(health_powerup_surface_scaled, health_powerup_surface_rect)

        health_powerup_surface_rect.x -= health_powerup_speed

        if health_powerup_surface_rect.x < -100:

            health_powerup_surface_rect.x = random.randint(health_min_x, health_max_x)
            health_powerup_surface_rect.y = random.randint(min_y, max_y)

        if health_powerup_mask.overlap(player_mask, (player_rect.x - health_powerup_surface_rect.x, player_rect.y - health_powerup_surface_rect.y)):

            if player_health < 100:

                powerup_sound.play()

                player_health += 25

                health_powerup_surface_rect.x = random.randint(health_min_x, health_max_x)
                health_powerup_surface_rect.y = random.randint(min_y, max_y)

            else:

                pass

        # Checks to see if the bullet is shot

        if bullet_shot:

            player_bullet_rect.x += player_bullet_speed

        # Checks to see if the bullet goes off-screen

        if player_bullet_rect.x >= screen_width:

            player_bullet_rect.x = player_rect.x + 17

            player_bullet_rect.y = player_rect.y + 17

            bullet_shot = False

            bullet_follow_player = True

        # Drawing the bullet

        screen.blit(player_bullet_mask_image, player_bullet_rect)
        screen.blit(bullet_surface_scaled, player_bullet_rect)

        # Drawing the player

        if player_health == 100:

            screen.blit(player_mask_image, player_rect)
            screen.blit(player_surface_rotated, player_rect)

        elif player_health == 75:

            screen.blit(player_mask_image, player_rect)
            screen.blit(player_surface_slight_damaged_rotated, player_rect)

        elif player_health == 50:

            screen.blit(player_mask_image, player_rect)
            screen.blit(player_surface_damaged_rotated, player_rect)

        else:

            screen.blit(player_mask_image, player_rect)
            screen.blit(player_surface_very_damaged_rotated, player_rect)

        # Displaying the Health and Score

        display_score()

        display_health()

        # Functions foe the enemies

        # Enemy 1 #

        player_stats_enemy_1 = enemy_behavior(enemy_1_rect, enemy_1_mask_image, enemy_1_bullet_mask_image,
                                              enemy_1_bullet_rect, enemy_1_bullet_flipped, enemy_1_surface_flipped,
                                              enemy_1_bullet_speed, enemy_1_ship_speed, player_health, score,
                                              enemy_1_hit, enemy_1_bullet_stop, enemy_1_bullet_x, enemy_1_bullet_y,
                                              bullet_shot, bullet_follow_player)  # Function for enemy 1

        # Calculating the returned items

        player_health = player_stats_enemy_1[0]

        score = player_stats_enemy_1[1]

        enemy_1_bullet_speed = player_stats_enemy_1[2]

        enemy_1_bullet_stop = player_stats_enemy_1[3]

        enemy_1_hit = player_stats_enemy_1[4]

        bullet_shot = player_stats_enemy_1[5]

        bullet_follow_player = player_stats_enemy_1[6]

        # Enemy 7 #

        player_stats_enemy_7 = enemy_behavior(enemy_7_rect, enemy_7_mask_image, enemy_7_bullet_mask_image,
                                              enemy_7_bullet_rect, enemy_7_bullet_flipped, enemy_7_surface_flipped,
                                              enemy_7_bullet_speed, enemy_7_ship_speed, player_health, score,
                                              enemy_7_hit, enemy_7_bullet_stop, enemy_7_bullet_x, enemy_7_bullet_y,
                                              bullet_shot, bullet_follow_player)  # Function for enemy 1

        # Calculating the returned items

        player_health = player_stats_enemy_7[0]

        score = player_stats_enemy_7[1]

        enemy_7_bullet_speed = player_stats_enemy_7[2]

        enemy_7_bullet_stop = player_stats_enemy_7[3]

        enemy_7_hit = player_stats_enemy_7[4]

        bullet_shot = player_stats_enemy_7[5]

        bullet_follow_player = player_stats_enemy_7[6]

        # Enemy 2 #

        player_stats_enemy_2 = enemy_behavior(enemy_2_rect, enemy_2_mask_image, enemy_2_bullet_mask_image,
                                              enemy_2_bullet_rect, enemy_2_bullet_flipped, enemy_2_surface_flipped,
                                              enemy_2_bullet_speed, enemy_2_ship_speed, player_health, score,
                                              enemy_2_hit, enemy_2_bullet_stop, enemy_2_bullet_x, enemy_2_bullet_y,
                                              bullet_shot, bullet_follow_player)  # Function for enemy 2

        # Calculating the returned items

        player_health = player_stats_enemy_2[0]

        score = player_stats_enemy_2[1]

        enemy_2_bullet_speed = player_stats_enemy_2[2]

        enemy_2_bullet_stop = player_stats_enemy_2[3]

        enemy_2_hit = player_stats_enemy_2[4]

        bullet_shot = player_stats_enemy_2[5]

        bullet_follow_player = player_stats_enemy_2[6]

        # Enemy 8 #

        player_stats_enemy_8 = enemy_behavior(enemy_8_rect, enemy_8_mask_image, enemy_8_bullet_mask_image,
                                              enemy_8_bullet_rect, enemy_8_bullet_flipped, enemy_8_surface_flipped,
                                              enemy_8_bullet_speed, enemy_8_ship_speed, player_health, score,
                                              enemy_8_hit, enemy_8_bullet_stop, enemy_8_bullet_x, enemy_8_bullet_y,
                                              bullet_shot, bullet_follow_player)  # Function for enemy 2

        # Calculating the returned items

        player_health = player_stats_enemy_8[0]

        score = player_stats_enemy_8[1]

        enemy_8_bullet_speed = player_stats_enemy_8[2]

        enemy_8_bullet_stop = player_stats_enemy_8[3]

        enemy_8_hit = player_stats_enemy_8[4]

        bullet_shot = player_stats_enemy_8[5]

        bullet_follow_player = player_stats_enemy_8[6]

        # Enemy 3 #

        player_stats_enemy_3 = enemy_behavior(enemy_3_rect, enemy_3_mask_image, enemy_3_bullet_mask_image,
                                              enemy_3_bullet_rect, enemy_3_bullet_flipped, enemy_3_surface_flipped,
                                              enemy_3_bullet_speed, enemy_3_ship_speed, player_health, score,
                                              enemy_3_hit, enemy_3_bullet_stop, enemy_3_bullet_x, enemy_3_bullet_y,
                                              bullet_shot, bullet_follow_player)  # Function for enemy 3

        # Calculating the returned items

        player_health = player_stats_enemy_3[0]

        score = player_stats_enemy_3[1]

        enemy_3_bullet_speed = player_stats_enemy_3[2]

        enemy_3_bullet_stop = player_stats_enemy_3[3]

        enemy_3_hit = player_stats_enemy_3[4]

        bullet_shot = player_stats_enemy_3[5]

        bullet_follow_player = player_stats_enemy_3[6]

        # Enemy 9 #

        player_stats_enemy_9 = enemy_behavior(enemy_9_rect, enemy_9_mask_image, enemy_9_bullet_mask_image,
                                              enemy_9_bullet_rect, enemy_9_bullet_flipped, enemy_9_surface_flipped,
                                              enemy_9_bullet_speed, enemy_9_ship_speed, player_health, score,
                                              enemy_9_hit, enemy_9_bullet_stop, enemy_9_bullet_x, enemy_9_bullet_y,
                                              bullet_shot, bullet_follow_player)  # Function for enemy 3

        # Calculating the returned items

        player_health = player_stats_enemy_9[0]

        score = player_stats_enemy_9[1]

        enemy_9_bullet_speed = player_stats_enemy_9[2]

        enemy_9_bullet_stop = player_stats_enemy_9[3]

        enemy_9_hit = player_stats_enemy_9[4]

        bullet_shot = player_stats_enemy_9[5]

        bullet_follow_player = player_stats_enemy_9[6]

        # Enemy 4 #

        player_stats_enemy_4 = enemy_behavior(enemy_4_rect, enemy_4_mask_image, enemy_4_bullet_mask_image,
                                              enemy_4_bullet_rect, enemy_4_bullet_flipped, enemy_4_surface_flipped,
                                              enemy_4_bullet_speed, enemy_4_ship_speed, player_health, score,
                                              enemy_4_hit, enemy_4_bullet_stop, enemy_4_bullet_x, enemy_4_bullet_y,
                                              bullet_shot, bullet_follow_player)  # Function for enemy 3

        # Calculating the returned items

        player_health = player_stats_enemy_4[0]

        score = player_stats_enemy_4[1]

        enemy_4_bullet_speed = player_stats_enemy_4[2]

        enemy_4_bullet_stop = player_stats_enemy_4[3]

        enemy_4_hit = player_stats_enemy_4[4]

        bullet_shot = player_stats_enemy_4[5]

        bullet_follow_player = player_stats_enemy_4[6]

        # Enemy 10 #

        player_stats_enemy_10 = enemy_behavior(enemy_10_rect, enemy_10_mask_image, enemy_10_bullet_mask_image,
                                               enemy_10_bullet_rect, enemy_10_bullet_flipped, enemy_10_surface_flipped,
                                               enemy_10_bullet_speed, enemy_10_ship_speed, player_health, score,
                                               enemy_10_hit, enemy_10_bullet_stop, enemy_10_bullet_x, enemy_10_bullet_y,
                                               bullet_shot, bullet_follow_player)  # Function for enemy 3

        # Calculating the returned items

        player_health = player_stats_enemy_10[0]

        score = player_stats_enemy_10[1]

        enemy_10_bullet_speed = player_stats_enemy_10[2]

        enemy_10_bullet_stop = player_stats_enemy_10[3]

        enemy_10_hit = player_stats_enemy_10[4]

        bullet_shot = player_stats_enemy_10[5]

        bullet_follow_player = player_stats_enemy_10[6]

        # Enemy 5 #

        player_stats_enemy_5 = enemy_behavior(enemy_5_rect, enemy_5_mask_image, enemy_5_bullet_mask_image,
                                              enemy_5_bullet_rect, enemy_5_bullet_flipped, enemy_5_surface_flipped,
                                              enemy_5_bullet_speed, enemy_5_ship_speed, player_health, score,
                                              enemy_5_hit, enemy_5_bullet_stop, enemy_5_bullet_x, enemy_5_bullet_y,
                                              bullet_shot, bullet_follow_player)  # Function for enemy 3

        # Calculating the returned items

        player_health = player_stats_enemy_5[0]

        score = player_stats_enemy_5[1]

        enemy_5_bullet_speed = player_stats_enemy_5[2]

        enemy_5_bullet_stop = player_stats_enemy_5[3]

        enemy_5_hit = player_stats_enemy_5[4]

        bullet_shot = player_stats_enemy_5[5]

        bullet_follow_player = player_stats_enemy_5[6]

        # Enemy 11 #

        player_stats_enemy_11 = enemy_behavior(enemy_11_rect, enemy_11_mask_image, enemy_11_bullet_mask_image,
                                               enemy_11_bullet_rect, enemy_11_bullet_flipped, enemy_11_surface_flipped,
                                               enemy_11_bullet_speed, enemy_11_ship_speed, player_health, score,
                                               enemy_11_hit, enemy_11_bullet_stop, enemy_11_bullet_x, enemy_11_bullet_y,
                                               bullet_shot, bullet_follow_player)  # Function for enemy 3

        # Calculating the returned items

        player_health = player_stats_enemy_11[0]

        score = player_stats_enemy_11[1]

        enemy_11_bullet_speed = player_stats_enemy_11[2]

        enemy_11_bullet_stop = player_stats_enemy_11[3]

        enemy_11_hit = player_stats_enemy_11[4]

        bullet_shot = player_stats_enemy_11[5]

        bullet_follow_player = player_stats_enemy_11[6]

        # Enemy 6 #

        player_stats_enemy_6 = enemy_behavior(enemy_6_rect, enemy_6_mask_image, enemy_6_bullet_mask_image,
                                              enemy_6_bullet_rect, enemy_6_bullet_flipped, enemy_6_surface_flipped,
                                              enemy_6_bullet_speed, enemy_6_ship_speed, player_health, score,
                                              enemy_6_hit, enemy_6_bullet_stop, enemy_6_bullet_x, enemy_6_bullet_y,
                                              bullet_shot, bullet_follow_player)  # Function for enemy 3

        # Calculating the returned items

        player_health = player_stats_enemy_6[0]

        score = player_stats_enemy_6[1]

        enemy_6_bullet_speed = player_stats_enemy_6[2]

        enemy_6_bullet_stop = player_stats_enemy_6[3]

        enemy_6_hit = player_stats_enemy_6[4]

        bullet_shot = player_stats_enemy_6[5]

        bullet_follow_player = player_stats_enemy_6[6]

        # Enemy 12 #

        player_stats_enemy_12 = enemy_behavior(enemy_12_rect, enemy_12_mask_image, enemy_12_bullet_mask_image,
                                               enemy_12_bullet_rect, enemy_12_bullet_flipped, enemy_12_surface_flipped,
                                               enemy_12_bullet_speed, enemy_12_ship_speed, player_health, score,
                                               enemy_12_hit, enemy_12_bullet_stop, enemy_12_bullet_x, enemy_12_bullet_y,
                                               bullet_shot, bullet_follow_player)  # Function for enemy 3

        # Calculating the returned items

        player_health = player_stats_enemy_12[0]

        score = player_stats_enemy_12[1]

        enemy_12_bullet_speed = player_stats_enemy_12[2]

        enemy_12_bullet_stop = player_stats_enemy_12[3]

        enemy_12_hit = player_stats_enemy_12[4]

        bullet_shot = player_stats_enemy_12[5]

        bullet_follow_player = player_stats_enemy_12[6]

        # Checking if the player goes off-screen

        if player_rect.bottom >= screen_height:

            player_rect.bottom = 80

            if not bullet_shot:

                player_bullet_rect.y = player_rect.y + 17

        if player_rect.top <= 0:

            player_rect.top = screen_height - 80

            if not bullet_shot:

                player_bullet_rect.y = player_rect.y + 17

        if player_rect.left < 0:

            player_rect.left = 0

            if not bullet_shot:

                player_bullet_rect.x = player_rect.x + 17

        if player_rect.right > screen_width:

            player_rect.right = screen_width

            if not bullet_shot:

                player_bullet_rect.x = player_rect.x + 17

        if player_health <= 0:

            game_active = False

            pygame.mixer.music.stop()

    else:

        if (score == 0) and (player_health == 100):

            title_screen()

        else:

            game_over_screen()

            if not end_screen_music:

                mixer.music.load('Space Music Pack/in-the-wreckage.wav')  # Loads the game music
                pygame.mixer.music.play(-1)  # Plays the game music on loop
                pygame.mixer.music.set_volume(0.3)  # Sets the music volume

                end_screen_music = True

    # Updating the display

    pygame.display.update()  # Updates the display

    clock.tick(60)  # Acts as FPS
