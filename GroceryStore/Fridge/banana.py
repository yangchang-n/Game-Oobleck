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

class Konjac(pygame.sprite.Sprite) :

    def __init__(self, x, y) :
        super().__init__()
        self.image = pygame.Surface((30, 30))
        self.image.fill((120, 120, 120))
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

characters = pygame.sprite.Group()
objects = pygame.sprite.Group()

character_xpos, character_ypos = (screen_width / 2) - 15, (screen_height / 2) - 15
oobleck_xpos, oobleck_ypos = random.randrange(10, screen_width - 40 + 1), random.randrange(10, screen_height - 40 + 1)
konjac_xpos, konjac_ypos = random.randrange(10, screen_width - 40 + 1), random.randrange(10, screen_height - 40 + 1)

character = Character(character_xpos, character_ypos)
oobleck = Oobleck(oobleck_xpos, oobleck_ypos)
konjac = Konjac(konjac_xpos, konjac_ypos)

characters.add(character)
objects.add(oobleck)
objects.add(konjac)

running = True

while running :

    screen.fill((0, 0, 0))
    keys = pygame.key.get_pressed()
    clock.tick(60)

    for event in pygame.event.get() :
        if event.type == pygame.QUIT or keys[pygame.K_ESCAPE] :
            running = False

    if character.rect.colliderect(oobleck.rect) :
        objects.remove(oobleck)

    characters.update(keys)
    objects.update()

    characters.draw(screen)
    objects.draw(screen)

    pygame.display.update()

pygame.quit()