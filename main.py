#some audio effects from https://www.zapsplat.com/
#music from https://onemansymphony.bandcamp.com/album/wreckage-free
#sprites from https://craftpix.net/freebies/free-spaceship-pixel-art-sprite-sheets/?num=1&count=53&sq=ship&pos=4

import pygame
import random
import math
import time

# pygame setup
pygame.init()
dt = 0
FPS = 60
SCREEN_HEIGHT = 900
SCREEN_WIDTH = 1600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

#defines game states
running = True
playing = False
menu = True
options_menu = False
game_over = False
bob_mode = False
player_win = False

#defines some additional game variables
score = 0
player_lives = 3
volume = .1
font = pygame.font.Font("SF Atarian System.ttf", 40)
winning_score = 1000

#loads music
pygame.mixer.pre_init(44100, -16, 2, 512)
menu_music = pygame.mixer.music.load('One Man Symphony - Wreckage (Free)/One Man Symphony - Wreckage (Free) - 01 Black Holes (Action 01) - Loops.mp3')
pygame.mixer.music.set_volume(volume)
pygame.mixer.music.play(-1, .5, 2500)
pygame.mixer.set_num_channels(64)

#loads some sound files
player_sound = pygame.mixer.Sound("audio/zapsplat_cartoon_anime_laser_blash_short_weak_92469.mp3")
boss_incoming = pygame.mixer.Sound("audio/boss_incoming.wav")
boss_pew = pygame.mixer.Sound("audio/boss_shoot_sound_2.ogg")
boss_pew.set_volume(volume)
boss_image = pygame.image.load("enemies/Boss/boss.png").convert_alpha()

bob_channel = pygame.mixer.Channel(29)
bob_pew = pygame.mixer.Sound("audio/bob_pews.mp3")
bob_pew.set_volume(volume)
bob_boss = pygame.image.load("enemies/Boss/bob_boss.png").convert_alpha()
boss_channel = pygame.mixer.Channel(28)

#default (x, y) offset for the ship
ship_y_offset = 54
ship_x_offset = 40



#loads background images and defines variables unique to them
bg_one = pygame.image.load("backgrounds/bg_1.png").convert_alpha()
bg_one_width = bg_one.get_width()
bg_one_tiles = math.ceil(SCREEN_WIDTH / bg_one_width) + 1 
bg_one_scroll = 0

bg_two = pygame.image.load("backgrounds/bg_2.png").convert_alpha()
bg_two_width = bg_two.get_width()
bg_two_tiles = math.ceil(SCREEN_WIDTH / bg_two_width) + 1 
bg_two_scroll = 0

bg_three = pygame.image.load("backgrounds/bg_3.png").convert_alpha()
bg_three_width = bg_three.get_width()
bg_three_tiles = math.ceil(SCREEN_WIDTH / bg_three_width) + 1 
bg_three_scroll = 0

bg_menu = pygame.image.load("backgrounds/menu.png").convert_alpha()
option_menu = pygame.image.load("backgrounds/controls_menu.png").convert_alpha()


full_lives = pygame.image.load("spaceship/Working Folder/Full Lives.png").convert_alpha()
two_lives = pygame.image.load("spaceship/Working Folder/Two Lives.png").convert_alpha()
one_lives = pygame.image.load("spaceship/Working Folder/One Life.png").convert_alpha()

class Player(pygame.sprite.Sprite):
    
    cooldown = 333#milliseconds
    shoot_sound = player_sound
    shoot_sound.set_volume(volume)

    def __init__(self):
        super().__init__()
        self.lastshot = pygame.time.get_ticks()
        self.animation_speed = 0.2
        self.alive = True

        #loads all the images for the animation of the ship idling
        self.space_ship = []
        for i in range(1, 7):
            self.space_ship.append(pygame.image.load(f"spaceship/Working Folder/move_{i}.png").convert_alpha())

        #loads all the images for the animation of the ship idling
        self.space_ship2 = []
        for i in range(1, 6):
            self.space_ship2.append(pygame.image.load(f"spaceship/Working Folder/boost_{i}.png").convert_alpha())

        #loads all the images for the animation of the ships exploding
        self.destroyed = []
        for i in range(1, 16):
            self.destroyed.append(pygame.image.load(f"spaceship/unused/destroyed_{i}.png"))

        #loads all the images for the animation of the ship moving forward while turning down
        self.space_ship_turning_down_boost = [pygame.image.load("spaceship/Working Folder/turn_up_half_boost.png").convert_alpha()]
        for i in range(1, 6):
            self.space_ship_turning_down_boost.append(pygame.image.load(f"spaceship/Working Folder/turn_down_full_boost_{i}.png").convert_alpha())
        
        #loads all the images for the animation of the ship moving forward while turning up
        self.space_ship_turning_up_boost = [pygame.image.load("spaceship/Working Folder/turn_down_half_boost.png").convert_alpha()]
        for i in range(1, 6):
            self.space_ship_turning_up_boost.append(pygame.image.load(f"spaceship/Working Folder/turn_up_full_boost_{i}.png").convert_alpha())


        #loads all the images for the animation of the ship turning down
        self.space_ship_turning_down = [pygame.image.load("spaceship/Working Folder/turn_down_half_moving.png").convert_alpha()]
        for i in range(1, 7):
            self.space_ship_turning_down.append(pygame.image.load(f"spaceship/Working Folder/turn_down_full_moving_{i}.png").convert_alpha())

        #loads all the images for the animation of the ship turning up
        self.space_ship_turning_up = [pygame.image.load("spaceship/Working Folder/turn_up_half_moving.png").convert_alpha()]
        for i in range(1, 7):
            self.space_ship_turning_up.append(pygame.image.load(f"spaceship/Working Folder/turn_up_full_moving_{i}.png").convert_alpha())

        #loads animations for the return to moving state
        self.return_to_idle_neg_1 = [ pygame.image.load("spaceship/Working Folder/turn_down_half_moving.png").convert_alpha(),  pygame.image.load("spaceship/Working Folder/idle.png").convert_alpha()]
        self.return_to_idle_1 = [ pygame.image.load("spaceship/Working Folder/turn_up_half_moving.png").convert_alpha(),  pygame.image.load("spaceship/Working Folder/idle.png").convert_alpha()]

        #loads all the images for the animation of the ship turning both down and up while moving forward
        self.ship_return_to_center_top = pygame.image.load("spaceship/Working Folder/turn_up_half_moving.png").convert_alpha()
        self.ship_return_to_center_bottom = pygame.image.load("spaceship/Working Folder/turn_down_half_moving.png").convert_alpha()

        #loads all the images for the animation of the ship turning both down and up while moving forward
        self.ship_boost_return_to_center_top = pygame.image.load("spaceship/Working Folder/turn_up_half_boost.png").convert_alpha()
        self.ship_boost_return_to_center_bottom = pygame.image.load("spaceship/Working Folder/turn_down_half_boost.png").convert_alpha()

        #variables to store current index valuesfor various animation states
        self.ship_idle_index = 0
        self.ship_thrust_index = 0
        self.ship_turning_index = 0
        self.destruction_index = 0

        #sets the starting image and position for the ship
        self.image = self.space_ship[self.ship_thrust_index]
        self.rect = self.image.get_rect(center = (150,SCREEN_HEIGHT//2))

        #variable to indidcate the previous turn direction, used to trasition image back to idle 1 from up, -1 from down
        self.from_down = -1
        self.from_up = 1
        self.previous_turn = 0



        # #loads all the images for the animation of the ship turning both down and up, while not going foward
        # self.ship_turning_down = [ pygame.image.load("spaceship/turn_down_1.png").convert_alpha(),  pygame.image.load("spaceship/turn_down_2.png").convert_alpha()]
        # self.ship_turning_up = [ pygame.image.load("spaceship/turn_up_1.png").convert_alpha(),  pygame.image.load("spaceship/turn_up_2.png").convert_alpha()]

        #loads the sound files related to the ship
        self.shoot_channel = pygame.mixer.Channel(32)
        self.thruster_channel = pygame.mixer.Channel(31)
        self.thrusters_sound = pygame.mixer.Sound("audio/zapsplat_science_fiction_spaceship_station_drone_loud.mp3")
        self.thrusters_sound.set_volume(volume)
        self.explosion_sound = pygame.mixer.Sound("audio/explosion.ogg")
        self.explosion_channel = pygame.mixer.Channel(30)
        
    def player_input(self, keys):
        keys = pygame.key.get_pressed()
        # mouse = pygame.mouse.get_pressed()

        if keys[pygame.K_w] and self.rect.top >  -ship_y_offset:
            self.rect.y -= 600 * dt
        if keys[pygame.K_s] and self.rect.bottom < SCREEN_HEIGHT + ship_y_offset:
            self.rect.y += 600 * dt
        if keys[pygame.K_a] and self.rect.left > - ship_x_offset:
            self.rect.x -= 450 * dt
        if keys[pygame.K_d] and self.rect.right < SCREEN_WIDTH//5*3+ ship_x_offset:
            self.rect.x += 450 * dt
            if not self.thruster_channel.get_busy():
                self.thruster_channel.play(self.thrusters_sound)
        if not keys[pygame.K_d]:
            self.thrusters_sound.stop()

    
        #shoots and checks to see if the time since last shot is greater than the defined cooldown
        time_now = pygame.time.get_ticks()
        if keys[pygame.K_SPACE] and time_now - self.lastshot > self.cooldown:
            bullet = Bullets(self.rect.centerx, self.rect.centery, 1)
            player_bullets_group.add(bullet)
            self.lastshot = time_now
            self.shoot_channel.play(self.shoot_sound) 

    def explode(self):
        global player_lives

        if not self.explosion_channel.get_busy():
            self.explosion_channel.play(self.explosion_sound)
        self.destruction_index += 0.15
        if self.destruction_index >= len(self.destroyed):
            player_lives -= 1
            self.kill()
        else:
            self.image = self.destroyed[int(self.destruction_index)]

    def animation_state(self, keys):

        if keys[pygame.K_d] and keys[pygame.K_w]:
            self.ship_turning_index += self.animation_speed
            if self.ship_turning_index >= len(self.space_ship_turning_up_boost):
                self.ship_turning_index = 1
            self.image = self.space_ship_turning_up_boost[int(self.ship_turning_index)]
            self.ship_idle_index = 0
            self.ship_thrust_index = 0
            self.previous_turn = self.from_up

        elif keys[pygame.K_d] and keys[pygame.K_s]:
            self.ship_turning_index += self.animation_speed
            if self.ship_turning_index >= len(self.space_ship_turning_down_boost):
                self.ship_turning_index = 1
            self.image = self.space_ship_turning_down_boost[int(self.ship_turning_index)]
            self.ship_thrust_index = 0
            self.previous_turn = self.from_down

        elif keys[pygame.K_s]:
            #since only two frames in downward turn, check index at start
            self.ship_turning_index += self.animation_speed
            if self.ship_turning_index >= len(self.space_ship_turning_down):
                self.ship_turning_index = 1
            self.image = self.space_ship_turning_down[int(self.ship_turning_index)]
            #sets to -1 to know there was a previous turn up for return to idle animation frames
            self.previous_turn = self.from_down
            #will set next idle loop to 0
            self.ship_idle_index = 0
            self.ship_thrust_index = 0

        elif keys[pygame.K_w]:
            #since only two frames in upward turn, check index at start
            self.ship_turning_index += self.animation_speed
            if self.ship_turning_index >= len(self.space_ship_turning_up):
                self.ship_turning_index = 1
            self.image = self.space_ship_turning_up[int(self.ship_turning_index)]
            #sets to 1 to know there was a previous turn up for return to idle animation frames
            self.previous_turn = self.from_up
            #will set next idle loop to 0
            self.ship_idle_index = 0
            self.ship_thrust_index = 0
            
        elif keys[pygame.K_d]:
            if self.previous_turn == self.from_up:
                self.ship_thrust_index += self.animation_speed
                self.image = self.ship_boost_return_to_center_top
                if self.ship_thrust_index >= 1:
                    self.previous_turn = 0
            elif self.previous_turn == self.from_down:
                self.ship_thrust_index += self.animation_speed
                self.image = self.ship_boost_return_to_center_bottom
                if self.ship_thrust_index >= 1:
                    self.previous_turn = 0
            else:
                self.ship_thrust_index += self.animation_speed
                if self.ship_thrust_index >= len(self.space_ship2):
                    self.ship_thrust_index = 0
                self.image = self.space_ship2[int(self.ship_thrust_index)]
            self.ship_turning_index = 0
            self.ship_idle_index = 0

        else:
            if self.previous_turn == self.from_up:
                self.ship_idle_index += self.animation_speed
                self.image = self.ship_return_to_center_top
                if self.ship_idle_index >= 1:
                    self.previous_turn = 0
            elif self.previous_turn == self.from_down:
                self.ship_idle_index += self.animation_speed
                self.image = self.ship_return_to_center_bottom
                if self.ship_idle_index >= 1:
                    self.previous_turn = 0
            else:
                self.ship_idle_index += self.animation_speed
                if self.ship_idle_index >= len(self.space_ship):
                    self.ship_idle_index = 0
                self.image = self.space_ship[int(self.ship_idle_index)]
            self.ship_thrust_index = 0
            self.ship_turning_index = 0
        
        #update mask
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        if self.alive:
            keys = pygame.key.get_pressed()
            self.player_input(keys)
            # self.apply_gravity()
            self.animation_state(keys)
        else:
            self.thrusters_sound.stop()
            self.explode()
        # self.rotate_toward_mouse()

class Bullets(pygame.sprite.Sprite):
    animation_speed = 0.2
    animation_list = []
    for i in range(1, 5):
        image = pygame.image.load(f"enemies/enemy_1/rocket_{i}.png").convert_alpha()
        image = pygame.transform.scale_by(image, 2)
        animation_list.append(image)
        rocket = pygame.mixer.Sound("audio/cartoon_rocket_launch.wav")
    def __init__(self,x,y, origin):
        super().__init__()
        self.x = x
        self.y = y
        self.origin = origin
        self.animation_index = 0
        if origin == 1:
            self.image = pygame.image.load("spaceship/unused/blue_laser.png").convert_alpha()
        elif origin == -1:
            self.image = self.animation_list[self.animation_index]
        elif origin == -2:
            self.y_speed = random.randrange(-10,10)
            self.image = pygame.image.load("enemies/Boss/ball_red_2.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = [x,y]
        

    def animate(self):
        if self.origin == -1:
            self.animation_index += self.animation_speed
            if self.animation_index >= len(self.animation_list):
                self.animation_index = 0
            self.image = self.animation_list[int(self.animation_index)]

    def update(self):
        global score

        if self.origin == 1:
            self.rect.x += 800 * dt
            if pygame.sprite.spritecollide(self, enemies_group, True, pygame.sprite.collide_mask):
                score += 50
                self.kill()
            if pygame.sprite.spritecollide(self, boss_group, False, pygame.sprite.collide_mask):
                boss_group.sprite.health -= 1
                self.kill()
            if self.rect.left > SCREEN_WIDTH:
                self.kill()
        elif self.origin == -1: 
            self.rect.x -= 800 * dt
            if pygame.sprite.spritecollide(self, player, False, pygame.sprite.collide_mask):
                self.kill()
                player.sprite.alive = False
            if self.rect.right < 0:
                self.kill()
        elif self.origin == -2: 
            self.rect.x -= 400 * dt
            self.rect.y += self.y_speed
            if pygame.sprite.spritecollide(self, player, False, pygame.sprite.collide_mask):
                self.kill()
                player.sprite.alive = False
            if self.rect.right < 0:
                self.kill()

class Enemy(pygame.sprite.Sprite):
    shoot_cooldown = 2400 #milliseconds
    rocket = pygame.mixer.Sound("audio/cartoon_rocket_launch.wav")
    rocket.set_volume(volume)
    animation_speed = 0.2
    animation_list = []
    for i in range(1, 7):
        image = pygame.image.load(f"enemies/enemy_1/boost_{i}.png").convert_alpha()
        image = pygame.transform.scale_by(image, .75)
        animation_list.append(image)

    def __init__(self, y):
        super().__init__()
        #sets the starting image and position for the enemy
        self.animation_index = 0
        self.lastshot = pygame.time.get_ticks()
        self.image = self.animation_list[0]
        self.rect = self.image.get_rect(center = (SCREEN_WIDTH + self.image.get_width() , y))
    
    def animate(self):
        self.animation_index += self.animation_speed
        if self.animation_index >= len(self.animation_list):
            self.animation_index = 0
        self.image = self.animation_list[int(self.animation_index)]
        #update mask used for collision detection
        self.mask = pygame.mask.from_surface(self.image)

    def shoot(self):
        time_now = pygame.time.get_ticks()
        if time_now - self.lastshot > Enemy.shoot_cooldown:
            bullet = Bullets(self.rect.centerx, self.rect.centery, -1)
            enemy_bullets_group.add(bullet) 
            self.lastshot = time_now
            self.rocket.play()

    def update(self):
        self.animate()
        self.shoot()
        self.rect.x -= 200 * dt
        if pygame.sprite.spritecollide(self, player, False, pygame.sprite.collide_mask):
            self.kill()
            player.sprite.alive = False
        if self.rect.centerx <= 0 - self.image.get_width():
            self.kill()

class Boss(pygame.sprite.Sprite):
    shoot_cooldown = 25 #50 seems like a good default value
    def __init__(self):
        super().__init__()
        #sets the starting image and position for the enemy
        self.lastshot = pygame.time.get_ticks()
        self.image = boss_image
        self.rect = self.image.get_rect(center = (SCREEN_WIDTH + self.image.get_width() , SCREEN_HEIGHT//2))
        self.mask = pygame.mask.from_surface(self.image)
        self.move_up = random.choice([True, False])
        self.health = 50
        self.alive = True

    def shoot(self):
        time_now = pygame.time.get_ticks()
        if time_now - self.lastshot > Boss.shoot_cooldown:
            bullet = Bullets(self.rect.midleft[0], self.rect.midleft[1], -2)
            enemy_bullets_group.add(bullet) 
            self.lastshot = time_now
            if not bob_channel.get_busy():
                bob_channel.play(boss_pew)

    def update(self):
        if self.health <= 0:
            self.alive = False
            self.kill()
        if self.alive:
            if self.rect.x > (SCREEN_WIDTH//5)*3:
                self.rect.x -= 200 * dt
            else:
                if self.rect.midtop[1] <= 0:
                    self.move_up = False
                elif self.rect.midbottom[1] >= SCREEN_HEIGHT:
                    self.move_up = True

                if self.move_up:
                    self.rect.y -= 200 * dt
                else:
                    self.rect.y += 200 * dt
                self.shoot()

class Button():
    def __init__(self, x, y, image) :
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        self.clicked = False

    def update(self):
        pos = pygame.mouse.get_pos()

        action = False

        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] and self.clicked == False:
                action = True
                self.clicked = True

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False
        
        screen.blit(self.image, self.rect.topleft)

        return action


#defines some functions for scrolling the background images
def draw_bg_one():
    for i in range(0, bg_one_tiles):
        screen.blit(bg_one, (i * bg_one_width + bg_one_scroll,0))

def draw_bg_two():
    for i in range(0, bg_two_tiles):
        screen.blit(bg_two, (i * bg_two_width + bg_two_scroll,0))

def draw_bg_three():
    for i in range(0, bg_three_tiles):
        screen.blit(bg_three, (i * bg_three_width + bg_three_scroll,0))

def draw_menu(menu):
    screen.blit(menu, (0,0))

#displays players life count
def display_current_lives(screen):
    if player_lives == 3:
        screen.blit(pygame.transform.scale_by(full_lives, .75), (10, 10))
    elif player_lives == 2:
        screen.blit(pygame.transform.scale_by(two_lives, .75), (10, 10))
    elif player_lives == 1:
        screen.blit(pygame.transform.scale_by(one_lives, .75), (10, 10))

def display_score(screen, score, font, color, location):
    img = font.render(f"Score: {score}", True, color)
    screen.blit(img, location)

def display_text(screen, text, font, color, location):
    img = font.render(text, True, color)
    screen.blit(img, location)

def display_win_message(screen, font, color):
        you_win = font.render(f"YOU WIN!", True, color)
        screen.blit(you_win, (SCREEN_WIDTH//2, SCREEN_HEIGHT//2))

def respawn():
    player.add(Player())
    enemies_group.empty()
    enemy_bullets_group.empty()
    
#creates the player and adds them to a Sprite group
player = pygame.sprite.GroupSingle()
player.add(Player())

#creates the group that will house all bullets created
player_bullets_group = pygame.sprite.Group()
enemy_bullets_group = pygame.sprite.Group()

#creates the group that will house all the enemies created
enemies_group = pygame.sprite.Group()

#creates the group that will house the boss created
boss_group = pygame.sprite.GroupSingle()
boss_spawned = False
#defines spawner cooldown for enemies
enemy_spanwer_cooldown = 1500
last_enemy_spawned = pygame.time.get_ticks()

#initialize the buttons for main menu
start = pygame.image.load("buttons/start_yellow.png").convert_alpha()
start_button = Button(bg_menu.get_width() * .82 , (SCREEN_HEIGHT//6), start)

#initialize the buttons for main menu
options = pygame.image.load("buttons/options_yellow.png").convert_alpha()
options_button = Button(bg_menu.get_width() * .82, (SCREEN_HEIGHT//6) * 3, options)

#initialize the buttons for main menu
exits = pygame.image.load("buttons/exit_yellow.png").convert_alpha()
exit_button = Button(bg_menu.get_width() * .82, (SCREEN_HEIGHT//6) * 5, exits)

#initialize the buttons for the extra menus
back = pygame.image.load("buttons/back_yellow.png").convert_alpha()
back_button = Button(bg_menu.get_width() * .82, (SCREEN_HEIGHT//6) * 5, back)

#initialize the buttons for the extra menus
restart = pygame.image.load("buttons/restart_yellow.png").convert_alpha()
restart_button = Button(bg_menu.get_width() * .82, (SCREEN_HEIGHT//6) * 5, restart)

bob = pygame.image.load("buttons/bob.png").convert_alpha()
bob = pygame.transform.scale_by(bob, .75)
bob_button = Button(bg_menu.get_width() * .82, (SCREEN_HEIGHT//6)//2, bob)

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE and menu == False:
                game_music = pygame.mixer.music.load('One Man Symphony - Wreckage (Free)/One Man Symphony - Wreckage (Free) - 01 Black Holes (Action 01) - Loops.mp3')
                pygame.mixer.music.play(-1, .5, 2500)
                menu = True
                playing = False
                pygame.mouse.set_visible(True)
            #if player dead, respawn and reset enemy respawn timer
            if not player and player_lives > 0:
                if event.key == pygame.K_SPACE:
                    respawn()
                    enemy_spanwer_cooldown = 1500
 
    if menu:
        draw_menu(bg_menu)
        
        if start_button.update():
            start_button.image = pygame.image.load("buttons/resume_yellow.png").convert_alpha()
            game_music = pygame.mixer.music.load('One Man Symphony - Wreckage (Free)/One Man Symphony - Wreckage (Free) - 02 Unknown (Action 02) - Loops.mp3')
            pygame.mixer.music.play(-1, .5, 2500)
            playing = True
            menu = False
            #hide mouse
            pygame.mouse.set_visible(False)
            for enemy in enemies_group:
                enemy.lastshot = random.randint(pygame.time.get_ticks() - 2400, pygame.time.get_ticks())

        if options_button.update():
            menu = False
            options_menu = True
        
        if exit_button.update():
            running = False
            pygame.quit()
            quit()

    #displays the options menu to the user, which contains the controls, a back button, and bob mode
    if options_menu:
        draw_menu(option_menu)
        if back_button.update():
            menu = True
            options_menu = False
            time.sleep(.2)
        #allows user to enter bob mode
        if not bob_mode:
            if bob_button.update():
                boss_pew = bob_pew
                bob_mode = True
                boss_image = bob_boss

    if playing:

        if player_lives == 0:
            playing = False
            game_over = True
            pygame.mixer.stop()        
        
        #spawns enemies at an increasingly faster rate
        time_now = pygame.time.get_ticks()
        if time_now - last_enemy_spawned >= enemy_spanwer_cooldown and score < winning_score:
            enemies_group.add(Enemy(random.randint(50,SCREEN_HEIGHT-50)))
            last_enemy_spawned = time_now
            if enemy_spanwer_cooldown > 500:
                enemy_spanwer_cooldown -= 50

        #spawns boss if score is achieved and enemies have stopped spawning
        elif time_now - last_enemy_spawned >= enemy_spanwer_cooldown and score >= winning_score:
            if not boss_group and not boss_spawned:
                boss_channel.play(boss_incoming)
                pygame.mixer.music.stop()
                boss_group.add(Boss())
                boss_spawned = True
        
        #if boss was spawned and then killed, player wins end game
        if not boss_group and boss_spawned:
            player_win = True
            score = 99999
            playing = False
            game_over = True
            pygame.mixer.stop()
        
        #loads boss music once the warnng sound is done
        if boss_spawned and not boss_channel.get_busy() and not pygame.mixer.music.get_busy():
            game_music = pygame.mixer.music.load('One Man Symphony - Wreckage (Free)/One Man Symphony - Wreckage (Free) - 03 Singularity (Action 03) - Loops.mp3')
            pygame.mixer.music.play(-1, .5, 2500)

        # scrolls the background endlessly with 3 tiles, creating a parallax effect
        bg_one_scroll -= .5
        if abs(bg_one_scroll) > bg_one_width:
            bg_one_scroll = 0
        draw_bg_one()    

        bg_two_scroll -= 1.5
        if abs(bg_two_scroll) > bg_two_width:
            bg_two_scroll = 0
        draw_bg_two()

        bg_three_scroll -= 2
        if abs(bg_three_scroll) > bg_three_width:
            bg_three_scroll = 0
        draw_bg_three()

        #begins updates
        player_bullets_group.update()
        enemy_bullets_group.update()
        enemies_group.update()
        player.update()
        boss_group.update()

        #draw groups to screen
        player.draw(screen)  
        display_current_lives(screen)
        display_score(screen, score, font, "white", (25, 100))
        player_bullets_group.draw(screen)    
        enemy_bullets_group.draw(screen)
        enemies_group.draw(screen)   
        boss_group.draw(screen)
        if not player and player_lives > 0:
            display_text(screen, "Press SPACE to respawn!", font, "white", (SCREEN_WIDTH//2 - 120, SCREEN_HEIGHT//2-20))
        
    if game_over:
        pygame.mouse.set_visible(True)
        draw_menu(bg_menu)
        display_score(screen, score, font, "white", (bg_menu.get_width() * .77, 300))
        #display win or lose message
        if player_win == True:
            display_text(screen, "You win!", font, "white", (bg_menu.get_width() * .78, 100))
        else:
            display_text(screen, "You lose!", font, "white", (bg_menu.get_width() * .78, 100))
        
        if restart_button.update():
            #user clicked restart button, reset all values
            score = 0
            player_lives = 3
            start_button.image = pygame.image.load("buttons/start_yellow.png").convert_alpha()
            respawn()
            boss_group.empty()
            game_over = False
            menu = True
            boss_spawned = False
            player_win = False
            bob_mode = False
            boss_image = pygame.image.load("enemies/Boss/boss.png")
            boss_pew = pygame.mixer.Sound("audio/boss_shoot_sound_2.ogg")
            boss_pew.set_volume(volume)
            game_music = pygame.mixer.music.load('One Man Symphony - Wreckage (Free)/One Man Symphony - Wreckage (Free) - 01 Black Holes (Action 01) - Loops.mp3')
            pygame.mixer.music.play(-1, .5, 2500)
            time.sleep(.2)

    # update() the display show was drawn above
    pygame.display.update()
    # limits FPS to 60 and inits dt as a variable to perform calculations
    dt = clock.tick(FPS) / 1000

pygame.quit()
