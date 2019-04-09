# Save this file as something meaningful!
# Unless you want your game to be callled skeleton...


import pygame
from pygame.math import Vector2
from random import randint

# Setup
pygame.init()

WHITE = (255, 255, 255)
RED   = (255,   0,   0)
GREEN = (  0, 255,   0)
BLUE  = (  0,   0, 255)
BLACK = (  0,   0,   0)
SPACE = (  1,   5,  41)

# Screen
width = 400
height = 700
size = [width, height]
screen = pygame.display.set_mode(size)

# Objects and variables
done = False
clock = pygame.time.Clock()
x_speed = 0
y_speed = 0
small_font = pygame.font.SysFont("Incised901 Ndlt BT", 30)
hit_count = 0


SPAWN_BIG = pygame.USEREVENT + 1
SPAWN_COMET = pygame.USEREVENT + 2



# Keys
Key_a = False
Key_d = False




class Ship(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.speed = Vector2(0, 0)

        self.image = pygame.image.load('ship.png')
        self.image = pygame.transform.scale(self.image, (46, 78))
        self.mask = pygame.mask.from_surface(self.image)

        self.rect = self.image.get_rect()
        self.rect.x = width/2
        self.rect.y = height-100
        self.radius = 76

    def update(self):
        self.rect.x += self.speed.x
        self.rect.y += self.speed.y




class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.speed = Vector2(0, 5)

        self.image = pygame.image.load('comet.png')
        self.image = pygame.transform.scale(self.image, (26, 82))
        self.mask = pygame.mask.from_surface(self.image)
        #self.image.set_colorkey(WHITE)

        self.rect = self.image.get_rect()
        self.rect.x = randint(0, width - 82)
        self.rect.y = -82
        self.radius = 80

    def update(self):
        self.rect.x += self.speed.x
        self.rect.y += self.speed.y




class BigEnemy(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.speed = Vector2(0, 2)

        self.image = pygame.image.load('comet.png')
        self.image = pygame.transform.scale(self.image, (200, 400))
        self.mask = pygame.mask.from_surface(self.image)
        #self.image.set_colorkey(WHITE)

        self.rect = self.image.get_rect()
        self.rect.x = randint(0, width - 200)
        self.rect.y = -300
        self.radius = 398

    def update(self):
        self.rect.x += self.speed.x
        self.rect.y += self.speed.y




# Create Objects
# All the objects to be on the screen when the game starts.
player_ship = Ship()

# Handle sprites
# Create as many Sprite groups as you need to make things easy to manage.
# all_sprites contains all the objects we'll ever create. All objects must be
# added to the all_sprites Group for things to work.
all_sprites = pygame.sprite.Group()
all_sprites.add(player_ship)
all_bullets = pygame.sprite.Group()
all_comets = pygame.sprite.Group()




comet = Enemy()

all_sprites.add(comet)
all_comets.add(comet)



bigcomet = BigEnemy()

all_sprites.add(bigcomet)
all_comets.add(bigcomet)







# -------- Main Program Loop -----------
# we use the global variable done to control when to end the game.
while not done:
    # --- Event Processing
    # Get all events from keyboard and/or mouse.
    for event in pygame.event.get():
        # if you click the x in the window top the game will end
        if event.type == pygame.QUIT:
            done = True


        # if you press a key and it is either A or D change the speed of
        # the x_speed variable.
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                Key_a = True
                x_speed = -3
            if event.key == pygame.K_d:
                Key_d = True
                x_speed = 3



            if event.key == pygame.K_o:
                comet = Enemy()

                all_sprites.add(comet)
                all_comets.add(comet)



            if event.key ==pygame.K_p:
                bigcomet = BigEnemy()

                all_sprites.add(bigcomet)
                all_comets.add(bigcomet)






        # When the A or D  key is released change the x_speed to 0.
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                Key_a = False
                x_speed = 0
                if Key_d == True:
                    x_speed = 3

            if event.key == pygame.K_d:
                Key_d = False
                x_speed = 0
                if Key_a == True:
                    x_speed = -3



        elif event.type == SPAWN_COMET:
            comet = Enemy()

            all_sprites.add(comet)
            all_comets.add(comet)

            pygame.time.set_timer(SPAWN_COMET, 600)




        elif event.type == SPAWN_BIG:
            bigcomet = BigEnemy()

            all_sprites.add(bigcomet)
            all_comets.add(bigcomet)

            pygame.time.set_timer(SPAWN_BIG, 5000)







    # --- Game Logic
    # Update variables
    player_ship.speed.x = x_speed
    all_sprites.update()

    # Collisions
    # Read the documentation of groupcollide very carefully and figure out
    # how the arguments work.
    hit_list = pygame.sprite.groupcollide(all_comets, all_bullets, True, True)
    hit_count += len(hit_list)

    collision = pygame.sprite.spritecollideany(player_ship, all_comets)
    if collision:
        real_collision = pygame.sprite.collide_mask(player_ship, collision)
        if real_collision:
            done = True


    # --- Draw
    # When using Sprite groups it is super easy to update the screen:
    # 1. Clear the screen.
    # 2. Call the draw method of the all_sprites Group using the screen as the
    #    only argument.
    screen.fill(SPACE)
    all_sprites.draw(screen)

    hit_text = small_font.render("Hits: " + str(hit_count), 1, BLACK)
    screen.blit(hit_text, (10, 10))

    # Update screen
    # pygame will draw the screen in the background and only when it is time
    # to update it will it be shown on the screen.
    clock.tick(60)  # update the screen 30 times every second.
    pygame.display.flip()


# When we break out of the gmae loop there is nothing to do but..
# Close the window and quit.
pygame.quit()
