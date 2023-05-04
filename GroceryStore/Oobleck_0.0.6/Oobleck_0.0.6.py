import pygame
import random

# 사용할 파라미터 import
from hyperparameters import BLACK, WHITE, GRAY, DARKRED, DARKGREEN, DARKYELLOW
from hyperparameters import WIDTH, HEIGHT, WIDTH_UNIT, HEIGHT_UNIT
from hyperparameters import EDGE_THICKNESS, PATH_THICKNESS
from hyperparameters import QUEEN_SIZE
from hyperparameters import count_ooblecks, count_konjacs, init_score, cool_down_time
from hyperparameters import player_wall_collisions, game_play, game_start, game_result, game_over, lift_key, player_moved

# gensprite는 게임을 구성할 객체들을 생성할 수 있는 class들을 구현한 파일
# genmaze는 게임 내 미로에 관한 생성, 제어함수들을 구현한 파일
from gensprite import Player, Oobleck, MazeBlock
from genmaze import generate_maze, generate_random_location, collision_detector

# 초기화
pygame.init()

# 프레임을 측정할 시간과 사용할 글씨 폰트 불러오기
clock = pygame.time.Clock()
font_36 = pygame.font.Font(None, 36)
font_54 = pygame.font.Font(None, 54)
font_72 = pygame.font.Font(None, 72)

# 게임창의 크기와 제목
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Oobleck')

# 버튼 객체
play_button_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 175, 200, 50)
quit_button_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 250, 200, 50)
start_button_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 175, 200, 50)

# 이건 아마 gensprite로 옮길 듯
# player_moveskill_dict = {'move' : 0,
#                          'dash' : 0,
#                          'warp' : 0,
#                          'big warp' : 0}

# oobleck_moveskill_dict = {'move' : 0,
#                           'dash' : 0,
#                           'warp' : 0,
#                           'big warp' : 0}

# 미로의 정보를 불러올 빈 리스트 생성
maze = []

# 게임 시작, 화면에 그릴 내용들을 게임을 종료하기 전까지 계속 반복 업데이트
while not game_over :

    clock.tick(60)                                      # FPS = 60
    keys = pygame.key.get_pressed()                     # 키 입력 event 처리를 위한 리스트

    for event in pygame.event.get() :                   # 게임 내 발생하는 다양한 event의 동작을 서술

        if event.type == pygame.QUIT :                  # pygame을 종료하게 될 경우 loop break
            game_over = True

        elif event.type == pygame.KEYDOWN :             # 키를 누를 경우
            if event.key == pygame.K_ESCAPE :
                game_over = True
            elif event.key == pygame.K_p :              # 점수 화면으로 조기 종료
                game_result = True

            if event.key == pygame.K_w :                # ----- 여기부터 하단까지는 키를 누르는 순간에만 -----
                lift_key = False                        #       입력이 들어가도록 하기 위한 장치
            elif event.key == pygame.K_s :
                lift_key = False
            elif event.key == pygame.K_a :
                lift_key = False
            elif event.key == pygame.K_d :
                lift_key = False

        elif event.type == pygame.KEYUP :               # 키를 뗄 경우

            if event.key == pygame.K_w :
                lift_key = True
            elif event.key == pygame.K_s :
                lift_key = True
            elif event.key == pygame.K_a :
                lift_key = True
            elif event.key == pygame.K_d :
                lift_key = True                         # -------------------------------------------------

        elif event.type == pygame.MOUSEBUTTONUP :                                       # 마우스 커서가 앞서 만든 버튼 객체 위에서 클릭할 때

            if play_button_rect.collidepoint(pygame.mouse.get_pos()) :
                play_button_rect = pygame.Rect(0, 0, 0, 0)
                game_play = True

            elif quit_button_rect.collidepoint(pygame.mouse.get_pos()) :
                game_over = True                

            elif start_button_rect.collidepoint(pygame.mouse.get_pos()) :
                
                [player_coordinates, queen_coordinates] = generate_random_location()    # 플레이어의 시작점과 끝점을 4곳 중 랜덤으로 지정 (반대에 위치)
                oobleck_possible_coordinates = []                                       # oobleck이 생성될 수 있는 지점들의 후보 (3면이 벽인 곳)

                maze = generate_maze(WIDTH_UNIT, HEIGHT_UNIT)                           # 미로 생성 (maze는 element가 0 또는 1로 이루어진 matrix로, 1인 곳은 벽을 의미)
                maze_blocks = pygame.sprite.Group()                                     # 플레이어와 미로의 충돌 판정을 내기 위해 미로 블록을 스프라이트로 생성
                for i in range(len(maze)) :                                             # 생성된 미로 정보에 따라 미로 블록 배치
                    for j in range(len(maze[0])) :
                        if maze[i][j] == 1 :
                            maze_block = MazeBlock(i, j)
                            maze_blocks.add(maze_block)                                 # oobleck 생성 가능 범위를 제한하여 oobleck 기준 상하좌우에 벽이 3곳인 곳만 후보 지정
                        if (maze[i][j] == 0) and (j >= 7) and (j <= WIDTH_UNIT - 7) and (i >= 7) and (i <= HEIGHT_UNIT - 7) :
                            if (maze[i - 1][j] + maze[i + 1][j] + maze[i][j + 1] + maze[i][j - 1]) == 3 :
                                oobleck_possible_coordinates.append([j, i])

                players = pygame.sprite.Group()                                                 # 플레이어 객체 생성
                player = Player(player_coordinates[0], player_coordinates[1])
                players.add(player)

                ooblecks = pygame.sprite.Group()                                                # oobleck 객체 생성
                for o in range(0, count_ooblecks) :
                    oobleck_coordinates = random.choice(oobleck_possible_coordinates)
                    oobleck_possible_coordinates.remove(oobleck_coordinates)
                    globals()['oobleck{}'.format(o + 1)] = Oobleck(oobleck_coordinates, maze)
                    ooblecks.add(globals()['oobleck{}'.format(o + 1)])             

                queens = pygame.sprite.Group()                                                  # 끝점인 queen 객체 생성 (클래스를 gensprite에 넣지는 않았음)
                queen = pygame.sprite.Sprite()
                queen.image = pygame.Surface((QUEEN_SIZE, QUEEN_SIZE))
                queen.image.fill(DARKGREEN)
                queen.rect = pygame.Rect(queen_coordinates[0], queen_coordinates[1], QUEEN_SIZE, QUEEN_SIZE)
                queens.add(queen)

                game_start = True                                                               # 모든 생성 과정을 마치고 game_start를 False에서 True로 전환

    if not game_play :                                                                          # 메인 화면 창
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

    elif not game_start :                                                                       # 게임 플레이 설명 창
        screen.fill(GRAY)
        pygame.draw.rect(screen, WHITE, start_button_rect)
        pygame.draw.rect(screen, WHITE, quit_button_rect)
        how_to_play = font_72.render('How to play', True, WHITE)
        start_button_text = font_36.render('Start', True, BLACK)
        quit_button_text = font_36.render('Quit', True, BLACK)
        screen.blit(how_to_play, (WIDTH // 2 - 136, HEIGHT // 2 - 255))
        screen.blit(start_button_text, (WIDTH // 2 - 28, HEIGHT // 2 + 188))
        screen.blit(quit_button_text, (WIDTH // 2 - 25, HEIGHT // 2 + 263))

    else :                                                                                      # 게임 시작

        if not game_result :

            screen.fill(BLACK)                                                                  # 배경
            for i in range(0, HEIGHT_UNIT) :                                                    # 그리드
                for j in range(0, WIDTH_UNIT) :
                    pygame.draw.line(screen, (64, 64, 64), (0, i * PATH_THICKNESS - 1), (WIDTH_UNIT * PATH_THICKNESS, i * PATH_THICKNESS - 1), 2)
                    pygame.draw.line(screen, (64, 64, 64), (j * PATH_THICKNESS + EDGE_THICKNESS - 1, 0), (j * PATH_THICKNESS + EDGE_THICKNESS - 1, HEIGHT_UNIT * PATH_THICKNESS), 2)

            maze_blocks.draw(screen)                                                            # 각 객체 표현
            players.draw(screen)
            ooblecks.draw(screen)
            queens.draw(screen)

            player_moved = player.update(keys, lift_key, player_wall_collisions)                # 발생한 event에 따라 객체 업데이트
            player_wall_collisions = pygame.sprite.spritecollide(player, maze_blocks, False)    # 플레이어가 벽과 충돌한 event 발생을 위한 boolean
            if player_wall_collisions :                                                         # 충돌하면 충돌 전 좌표로 되돌림
                player.rect.x = player.prev_x
                player.rect.y = player.prev_y
                player_moved = False                                                            # oobleck들은 플레이어가 이동했을 때만 움직임

            for o in range(0, count_ooblecks) :                                                 # 모든 oobleck 객체 업데이트
                globals()['oobleck{}'.format(o + 1)].update(player_moved, player_wall_collisions)

            player_queen_collisions = pygame.sprite.spritecollide(player, queens, False)        # queen과 충돌한 event 발생 시 게임 결과 창으로 이동
            if player_queen_collisions :
                game_result = True

        else :                                                                                  # 게임 결과 창
            
            screen.fill(GRAY)
            score_text = font_72.render('Score', True, WHITE)
            screen.blit(score_text, (WIDTH // 2 - 78, HEIGHT // 2 - 165))

    pygame.display.update()                                                                     # 해당하는 창에서 모든 과정의 화면 표현을 업데이트

pygame.quit()                                                                                   # while loop break 후 pygame도 종료