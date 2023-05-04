import pygame
import random

from hyperparameters import BLACK, WHITE, GRAY, DARKRED, DARKGREEN, DARKYELLOW
from hyperparameters import PATH_THICKNESS
from hyperparameters import PLAYER_SIZE, player_speed
from hyperparameters import OOBLECK_SIZE, oobleck_speed
from hyperparameters import QUEEN_SIZE

class Player(pygame.sprite.Sprite) :

    def __init__(self, x, y) :
        super().__init__()
        self.image = pygame.Surface((PLAYER_SIZE, PLAYER_SIZE))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y
        self.prev_x, self.prev_y = self.rect.x, self.rect.y
        self.init_speed = player_speed

    def update(self, keys, lift_key, collisions) :

        self.prev_x = self.rect.x
        self.prev_y = self.rect.y
        player_moved = False

        if not collisions :

            if keys[pygame.K_w] and lift_key :
                self.rect.y -= self.init_speed
                player_moved = True
            elif keys[pygame.K_s] and lift_key :
                self.rect.y += self.init_speed
                player_moved = True

            if keys[pygame.K_a] and lift_key :
                self.rect.x -= self.init_speed
                player_moved = True
            elif keys[pygame.K_d] and lift_key :
                self.rect.x += self.init_speed
                player_moved = True

        return player_moved

class Oobleck(pygame.sprite.Sprite) :

    def __init__(self, coordinates, maze) :
        super().__init__()
        self.image = pygame.Surface((OOBLECK_SIZE, OOBLECK_SIZE))
        self.image.fill(DARKYELLOW)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = coordinates[0] * PATH_THICKNESS - OOBLECK_SIZE // 2, coordinates[1] * PATH_THICKNESS - OOBLECK_SIZE // 2 + 16
        self.prev_x, self.prev_y = self.rect.x, self.rect.y
        self.init_speed = oobleck_speed

        self.coordinates = coordinates
        self.prev_coordinates = self.coordinates
        self.maze = maze

    def update(self, player_moved, player_wall_collisions) :

        if not player_wall_collisions :

            if player_moved :

                self.prev_x = self.rect.x
                self.prev_y = self.rect.y
                self.prev_coordinates = self.coordinates

                detector = []

                if self.maze[self.coordinates[1] - 1][self.coordinates[0]] != 1 :
                    detector.append('N')
                if self.maze[self.coordinates[1] + 1][self.coordinates[0]] != 1 :
                    detector.append('S')
                if self.maze[self.coordinates[1]][self.coordinates[0] - 1] != 1 :
                    detector.append('W')
                if self.maze[self.coordinates[1]][self.coordinates[0] + 1] != 1 :
                    detector.append('E')

                detector = random.choice(detector)

                if detector == 'N' :
                    self.rect.y -= self.init_speed
                    self.coordinates[1] -= 1
                elif detector == 'S' :
                    self.rect.y += self.init_speed
                    self.coordinates[1] += 1
                elif detector == 'W' :
                    self.rect.x -= self.init_speed
                    self.coordinates[0] -= 1
                elif detector == 'E' :
                    self.rect.x += self.init_speed
                    self.coordinates[0] += 1

class MazeBlock(pygame.sprite.Sprite) :

    def __init__(self, x, y) :
        super().__init__()
        self.image = pygame.Surface((PATH_THICKNESS, PATH_THICKNESS))
        self.image.fill(GRAY)
        self.rect = pygame.Rect(y * PATH_THICKNESS - 16, x * PATH_THICKNESS, PATH_THICKNESS, PATH_THICKNESS)