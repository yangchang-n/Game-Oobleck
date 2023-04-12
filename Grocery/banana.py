import pygame
import random

pygame.init()

screen_width = 1280
screen_height = 720

clock = pygame.time.Clock()

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Banana')

class Character(pygame.sprite.Sprite) :

    def __init__(self, x, y) :
        super().__init__()
        self.image = pygame.Surface((30, 30))
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y

    def update(self, keys) :

        if keys[pygame.K_w] :
            self.rect.y -= 3
        elif keys[pygame.K_s] :
            self.rect.y += 3

        if keys[pygame.K_a] :
            self.rect.x -= 3
        elif keys[pygame.K_d] :
            self.rect.x += 3

class Oobleck(pygame.sprite.Sprite) :

    def __init__(self, x, y) :
        super().__init__()
        self.image = pygame.Surface((30, 30))
        self.image.fill((240, 220, 80))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y
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

all_sprites = pygame.sprite.Group()

character_xpos, character_ypos = screen_width / 2, screen_height / 2
oobleck_xpos, oobleck_ypos = random.randrange(20, screen_width - 20 + 1), random.randrange(20, screen_height - 20 + 1)

character = Character(character_xpos, character_ypos)
oobleck = Oobleck(oobleck_xpos, oobleck_ypos)

all_sprites.add(character)
all_sprites.add(oobleck)

running = True

while running :

    keys = pygame.key.get_pressed()
    clock.tick(60)

    for event in pygame.event.get() :
        if event.type == pygame.QUIT or keys[pygame.K_ESCAPE] :
            running = False

    if character.rect.colliderect(oobleck.rect) :
        all_sprites.remove(oobleck)

    character.update(keys)
    oobleck.update()
    screen.fill((0, 0, 0))
    all_sprites.draw(screen)
    pygame.display.update()

pygame.quit()