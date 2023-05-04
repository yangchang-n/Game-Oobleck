WIDTH, HEIGHT = 1280, 720
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
DARKRED = (128, 0, 0)
DARKGREEN = (0, 128, 0)
DARKYELLOW = (208, 188, 88)

EDGE_THICKNESS = 32 // 2
PATH_THICKNESS = 32
PLAYER_SIZE = 16
OOBLECK_SIZE = 16
QUEEN_SIZE = 16

WIDTH_UNIT = WIDTH // PATH_THICKNESS + 1
HEIGHT_UNIT = HEIGHT // PATH_THICKNESS + 1

player_speed = PATH_THICKNESS
oobleck_speed = PATH_THICKNESS

count_ooblecks = 5
count_konjacs = 5
init_score = 10
cool_down_time = 100

player_wall_collisions = False
game_play = False
game_start = False
game_result = False
game_over = False
lift_key = True
player_moved = False