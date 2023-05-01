import pygame
import random

pygame.init()
clock = pygame.time.Clock()
font_36 = pygame.font.Font(None, 36)
font_54 = pygame.font.Font(None, 54)
font_72 = pygame.font.Font(None, 72)

WIDTH, HEIGHT = 1280, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Oobleck')

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

class Player(pygame.sprite.Sprite) :

    def __init__(self, x, y) :
        super().__init__()
        self.image = pygame.Surface((PLAYER_SIZE, PLAYER_SIZE))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y
        self.prev_x, self.prev_y = self.rect.x, self.rect.y
        self.init_speed = player_speed

    def update(self, keys) :

        global lift_key, player_wall_collisions
        
        self.prev_x = self.rect.x
        self.prev_y = self.rect.y

        if keys[pygame.K_w] and lift_key :
            self.rect.y -= self.init_speed
        elif keys[pygame.K_s] and lift_key :
            self.rect.y += self.init_speed

        if keys[pygame.K_a] and lift_key :
            self.rect.x -= self.init_speed
        elif keys[pygame.K_d] and lift_key :
            self.rect.x += self.init_speed

        lift_key = False

        player_wall_collisions = pygame.sprite.spritecollide(self, maze_blocks, False)
        if player_wall_collisions :
            self.rect.x = self.prev_x
            self.rect.y = self.prev_y

class Oobleck(pygame.sprite.Sprite) :

    def __init__(self, x, y) :
        super().__init__()
        self.image = pygame.Surface((OOBLECK_SIZE, OOBLECK_SIZE))
        self.image.fill(DARKYELLOW)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y
        self.prev_x, self.prev_y = self.rect.x, self.rect.y
        self.init_speed = oobleck_speed

    def update(self, direction) :

        if not player_wall_collisions :
        
            self.prev_x = self.rect.x
            self.prev_y = self.rect.y

            if direction['N'] == 1 :
                self.rect.y -= self.init_speed
            elif direction['S'] == 1 :
                self.rect.y += self.init_speed
            elif direction['W'] == 1 :
                self.rect.x -= self.init_speed
            elif direction['E'] == 1 :
                self.rect.x += self.init_speed

            oobleck_wall_collisions = pygame.sprite.spritecollide(self, maze_blocks, False)
            if oobleck_wall_collisions :
                self.rect.x = self.prev_x
                self.rect.y = self.prev_y
                direction = {'N' : 0, 'S' : 0, 'W' : 0, 'E' : 0}
                direction[random.choice(['N', 'S', 'W', 'E'])] = 1
                self.update(direction)

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

    global player_coordinates, queen_coordinates

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

    return

play_button_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 175, 200, 50)
quit_button_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 250, 200, 50)
start_button_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 175, 200, 50)

game_play = False
game_start = False
game_result = False
game_over = False
lift_key = False

player_moveskill_dict = {'move' : 0,
                         'dash' : 0,
                         'warp' : 0,
                         'big warp' : 0}

for o in range(count_ooblecks) :
    globals()['oobleck{}_direction_dict'.format(o + 1)] = {'N' : 0, 'S' : 0, 'W' : 0, 'E' : 0}

oobleck_direction_dict = {'N' : 0,
                          'S' : 0,
                          'W' : 0,
                          'E' : 0}

oobleck_moveskill_dict = {'move' : 0,
                          'dash' : 0,
                          'warp' : 0,
                          'big warp' : 0}

maze = [[]]

while not game_over :

    clock.tick(60)
    keys = pygame.key.get_pressed()

    for event in pygame.event.get() :

        if event.type == pygame.QUIT :
            game_over = True

        elif event.type == pygame.KEYDOWN :
            if event.key == pygame.K_ESCAPE :
                game_over = True
            elif event.key == pygame.K_p :
                game_result = True

        elif event.type == pygame.KEYUP :

            if event.key == pygame.K_w :
                lift_key = True
            elif event.key == pygame.K_s :
                lift_key = True
            elif event.key == pygame.K_a :
                lift_key = True
            elif event.key == pygame.K_d :
                lift_key = True

            # if event.key == (pygame.K_w or pygame.K_s or pygame.K_a or pygame.K_d) :
            # if not player_wall_collisions :
            for o in range(count_ooblecks) :
                globals()['oobleck{}_direction_dict'.format(o + 1)][random.choice(['N', 'S', 'W', 'E'])] = 1

        elif event.type == pygame.MOUSEBUTTONUP :

            if play_button_rect.collidepoint(pygame.mouse.get_pos()) :
                play_button_rect = pygame.Rect(0, 0, 0, 0)
                game_play = True

            elif quit_button_rect.collidepoint(pygame.mouse.get_pos()) :
                game_over = True                

            elif start_button_rect.collidepoint(pygame.mouse.get_pos()) :
                
                generate_random_location()
                oobleck_possible_coordinates = []

                maze = generate_maze(WIDTH_UNIT, HEIGHT_UNIT)
                maze_blocks = pygame.sprite.Group()
                for i in range(len(maze)) :
                    for j in range(len(maze[0])) :
                        if maze[i][j] == 1 :
                            maze_block = pygame.sprite.Sprite()
                            maze_block.image = pygame.Surface((PATH_THICKNESS, PATH_THICKNESS))
                            maze_block.image.fill(GRAY)                        
                            maze_block.rect = pygame.Rect(j * PATH_THICKNESS - 16, i * PATH_THICKNESS, PATH_THICKNESS, PATH_THICKNESS)
                            maze_blocks.add(maze_block)
                        if (maze[i][j] == 0) and (j >= 7) and (j <= WIDTH_UNIT - 7) and (i >= 7) and (i <= HEIGHT_UNIT - 7) :
                            if (maze[i - 1][j] + maze[i + 1][j] + maze[i][j + 1] + maze[i][j - 1]) == 3 :
                                oobleck_possible_coordinates.append([j, i])

                players = pygame.sprite.Group()
                player = Player(player_coordinates[0], player_coordinates[1])
                players.add(player)

                ooblecks = pygame.sprite.Group()
                for o in range(0, count_ooblecks) :
                    oobleck_coordinate = random.choice(oobleck_possible_coordinates)
                    oobleck_possible_coordinates.remove(oobleck_coordinate)
                    oobleck_x_coordinate = oobleck_coordinate[0] * PATH_THICKNESS - OOBLECK_SIZE // 2
                    oobleck_y_coordinate = oobleck_coordinate[1] * PATH_THICKNESS - OOBLECK_SIZE // 2 + 16
                    globals()['oobleck{}'.format(o + 1)] = Oobleck(oobleck_x_coordinate, oobleck_y_coordinate)
                    ooblecks.add(globals()['oobleck{}'.format(o + 1)])                         

                queens = pygame.sprite.Group()
                queen = pygame.sprite.Sprite()
                queen.image = pygame.Surface((QUEEN_SIZE, QUEEN_SIZE))
                queen.image.fill(DARKGREEN)
                queen.rect = pygame.Rect(queen_coordinates[0], queen_coordinates[1], QUEEN_SIZE, QUEEN_SIZE)
                queens.add(queen)

                game_start = True

    if not game_play :
        screen.fill(BLACK)
        pygame.draw.rect(screen, WHITE, play_button_rect)
        pygame.draw.rect(screen, WHITE, quit_button_rect)
        pygame.draw.rect(screen, DARKYELLOW, pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 - 100, 200, 200))
        title = font_72.render('Oobleck', True, WHITE)
        play_button_text = font_36.render('Play', True, BLACK)
        quit_button_text = font_36.render('Quit', True, BLACK)
        screen.blit(title, (WIDTH // 2 - 100, HEIGHT // 2 - 165))
        screen.blit(play_button_text, (WIDTH // 2 - 25, HEIGHT // 2 + 188))
        screen.blit(quit_button_text, (WIDTH // 2 - 25, HEIGHT // 2 + 263))

    elif not game_start :
        screen.fill(GRAY)
        pygame.draw.rect(screen, WHITE, start_button_rect)
        pygame.draw.rect(screen, WHITE, quit_button_rect)
        how_to_play = font_72.render('How to play', True, WHITE)
        start_button_text = font_36.render('Start', True, BLACK)
        quit_button_text = font_36.render('Quit', True, BLACK)
        screen.blit(how_to_play, (WIDTH // 2 - 136, HEIGHT // 2 - 255))
        screen.blit(start_button_text, (WIDTH // 2 - 28, HEIGHT // 2 + 188))
        screen.blit(quit_button_text, (WIDTH // 2 - 25, HEIGHT // 2 + 263))

    else :

        if not game_result :

            screen.fill(BLACK)
            for i in range(0, HEIGHT_UNIT) :
                for j in range(0, WIDTH_UNIT) :
                    pygame.draw.line(screen, (64, 64, 64), (0, i * PATH_THICKNESS - 1), (WIDTH_UNIT * PATH_THICKNESS, i * PATH_THICKNESS - 1), 2)
                    pygame.draw.line(screen, (64, 64, 64), (j * PATH_THICKNESS + EDGE_THICKNESS - 1, 0), (j * PATH_THICKNESS + EDGE_THICKNESS - 1, HEIGHT_UNIT * PATH_THICKNESS), 2)

            maze_blocks.draw(screen)
            players.draw(screen)
            ooblecks.draw(screen)
            queens.draw(screen)

            players.update(keys)
            for o in range(0, count_ooblecks) :
                globals()['oobleck{}'.format(o + 1)].update(globals()['oobleck{}_direction_dict'.format(o + 1)])
                globals()['oobleck{}_direction_dict'.format(o + 1)] = {'N' : 0, 'S' : 0, 'W' : 0, 'E' : 0}

            queen_collisions = pygame.sprite.spritecollide(player, queens, False)
            if queen_collisions :
                game_result = True

        else :
            
            screen.fill(GRAY)
            score_text = font_72.render('Score', True, WHITE)
            screen.blit(score_text, (WIDTH // 2 - 78, HEIGHT // 2 - 165))

    pygame.display.update()

pygame.quit()