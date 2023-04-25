import pygame
import random

pygame.init()
clock = pygame.time.Clock()
font_36 = pygame.font.Font(None, 36)
font_52 = pygame.font.Font(None, 52)

WIDTH, HEIGHT = 1280, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Carrot')

# player_img = pygame.image.load('player.png')
# oobleck_img = pygame.image.load('oobleck.png')
# konjac_img = pygame.image.load('konjac.png')

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (120, 120, 120)
DARKRED = (150, 0, 0)
DARKGREEN = (0, 150, 0)

EDGE_THICKNESS = 32 // 2
PATH_THICKNESS = 32
PLAYER_SIZE = 16
ENDPOINT_SIZE = 16

class Player(pygame.sprite.Sprite) :

    def __init__(self, x, y) :
        super().__init__()
        self.image = pygame.Surface((PLAYER_SIZE, PLAYER_SIZE))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y
        self.init_speed = 5

    def update(self, keys) :

        if keys[pygame.K_w] :
            self.rect.y -= self.init_speed
        elif keys[pygame.K_s] :
            self.rect.y += self.init_speed

        if keys[pygame.K_a] :
            self.rect.x -= self.init_speed
        elif keys[pygame.K_d] :
            self.rect.x += self.init_speed

# class MazeBlock(pygame.sprite.Sprite) :

#     def __init__(self) :
#         super().__init__()
#         self.image = pygame.Surface((PATH_THICKNESS, PATH_THICKNESS))
#         self.image.fill(GRAY)
#         self.rect = self.image.get_rect()

def create_maze(maze_width, maze_height) :

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
                direction = random.choice(['N', 'S', 'E', 'W'])
                if direction == 'N' and maze_map[i - 1][j] == 0 :
                    maze_map[i - 1][j] = 1
                    break
                elif direction == 'S' and maze_map[i + 1][j] == 0 :
                    maze_map[i + 1][j] = 1
                    break
                elif direction == 'E' and maze_map[i][j + 1] == 0 :
                    maze_map[i][j + 1] = 1
                    break
                elif direction == 'W' and maze_map[i][j - 1] == 0 :
                    maze_map[i][j - 1] = 1
                    break

    return maze_map

def generate_random_location() :

    global player_coordinates, endpoint_coordinates

    player_coordinates = [0, 0]
    endpoint_coordinates = [0, 0]

    NE = [WIDTH - EDGE_THICKNESS - PATH_THICKNESS // 2 - PLAYER_SIZE // 2, EDGE_THICKNESS + PATH_THICKNESS // 2 - PLAYER_SIZE // 2 + 16]
    SE = [WIDTH - EDGE_THICKNESS - PATH_THICKNESS // 2 - PLAYER_SIZE // 2, HEIGHT - EDGE_THICKNESS - PATH_THICKNESS // 2 - PLAYER_SIZE // 2]
    SW = [EDGE_THICKNESS + PATH_THICKNESS // 2 - PLAYER_SIZE // 2, HEIGHT - EDGE_THICKNESS - PATH_THICKNESS // 2 - PLAYER_SIZE // 2]
    NW = [EDGE_THICKNESS + PATH_THICKNESS // 2 - PLAYER_SIZE // 2, EDGE_THICKNESS + PATH_THICKNESS // 2 - PLAYER_SIZE // 2 + 16]

    location = random.choice(['NE', 'SE', 'SW', 'NW'])
    if location == 'NE' :
        player_coordinates = NE
        endpoint_coordinates = SW
    elif location == 'SE' :
        player_coordinates = SE
        endpoint_coordinates = NW
    elif location == 'SW' :
        player_coordinates = SW
        endpoint_coordinates = NE
    elif location == 'NW' :
        player_coordinates = NW
        endpoint_coordinates = SE

    return

start_button_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 175, 200, 50)

ooblecks = []
konjacs = []

score = 10
game_start = False
game_result = False
game_over = False
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

        elif event.type == pygame.MOUSEBUTTONDOWN :

            if start_button_rect.collidepoint(pygame.mouse.get_pos()) :

                maze = create_maze(WIDTH // PATH_THICKNESS + 1, HEIGHT // PATH_THICKNESS + 1)

                # maze_surface = pygame.Surface((WIDTH, HEIGHT))
                # for i in range(len(maze)) :
                #     for j in range(len(maze[0])) :
                #         if maze[i][j] == 1 :
                #             pygame.draw.rect(maze_surface, GRAY, pygame.Rect(j * PATH_THICKNESS - 16, i * PATH_THICKNESS, PATH_THICKNESS, PATH_THICKNESS))

                maze_blocks = pygame.sprite.Group()
                for i in range(len(maze)) :
                    for j in range(len(maze[0])) :
                        if maze[i][j] == 1 :
                            maze_block = pygame.sprite.Sprite()
                            maze_block.image = pygame.Surface((PATH_THICKNESS, PATH_THICKNESS))
                            maze_block.image.fill(GRAY)                        
                            maze_block.rect = pygame.Rect(j * PATH_THICKNESS - 16, i * PATH_THICKNESS, PATH_THICKNESS, PATH_THICKNESS)
                            maze_blocks.add(maze_block)
                            # pygame.draw.rect(screen, GRAY, pygame.Rect(j * PATH_THICKNESS - 16, i * PATH_THICKNESS, PATH_THICKNESS, PATH_THICKNESS))

                generate_random_location()            
                player = Player(player_coordinates[0], player_coordinates[1])
                endpoint_rect = pygame.Rect(endpoint_coordinates[0], endpoint_coordinates[1], ENDPOINT_SIZE, ENDPOINT_SIZE)
                players = pygame.sprite.Group()
                players.add(player)

                # collision = pygame.sprite.spritecollideany(player, maze_surface)

                game_start = True

    if not game_start :
        screen.fill(BLACK)
        pygame.draw.rect(screen, WHITE, start_button_rect)
        title = font_52.render('Oobleck', True, WHITE)
        start_button_text = font_36.render('Start', True, BLACK)
        screen.blit(title, (WIDTH // 2 - 65, HEIGHT // 2 - 165))
        screen.blit(start_button_text, (WIDTH // 2 - 25, HEIGHT // 2 + 185))

    else :

        if not game_result :

            screen.fill(BLACK)

            # screen.blit(maze_surface, (0, 0))

            # for i in range(len(maze)) :
            #     for j in range(len(maze[0])) :
            #         if maze[i][j] == 1 :
            #             maze_block = pygame.sprite.Sprite()
            #             maze_block.image = pygame.Surface((PATH_THICKNESS, PATH_THICKNESS))
            #             maze_block.image.fill(GRAY)                        
            #             maze_block.rect = pygame.Rect(j * PATH_THICKNESS - 16, i * PATH_THICKNESS, PATH_THICKNESS, PATH_THICKNESS)
            #             maze_blocks.add(maze_block)
            #             pygame.draw.rect(screen, GRAY, pygame.Rect(j * PATH_THICKNESS - 16, i * PATH_THICKNESS, PATH_THICKNESS, PATH_THICKNESS))

            maze_blocks.draw(screen)

            pygame.draw.rect(screen, DARKGREEN, endpoint_rect)
            players.draw(screen)
            players.update(keys)

        else :
            
            screen.fill(GRAY)
            score_text = font_52.render('Score', True, WHITE)
            screen.blit(score_text, (WIDTH // 2 - 65, HEIGHT // 2 - 165))

    pygame.display.update()

pygame.quit()