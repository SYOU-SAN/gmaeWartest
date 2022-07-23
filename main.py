from cv2 import exp
from importlib_metadata import SelectableGroups
from matplotlib.pyplot import draw
import pygame
import random
import os

FPS = 60
WIDTH = 500
HIGHT = 600

WHITE = (255, 255, 255)
YELLOW = (255, 255, 1)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)

#creat game window
pygame.init() #pygame 初始化
pygame.mixer.init() #音效初始化
screen = pygame.display.set_mode((WIDTH, HIGHT))
clock = pygame.time.Clock()

#loading image()
background_img = pygame.image.load(os.path.join("img", "background.png")).convert()
player_img = pygame.image.load(os.path.join("img", "player.png")).convert()
player_mini_img = pygame.transform.scale(player_img, (35, 35))
player_mini_img.set_colorkey(WHITE)
#pygame.display.set_icon(pygame.image.load(os.path.join("img", "rocks1.png")).convert())
#rocks_img = pygame.image.load(os.path.join("img", "rocks.png")).convert()
bullets_img = pygame.image.load(os.path.join("img", "bullets.png")).convert()
rocks_img = []
for i in range(7):
    rocks_img.append(pygame.image.load(os.path.join("img", f"rocks{i}.png")).convert())

expl_anim = {}
expl_anim['large'] = []
expl_anim['small'] = []
expl_anim['player'] = []

for i in range(9):
    expl_img = pygame.image.load(os.path.join("img", f"expl{i}.png")).convert()
    expl_img.set_colorkey(BLACK)
    expl_anim["large"].append(pygame.transform.scale(expl_img, (75, 75)))
    expl_anim["small"].append(pygame.transform.scale(expl_img, (30, 30)))
    player_expl_img = pygame.image.load(os.path.join("img", f"player_expl{i}.png")).convert()
    player_expl_img.set_colorkey(BLACK)
    expl_anim["player"].append(pygame.transform.scale(expl_img, (75, 75)))

power_imgs= {}
power_imgs['shield'] = pygame.image.load(os.path.join("img", "shield.png")).convert()
power_imgs['gun'] = pygame.image.load(os.path.join("img", "gun.png")).convert()

#loanding music
shoot_sound = pygame.mixer.Sound(os.path.join("soundtrack", "shoot2.mp3"))
gun_sound = pygame.mixer.Sound(os.path.join("soundtrack", "coin01.mp3"))
shiel_sound = pygame.mixer.Sound(os.path.join("soundtrack", "coin02.mp3"))
die_sound = pygame.mixer.Sound(os.path.join("soundtrack", "playlaughing.mp3"))
expl_sound = [
        pygame.mixer.Sound(os.path.join("soundtrack", "explosion1.mp3")),
        pygame.mixer.Sound(os.path.join("soundtrack", "explosion2.mp3"))
    ]
pygame.mixer.music.load(os.path.join("soundtrack", "background.mp3"))
pygame.mixer.music.set_volume(0.5)

font_name = pygame.font.match_font('arial')
def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size) #文字物件(字體, 大小)
    text_surface = font.render(text, True, BLUE)
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
    BAR_HIGHT = 13
    fill = (hp/100) * BAR_LENGTH
    outline_reat = pygame.Rect(x, y, BAR_LENGTH, BAR_HIGHT)
    fill_rect = pygame.Rect(x, y, fill,BAR_HIGHT)
    pygame.draw.rect(surf, RED, fill_rect)
    pygame.draw.rect(surf, BLACK, outline_reat, 2)

def draw_lives(surf, lives, img, x, y):
    for i in range(lives):
        img_rect = img.get_rect()
        img_rect.x = x + 30* i
        img_rect.y = y
        surf.blit(img, img_rect)

def draw_init():
    screen.blit(background_img, (0, 0))
    draw_text(screen, 'DESERT WARRIOR', 55, WIDTH/2, HIGHT/4)
    draw_text(screen, '<--  -->MOVE AIRPLANE, SAPCE FOR SHOOTING', 19, WIDTH/2, HIGHT/2)
    draw_text(screen, 'PRESS ANY KEY TO START', 15, WIDTH/2, HIGHT* 3/4)
    pygame.display.update()
    watting = True
    while watting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return True
            elif event.type == pygame.KEYUP:
                watting = False
                return False

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(player_img, (95, 95))
        self.image.set_colorkey(WHITE)
        #self.image.fill(YELLOW)
        self.rect = self.image.get_rect() #定位
        self.radius = 25
        #pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.centerx = WIDTH/2 
        self.rect.bottom = HIGHT - 10
        self.speedx = 8
        self.health = 100
        self.live = 3
        self.hidden = False
        self.hide_time = 0
        self.gun = 1
        self.gun_time = 0

    def update(self) :
        now = pygame.time.get_ticks()
        if self.gun > 1 and now - self.gun_time > 5000:
            self.gun -= 1
            self.gun_time = now

        if self.hidden and now - self.hide_time > 1000:
            self.hidden = False
            self.rect.centerx = WIDTH / 2
            self.rect.bottom = HIGHT - 10

        key_pressed = pygame.key.get_pressed() #方向控制
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
                bullet1 = Bullet(self.rect.left, self.rect.centery)
                bullet2 = Bullet(self.rect.right, self.rect.centery)
                all_sprites.add(bullet1)
                all_sprites.add(bullet2)
                bullets.add(bullet1)
                bullets.add(bullet2)
                shoot_sound.play()

    def hide(self):
        self.hidden = True
        self.hide_time = pygame.time.get_ticks()
        self.rect.center = (WIDTH/2, HIGHT+500)

    def gunup(self):
        self.gun += 1
        self.gun_time = pygame.time.get_ticks()
        
class Rock(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image_ori = random.choice(rocks_img)
        self.image_ori.set_colorkey(WHITE)
        self.image = self.image_ori.copy()
        #self.image.fill(RED)
        self.rect = self.image.get_rect() #定位
        self.radius =int(self.rect.width * 0.9 / 2)
        # pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.x = random.randrange(0, WIDTH - self.rect.width)
        self.rect.y = random.randrange(-180, -100)
        self.speedy = random.randrange(2, 10)        
        self.speedx = random.randrange(-3, 3 )
        self.total_degree = 0
        self.rot_degree = random.randrange(-3, 3)

    def rotate(self):
        self.total_degree += self.rot_degree
        self.total_degree = self.total_degree % 180
        self.image = pygame.transform.rotate(self.image_ori, self.total_degree)
        center = self.rect.center #轉動後重新定位
        self.rect = self.image.get_rect()
        self.rect.center = center

    def update(self):
        self.rotate()
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        if self.rect.top > HIGHT or self.rect.left > WIDTH or self.rect.right < 0:
            self.rect.x = random.randrange(0, WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(2, 10)        
            self.speedx = random.randrange(-2, 2)

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(bullets_img, (45, 45))
        self.image.set_colorkey(WHITE)
        #self.image.fill(BLUE)
        self.rect = self.image.get_rect() #定位
        self.rect.centerx = x
        self.rect.bottom = y
        self.speedy = -10

    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()

class Explosion(pygame.sprite.Sprite):
    def __init__(self, center, size):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.image = expl_anim[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 50

    def update(self):
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
        self.type = random.choice(['shield', 'gun'])
        self.image = power_imgs[self.type]
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.speedy = 3

    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom > HIGHT:
            self.kill()
        
           

pygame.mixer.music.play(-1)

#game loop
show_init = True
running = True
while running:
    if show_init:
        close = draw_init()
        if close:
            break
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
    #get enter things
    for event in pygame.event.get():
        if event.type  == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()
    
    #game update
    all_sprites.update()

    #子彈與石頭
    attacks = pygame.sprite.groupcollide(rocks, bullets, True, True)
    for attack in attacks:
        random.choice(expl_sound).play()
        score += attack.radius
        expl = Explosion(attack.rect.center, 'large')
        all_sprites.add(expl)        
        if random.random() >0.98:
            pow = Power(attack.rect.center)
            all_sprites.add(pow)
            powers.add(pow)
        new_rock()

    #石頭與飛船
    hits = pygame.sprite.spritecollide(player, rocks, True, pygame.sprite.collide_circle) #矩形碰撞改成圓形"collode_ccircle"
    for hit in  hits:
        new_rock()
        player.health -= hit.radius
        expl = Explosion(hit.rect.center, 'small')
        all_sprites.add(expl)
        if player.health <= 0:
            game_over = Explosion(player.rect.center, 'player')
            all_sprites.add(game_over)
            die_sound.play()
            player.live -= 1
            player.health = 100
            player.hide()

    #寶物與飛船
    hits = pygame.sprite.spritecollide(player, powers, True)
    for hit in hits:
        if hit.type == 'shield':
            player.health += 20
            if player.health >100:
                player.health = 100
            shiel_sound.play()     
        elif hit.type == 'gun':
            player.gunup()
            gun_sound.play()
            
    if player.live == 0 and not(game_over.alive()):
        show_init = True

    
    #game display
    screen.fill((WHITE))
    screen.blit(background_img, (0, 0))
    all_sprites.draw(screen)
    pygame.display.set_caption("DESERT WARRIOR")
    draw_text(screen, str(score), 20, WIDTH / 2, 10)
    draw_health(screen, player.health, 5, 15)
    draw_lives(screen, player.live, player_mini_img, WIDTH - 100, 15)
    pygame.display.update()

    
pygame.quit()