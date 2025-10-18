import pygame, sys
from pygame.locals import *
from math import *

square_size = 10
eye_height = 1.7
# camera_height = 360
building_height = 3

map_width = 10
map_height = 10
# game_map = [[0] * map_width for _ in range(map_height)]
game_map = [[2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
            [3, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [2, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [3, 0, 0, 0, 2, 0, 0, 0, 0, 1],
            [2, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [3, 0, 0, 0, 1, 3, 1, 0, 0, 1],
            [2, 0, 0, 0, 2, 3, 0, 0, 0, 1],
            [3, 0, 1, 0, 0, 0, 0, 0, 0, 1],
            [2, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [3, 1, 2, 1, 2, 1, 2, 1, 2, 1], ]

player_x = 2.0
player_y = 2.0
player_dir = 30


def rotate(x, d, angle):
    r_angle = radians(angle)
    # rotate_x = x * cos(r_angle) + d * sin(r_angle)
    # rotate_y = d * cos(r_angle) - x * sin(r_angle)
    rotate_x = cos(r_angle) * x - sin(r_angle) * d
    rotate_y = sin(r_angle) * x + cos(r_angle) * d
    return rotate_x, rotate_y


def calculate_distance_remaining(position, negative):
    if not position % square_size:
        return square_size
    if negative:
        return position % square_size
    else:
        return -(position % square_size)


def get_map(x, y):
    return floor(x), floor(y)


def calculate_step(dx, dy):
    min_step = 0.1
    if abs(dx) > abs(dy):
        x_step = min_step if dx > 0 else -min_step
        y_step = abs(dy / dx) * (min_step if dy > 0 else -min_step)
    else:
        y_step = min_step if dy > 0 else -min_step
        x_step = abs(dx / dy) * (min_step if dx > 0 else -min_step)
    return x_step, y_step


def cast_ray(start_x, start_y, dx, dy):
    x_pos, y_pos = start_x, start_y
    list_x, list_y = 0, 0
    x_step, y_step = calculate_step(dx, dy)
    while True:
        x_pos += x_step
        y_pos += y_step
        list_x = floor(x_pos) if dx > 0 else ceil(x_pos)
        list_y = floor(y_pos) if dy > 0 else ceil(y_pos)
        if game_map[list_y][list_x]:
            break
    return x_pos, y_pos, list_x, list_y


def get_color(x, y):
    if game_map[y][x] == 1:
        return 255, 255, 255
    elif game_map[y][x] == 2:
        return 255, 0, 0
    elif game_map[y][x] == 3:
        return 0, 0, 255


def represent_ray(map_x, map_y, render_x, ry):
    if game_map[map_y][map_x]:
        line_color = get_color(map_x, map_y)
        h = (camera_height * ry) / (screen_distance * 2)
        yk1 = (building_height - eye_height) / h
        render_y = screen_height / 2 * (1 - yk1)
        yk2 = eye_height / h
        render_h = screen_height / 2 * (yk1 + yk2)
        pygame.draw.rect(game_screen, line_color, (render_x, render_y, line_width, render_h))


def cast_mutiple_rays():
    # 当前对应的屏幕位置（非像素）：-179.5~179.5
    screen_x = -clarity_n / 2 + 0.5

    # 对于每个screen_x（重复clarity_n次）
    for i in range(clarity_n):
        rotate_x, rotate_y = rotate(-screen_x, screen_distance, player_dir)
        x_pos, y_pos, map_x, map_y = cast_ray(player_x, player_y, rotate_x, rotate_y)
        rx, ry = rotate(x_pos - player_x, y_pos - player_y, -player_dir)
        represent_ray(map_x, map_y, (screen_x + clarity_n / 2) * line_width, ry)
        screen_x += 1


pygame.init()
FPS = 60
fpsClock = pygame.time.Clock()

clarity_n = 200
line_width = 5

screen_width = line_width * clarity_n
screen_height = round(screen_width * 0.5625)
screen_distance = clarity_n / 2 * 1

camera_height = clarity_n * 1

game_screen = pygame.display.set_mode((screen_width, screen_height), 0, 32)
pygame.display.set_caption('game')

# pygame.event.set_grab(True)

while True:
    game_screen.fill((0, 0, 0))
    cast_mutiple_rays()
    player_dir += 0.5
    player_dir %= 360
    # pygame.mouse.set_pos(100,100)
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    pygame.display.update()
    fpsClock.tick(FPS)
