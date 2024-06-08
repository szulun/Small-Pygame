import sys
import os
import pygame
import random

FPS = 60
WIDTH = 500
HEIGHT = 600

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)


# 初始化并创建窗口
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Z's game")
clock = pygame.time.Clock()

# 加载图像
background_img_path = "/Users/z/Desktop/pygame_env/img/background.png"
background_img = pygame.image.load(background_img_path).convert()
background_img = pygame.transform.scale(background_img, (WIDTH, HEIGHT))

player_img_path = "/Users/z/Desktop/pygame_env/img/player.png"
player_img = pygame.image.load(player_img_path).convert()
player_img = pygame.transform.scale(player_img, (50, 40))
player_mini_img = pygame.transform.scale(player_img, (25, 19))
player_mini_img.set_colorkey(BLACK)
pygame.display.set_icon(player_mini_img)
bullet_img_path = "/Users/z/Desktop/pygame_env/img/bullet.png"
bullet_img = pygame.image.load(bullet_img_path).convert()
bullet_img = pygame.transform.scale(bullet_img, (10, 10))

rock_img_paths = [
    "/Users/z/Desktop/pygame_env/img/rock1.png", 
    "/Users/z/Desktop/pygame_env/img/rock2.png", 
    "/Users/z/Desktop/pygame_env/img/rock3.png",
    "/Users/z/Desktop/pygame_env/img/rock4.png",
    "/Users/z/Desktop/pygame_env/img/rock5.png",
    "/Users/z/Desktop/pygame_env/img/rock6.png"
]
rock_imgs = []
for path in rock_img_paths:
    rock_img = pygame.image.load(path).convert_alpha()
    rock_imgs.append(rock_img)

expl_anim = {'lg': [], 'sm': []}
expl_anim_paths = [
    "/Users/z/Desktop/pygame_env/img/player_expl0.png",
    "/Users/z/Desktop/pygame_env/img/player_expl1.png",
    "/Users/z/Desktop/pygame_env/img/player_expl2.png",
    "/Users/z/Desktop/pygame_env/img/player_expl3.png",
    "/Users/z/Desktop/pygame_env/img/player_expl4.png",
    "/Users/z/Desktop/pygame_env/img/player_expl5.png",
    "/Users/z/Desktop/pygame_env/img/player_expl6.png",
    "/Users/z/Desktop/pygame_env/img/player_expl7.png",
    "/Users/z/Desktop/pygame_env/img/player_expl8.png"
]
for path in expl_anim_paths:
    expl_img = pygame.image.load(path).convert_alpha()
    expl_img.set_colorkey(BLACK)
    expl_anim['lg'].append(pygame.transform.scale(expl_img, (75, 75)))
    expl_anim['sm'].append(pygame.transform.scale(expl_img, (30, 30)))

power_imgs = {}
prize1_img_path = "/Users/z/Desktop/pygame_env/img/prize1.png"
prize2_img_path = "/Users/z/Desktop/pygame_env/img/prize2.png"
power_imgs['prize1'] = pygame.image.load(prize1_img_path).convert()
power_imgs['prize2'] = pygame.image.load(prize2_img_path).convert()

# 声音
shoot_sound_path = "/Users/z/Desktop/pygame_env/music/shoot.wav"
shoot_sound = pygame.mixer.Sound(shoot_sound_path)
prize1_path = "/Users/z/Desktop/pygame_env/music/pow0.wav"
prize1_sound = pygame.mixer.Sound(prize1_path)
prize2_path = "/Users/z/Desktop/pygame_env/music/pow1.wav"
prize2_sound = pygame.mixer.Sound(prize2_path)
die_sound_path = "/Users/z/Desktop/pygame_env/music/rumble.ogg"
die_sound = pygame.mixer.Sound(die_sound_path)
expl_sounds = [
    pygame.mixer.Sound("/Users/z/Desktop/pygame_env/music/get_point.wav"),
    pygame.mixer.Sound("/Users/z/Desktop/pygame_env/music/get_point2.wav")
]
pygame.mixer.music.load("/Users/z/Desktop/pygame_env/music/background.mp3")
pygame.mixer.music.set_volume(0.1)

font_path = "/Users/z/Desktop/pygame_env/font.ttf"

def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_path, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.centerx = x
    text_rect.top = y
    surf.blit(text_surface, text_rect)

def new_rock():
    r = Rock()
    all_sprites.add(r)
    rocks.add(r)

def draw_health(surf, hp, x, y):
    if hp < 0:
        hp = 0
    BAR_LENGTH = 100
    BAR_HEIGHT = 10
    fill = (hp / 100) * BAR_LENGTH
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
    pygame.draw.rect(surf, GREEN, fill_rect)
    pygame.draw.rect(surf, WHITE, outline_rect, 2)

def draw_lives(surf, lives, img, x, y):
    for i in range(lives):
        img_rect = img.get_rect()
        img_rect.x = x + 30 * i
        img_rect.y = y
        surf.blit(img,img_rect)

def draw_init():
    screen.blit(background_img, (0,0))
    draw_text(screen, "Space World", 64, WIDTH/2, HEIGHT/4)
    draw_text(screen, "<- -> Move, Space shoooooot!", 22, WIDTH/2, HEIGHT/2)
    draw_text(screen, "Touch any key to start 開始", 18, WIDTH/2, HEIGHT * 3/4)
    pygame.display.update()
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                waiting = False

def draw_play_again(total_score):
    screen.blit(background_img, (0,0))
    draw_text(screen, "Game Over", 64, WIDTH/2, HEIGHT/4)
    draw_text(screen, f"Total Score: {total_score}", 36, WIDTH/2, HEIGHT/2 - 50)
    draw_text(screen, "Play again? (Y/N)", 22, WIDTH/2, HEIGHT/2 + 50)
    pygame.display.update()
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_y:
                    return True
                elif event.key == pygame.K_n:
                    return False

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = player_img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * 0.85 / 2)
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 10 
        self.speedx = 8
        self.health = 100
        self.lives = 3
        self.hidden = False
        self.hide_time = 0
        self.gun = 1
        self.gun_time = 0

    def update(self):
        now = pygame.time.get_ticks() 
        if self.gun > 1 and now - self.gun_time > 5000:
            self.gun -= 1
            self.gun_time = now

        if self.hidden and now - self.hide_time > 1000:
            self.hidden = False
            self.rect.centerx = WIDTH / 2
            self.rect.bottom = HEIGHT - 10 

        key_pressed = pygame.key.get_pressed()
        if key_pressed[pygame.K_RIGHT]:
            self.rect.x += self.speedx
        if key_pressed[pygame.K_LEFT]:
            self.rect.x -= self.speedx
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
            
    def shoot(self):
        if not(self.hidden):
            if self.gun == 1:
                bullet = Bullet(self.rect.centerx, self.rect.top)
                all_sprites.add(bullet)
                bullets.add(bullet)
                shoot_sound.play()
            elif self.gun >= 2:
                bullet1 = Bullet(self.rect.left,  self.rect.centery)
                bullet2 = Bullet(self.rect.right, self.rect.centery)
                all_sprites.add(bullet1)
                all_sprites.add(bullet2)
                bullets.add(bullet1)
                bullets.add(bullet2)
                shoot_sound.play()

    def hide(self):
        self.hidden = True
        self.hide_time = pygame.time.get_ticks()
        self.rect.center = (WIDTH/2, HEIGHT + 500)

    def gunup(self):
        self.gun += 1
        self.gun_time = pygame.time.get_ticks()

class Rock(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image_ori = random.choice(rock_imgs)
        self.image = self.image_ori.copy()
        self.rect = self.image.get_rect()
        self.radius = self.rect.width * 0.4
        self.rect.x = random.randrange(0, WIDTH - self.rect.width)
        self.rect.y = random.randrange(-180, -100)
        self.speedy = random.randrange(2, 10)
        self.speedx = random.randrange(-3, 3)
        self.total_degree = 0
        self.rot_degree = random.randrange(-3, 3)
        
    def rotate(self):
        self.total_degree += self.rot_degree
        self.total_degree = self.total_degree % 360
        self.image = pygame.transform.rotate(self.image_ori, self.total_degree)
        center = self.rect.center
        self.rect = self.image.get_rect()
        self.rect.center = center

    def update(self):
        self.rotate()
        self.rect.y += self.speedy
        self.rect.x += self.speedx        
        if self.rect.top > HEIGHT or self.rect.left > WIDTH or self.rect.left < 0:
            self.rect.x = random.randrange(0, WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(2, 10)
            self.speedx = random.randrange(-3, 3)
            
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = bullet_img
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speedy = -20

    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()

class Explosion(pygame.sprite.Sprite):
    def __init__(self, center, size):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        if self.size == "player":
            self.image = pygame.Surface((1, 1))  # to avoid error, create a blank image
        else:
            self.image = expl_anim[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 50

    def update(self):
        if self.size != "player":  
            now = pygame.time.get_ticks()
            if now - self.last_update > self.frame_rate:
                self.last_update = now
                self.frame += 1
                if self.frame == len(expl_anim[self.size]):
                    self.kill()
                else:
                    self.image = expl_anim[self.size][self.frame]
                    center = self.rect.center
                    self.rect = self.image.get_rect()
                    self.rect.center = center

class Power(pygame.sprite.Sprite):
    def __init__(self, center):
        pygame.sprite.Sprite.__init__(self)
        self.type = random.choice(["prize1", "prize2"])
        self.image = power_imgs[self.type]
        self.image.set_colorkey(BLACK)
        self.image = pygame.transform.scale(self.image, (self.image.get_width() // 5, self.image.get_height() // 5))
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.speedy = 3

    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT:
            self.kill()

# all_sprites = pygame.sprite.Group()
# rocks = pygame.sprite.Group()
# bullets = pygame.sprite.Group()
# powers = pygame.sprite.Group()
# player = Player()
pygame.mixer.music.play(-1)

# game loop main
show_init = True
running = True
while running:
    if show_init:
        draw_init()
        show_init = False
        all_sprites = pygame.sprite.Group()
        rocks = pygame.sprite.Group()
        bullets = pygame.sprite.Group()
        powers = pygame.sprite.Group()
        player = Player()

        all_sprites.add(player)
        for i in range(8):
            new_rock()
        score = 0

    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()

    all_sprites.update()
    

    # check bullets hit rocks or not
    hits = pygame.sprite.groupcollide(rocks, bullets, True, True, pygame.sprite.collide_circle)
    for rock_hit, bullet_hit_list in hits.items():
        for bullet in bullet_hit_list:
            score += int(rock_hit.radius)
        
        explosion = Explosion(rock_hit.rect.center, 'lg')
        all_sprites.add(explosion)
        random.choice(expl_sounds).play()
        if random.random() > 0.9:
            pow = Power(rock_hit.rect.center)
            all_sprites.add(pow)
            powers.add(pow)
        new_rock()

    # check player hit by rocks or not
    hits = pygame.sprite.spritecollide(player, rocks, True, pygame.sprite.collide_circle)
    for hit in hits:
        new_rock()
        player.health -= hit.radius 
        expl = Explosion(hit.rect.center, "sm")
        all_sprites.add(expl)
        if player.health <= 0:
            death_expl = Explosion(player.rect.center, "player")
            die_sound.play()
            all_sprites.add(death_expl)
            die_sound.play()
            player.lives -= 1
            player.health = 100
            player.hide()

    hits = pygame.sprite.spritecollide(player, powers, True)  # True!!
    for hit in hits:
        if hit.type == "prize1":
            player.health += 20
            if player.health > 100:
                player.health = 100
            prize1_sound.play()
        elif hit.type == "prize2":
            player.gunup()
            prize2_sound.play()

    # if player game over, ask play again or not
    if player.lives == 0:
        if not draw_play_again(score):
            running = False
        else:
            show_init = True
       

    screen.fill(BLACK)
    screen.blit(background_img, (0, 0))
    all_sprites.draw(screen)
    draw_text(screen, str(score), 18, WIDTH / 2, 10)
    draw_health(screen, player.health, 5, 15)
    draw_lives(screen, player.lives, player_mini_img, WIDTH - 100, 15)
    pygame.display.flip()

pygame.quit()