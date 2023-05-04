import random

from hyperparameters import WIDTH, HEIGHT
from hyperparameters import EDGE_THICKNESS, PATH_THICKNESS
from hyperparameters import PLAYER_SIZE

def generate_maze(maze_width, maze_height) :

    maze_map = [[0 for x in range(maze_width)] for y in range(maze_height)]

    for x in range(maze_width) :
        maze_map[0][x] = 1
        maze_map[maze_height - 1][x] = 1
    for y in range(maze_height) :
        maze_map[y][0] = 1
        maze_map[y][maze_width - 1] = 1

    for i in range(2, maze_height - 2, 2) :
        for j in range(2, maze_width - 2, 2) :
            maze_map[i][j] = 1
            while True :
                direction = random.choice(['N', 'S', 'W', 'E'])
                if direction == 'N' and maze_map[i - 1][j] == 0 :
                    maze_map[i - 1][j] = 1
                    break
                elif direction == 'S' and maze_map[i + 1][j] == 0 :
                    maze_map[i + 1][j] = 1
                    break
                elif direction == 'W' and maze_map[i][j - 1] == 0 :
                    maze_map[i][j - 1] = 1
                    break
                elif direction == 'E' and maze_map[i][j + 1] == 0 :
                    maze_map[i][j + 1] = 1
                    break

    return maze_map

def generate_random_location() :

    player_coordinates = [0, 0]
    queen_coordinates = [0, 0]

    NE = [WIDTH - EDGE_THICKNESS - PATH_THICKNESS // 2 - PLAYER_SIZE // 2, EDGE_THICKNESS + PATH_THICKNESS // 2 - PLAYER_SIZE // 2 + 16]
    SE = [WIDTH - EDGE_THICKNESS - PATH_THICKNESS // 2 - PLAYER_SIZE // 2, HEIGHT - EDGE_THICKNESS - PATH_THICKNESS // 2 - PLAYER_SIZE // 2]
    SW = [EDGE_THICKNESS + PATH_THICKNESS // 2 - PLAYER_SIZE // 2, HEIGHT - EDGE_THICKNESS - PATH_THICKNESS // 2 - PLAYER_SIZE // 2]
    NW = [EDGE_THICKNESS + PATH_THICKNESS // 2 - PLAYER_SIZE // 2, EDGE_THICKNESS + PATH_THICKNESS // 2 - PLAYER_SIZE // 2 + 16]

    location = random.choice(['NW', 'SW', 'SE', 'NE'])
    if location == 'NW' :
        player_coordinates = NW
        queen_coordinates = SE
    elif location == 'SW' :
        player_coordinates = SW
        queen_coordinates = NE
    elif location == 'SE' :
        player_coordinates = SE
        queen_coordinates = NW
    elif location == 'NE' :
        player_coordinates = NE
        queen_coordinates = SW

    return player_coordinates, queen_coordinates

def collision_detector(collisions_list) :

    detected = False
    if any(collisions_list) :
        detected = True

    return detected