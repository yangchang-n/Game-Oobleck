##############################

import pygame
import random

##############################

pygame.init()

screen_width = 640
screen_height = 480

clock = pygame.time.Clock()

# font = pygame.font.SysFont('Helvetica', 24)
# text = font.render('Elapsed Time : 0 ms', True, (255, 255, 255))
# start_time = pygame.time.get_ticks()

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Oobleck')

##############################

class Character(pygame.sprite.Sprite) :

    def __init__(self, character_x_pos, character_y_pos) :
        super().__init__()
        self.image = pygame.Surface((30, 30))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.x = character_x_pos
        self.rect.y = character_y_pos

    def update(self, keys) :

        if keys[pygame.K_w] : 
            self.rect.y -= 3
        elif keys[pygame.K_s] : 
            self.rect.y += 3            

        if keys[pygame.K_a] : 
            self.rect.x -= 3        
        elif keys[pygame.K_d] : 
            self.rect.x += 3  

##############################

class Object(pygame.sprite.Sprite) :

    def __init__(self, object_x_pos, object_y_pos) :
        super().__init__()
        self.image = pygame.Surface((30, 30))
        self.image.fill((0, 255, 0))
        self.rect = self.image.get_rect()
        self.rect.x = object_x_pos
        self.rect.y = object_y_pos
        self.x_speed = random.randrange(1, 3 + 1)
        self.y_speed = random.randrange(1, 3 + 1)

    def update(self) :
        self.rect.move_ip(self.x_speed, self.y_speed)
        if self.rect.top < 0 :
            self.y_speed = - self.y_speed
        elif self.rect.bottom > screen_height :
            self.y_speed = - self.y_speed            
        elif self.rect.left < 0 :
            self.x_speed = - self.x_speed            
        elif self.rect.right > screen_width :
            self.x_speed = - self.x_speed

##############################

all_sprites = pygame.sprite.Group()

character_init_x_pos, character_init_y_pos = screen_width / 2, screen_height / 2
object_init_x_pos, object_init_y_pos = random.randrange(20, screen_width - 20 + 1), random.randrange(20, screen_height - 20 + 1)

character = Character(character_init_x_pos, character_init_y_pos)
object = Object(object_init_x_pos, object_init_y_pos)

all_sprites.add(character)
all_sprites.add(object)

##############################

running = True

while running :

    keys = pygame.key.get_pressed()
    clock.tick(144)

    for event in pygame.event.get() :
        if event.type == pygame.QUIT or keys[pygame.K_ESCAPE] :
            running = False

    # elapsed_time = pygame.time.get_ticks() - start_time
    # text = font.render('Elapsed Time : {} ms'.format(elapsed_time), True, (255, 255, 255))

    if character.rect.colliderect(object.rect) :
        all_sprites.remove(object)

    character.update(keys)
    object.update()
    screen.fill((0, 0, 0))
    # screen.blit(text, (10, 10))
    all_sprites.draw(screen)
    pygame.display.update()

pygame.quit()

##############################