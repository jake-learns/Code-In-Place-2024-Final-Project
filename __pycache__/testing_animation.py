from spritesheet import *
import pygame


pygame.init()

SCREEN_HEIGHT = 900
SCREEN_WIDTH = 1600

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Test")


#creation animation list
animation_list = []
animation_steps =  8
sprite_sheet_image = pygame.image.load("spaceship\\unused\Evasion.png").convert_alpha()
destroyed_prite_sheet = SpriteSheet(sprite_sheet_image, animation_steps)

for image in range(animation_steps):
    animation_list.append(destroyed_prite_sheet.get_image(image, 3))

BG = "white"
BLACK  = "black"
run = True

last_update = pygame.time.get_ticks()
animation_cooldown = 100 #milliseconds
frame = 0

while run:

    #update background
    screen.fill(BLACK)

    #update anmation
    current_time = pygame.time.get_ticks()
    if current_time - last_update >=  animation_cooldown:
        frame += 1
        last_update = current_time
        print(len(animation_list))
        if frame >= len(animation_list):
            frame = 0


    #display image
    for x in range(animation_steps):
        screen.blit(animation_list[frame], (0, 0))

    #handles events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()