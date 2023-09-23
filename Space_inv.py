import pygame
import sys
import os
from random import randint, choice
pygame.init()
pygame.display.set_caption('Space invaders')
enemy = ['enemy_ship1.png', 'enemy_ship2.png', 'enemy_ship3.png', 'enemy_ship1.png', 'enemy_ship2.png',
         'enemy_ship1.png']
enemy5_10 = ['enemy_ship1.png', 'enemy_ship1.png', 'enemy_ship2.png', 'enemy_ship2.png', 'enemy_ship3.png']
enemy10_15 = ['enemy_ship1.png', 'enemy_ship2.png', 'enemy_ship3.png', 'enemy_ship3.png']
enemy15 = ['enemy_ship3.png']
explosion = ['image_part_001.png', 'image_part_002.png', 'image_part_003.png', 'image_part_004.png',
             'image_part_005.png',
             'image_part_006.png', 'image_part_007.png', 'image_part_008.png', 'image_part_009.png',
             'image_part_010.png',
             'image_part_011.png', 'image_part_012.png', 'image_part_013.png', 'image_part_014.png']
boss_attacks = ['attack1', 'attack2']
boss_attacks2 = ['attack1', 'attack2', 'attack3', 'attack4']
# некоторые основные переменные
timer = 2000
wave = 19
player_hp = 700
max_hp = 700
score = 20000
lives = 10
enemy_count = 5

pause, boss_fight, boss_po, game_over = False, False, False, False
pygame.time.set_timer(pygame.USEREVENT, timer)


class Enemy(pygame.sprite.Sprite):  # появление врагов
    def __init__(self, x, filename, group):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join("data", filename)).convert_alpha()
        if filename == 'enemy_ship1.png':
            self.hp = 75 + 25 * wave
            self.score = 50
        elif filename == 'enemy_ship2.png':
            self.hp = 125 + 30 * wave
            self.score = 75
        elif filename == 'enemy_ship3.png':
            self.hp = 175 + 35 * wave
            self.score = 100
        self.counter_shot = 50
        self.shot_speed = 1
        self.image = pygame.transform.scale(self.image, (100, 100))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = -100
        self.speed_enemy = 2
        self.add(group)
        self.name = filename

    def update(self):
        death = pygame.mixer.Sound('sound/explosion.wav')
        death.set_volume(0.2)
        self.counter_shot -= self.shot_speed
        global player_hp, score, lives, enemy_count, timer, wave
        if self.rect.y + self.speed_enemy < 700:
            self.rect.y += self.speed_enemy
        else:
            self.kill()
            lives -= 1
            if wave == 10 or wave == 20:
                enemy_count -= 1
        for i in range(len(shoots)):
            i1 = int(str(i))
            i = shoots[i1]
            if i == '.':
                continue
            x, y, speed = i.get_x(), i.get_y(), i.get_speed()
            if self.rect.x < x < self.rect.x + 100 and self.rect.y < y < self.rect.y + 100 and speed < 0:  #уменьшение хп врага
                self.hp -= damage
                hit = pygame.mixer.Sound('sound\expl6.wav')
                hit.set_volume(0.2)
                hit.play()
                expl = Explosion((self.rect.x + 50, self.rect.y + 50), 'small')
                explosions.append(expl)
                all_sprites.add(expl)
                if self.hp <= 0:
                    expl = Explosion((self.rect.x + 50, self.rect.y + 50), 'lg')
                    explosions.append(expl)
                    all_sprites.add(expl)
                    score += self.score
                    enemy_count -= 1
                    self.kill()
                    death.play()
                shoots[i1].delet()
                shoots[i1] = '.'
        if self.rect.x < player_x + 50 < self.rect.x + 100 and self.rect.y < player_y + 50 < self.rect.y + 100:  #таран
            player_hp -= 50
            enemy_count -= 1
            score += self.score
            expl = Explosion((self.rect.x + 50, self.rect.y + 50), 'lg')
            explosions.append(expl)
            all_sprites.add(expl)
            self.kill()
            death.play()
        if player_x - 50 <= self.rect.x <= player_x + 100 and self.counter_shot < 0:  #вражеский выстрел
            self.counter_shot = 100
            if self.name == 'enemy_ship1.png':
                shoots.append(Shoot(self.rect.x, self.rect.y, 10))
            elif self.name == 'enemy_ship2.png':
                shoots.append(Shoot(self.rect.x - 10, self.rect.y, 10))
                shoots.append(Shoot(self.rect.x + 10, self.rect.y, 10))
            elif self.name == 'enemy_ship3.png':
                shoots.append(Shoot(self.rect.x, self.rect.y, 10))
                shoots.append(Shoot(self.rect.x - 20, self.rect.y - 15, 10))
                shoots.append(Shoot(self.rect.x + 20, self.rect.y - 15, 10))
            hit = pygame.mixer.Sound('sound/pew.wav')
            hit.set_volume(0.2)
            hit.play()


class Explosion(pygame.sprite.Sprite):  # появление взрыва при убийстве врагов или попадании
    def __init__(self, center, size):
        pygame.sprite.Sprite.__init__(self)
        self.frame = 0
        self.image = pygame.image.load(os.path.join("data", explosion[self.frame])).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.size = size
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 50

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.size == 'small':
                self.frame += 1
            if self.frame == len(explosion) - 1:
                self.kill()
            else:
                center = self.rect.center
                if self.frame >= 14:
                    self.kill()
                else:
                    size_ex = 200
                    if self.size == 'small':
                        size_ex = 40
                    elif self.size == 'v_lg':
                        size_ex = 300
                    self.image = pygame.image.load(os.path.join("data", explosion[self.frame])).convert_alpha()
                    self.image = pygame.transform.scale(self.image, (size_ex, size_ex))
                    self.rect = self.image.get_rect()
                    self.rect.center = center


class Shoot:  # появление снаряда при выстреле
    def __init__(self, x, y, speed):
        self.speed = speed
        self.sprite = pygame.sprite.Sprite()
        if self.speed < 0:
            self.sprite.image = load_image("shot_1.png")
        else:
            self.sprite.image = load_image("shot_2.png")
        self.sprite.rect = self.sprite.image.get_rect()
        all_sprites.add(self.sprite)
        self.sprite.rect.x = x + 45
        self.sprite.rect.y = y - 10

    def move(self):
        self.sprite.rect.y += self.speed
        if self.sprite.rect.y + self.speed < -20:
            all_sprites.remove(self.sprite)
        if self.sprite.rect.y + self.speed > 800:
            all_sprites.remove(self.sprite)

    def delet(self):  # удаление одной
        all_sprites.remove(self.sprite)

    def get_y(self):
        return int(self.sprite.rect.y)

    def get_x(self):
        return int(self.sprite.rect.x)

    def get_speed(self):
        return self.speed


class Boss(pygame.sprite.Sprite):  # появление босса
    def __init__(self, filename, group):
        global boss_now
        pygame.sprite.Sprite.__init__(self)
        self.add(group)
        self.image = pygame.image.load(os.path.join("data", filename)).convert_alpha()
        self.image = pygame.transform.scale(self.image, (300, 300))
        self.rect = self.image.get_rect()
        self.rect.x = 400
        self.rect.y = 0
        if filename == 'boss1.png':
            boss_now = 'boss1.png'
            self.hp = 100000
            self.speed = 3
        else:
            boss_now = 'boss2.png'
            self.hp = 1000000
            self.speed = 5
        self.left = True
        self.score = 2000

    def update(self):
        global damage, score, enemy_count, boss_po, timer, win_game
        death = pygame.mixer.Sound('sound/explosion.wav')
        death.set_volume(0.2)
        if self.rect.x - self.speed > 0 and self.left:
            self.rect.x -= self.speed
        else:
            self.left = False
        if self.rect.x + self.speed < 680 and not self.left:
            self.rect.x += self.speed
        else:
            self.left = True
        for i in range(len(shoots)):
            if shoots[i] == '.':
                continue
            speed = shoots[i].get_speed()
            if speed > 0:
                continue
            i1 = int(str(i))
            i = shoots[i1]
            x, y = i.get_x(), i.get_y()
            if self.rect.x < x < self.rect.x + 300 and self.rect.y < y < self.rect.y + 300 and speed < 0:
                self.hp -= damage
                hit = pygame.mixer.Sound('sound\expl6.wav')
                hit.set_volume(0.2)
                hit.play()
                expl = Explosion((self.rect.x + 150, self.rect.y + 150), 'small')
                explosions.append(expl)
                all_sprites.add(expl)
                if self.hp <= 0:
                    expl = Explosion((self.rect.x + 50, self.rect.y + 50), 'v_lg')
                    explosions.append(expl)
                    all_sprites.add(expl)
                    score += self.score
                    enemy_count -= 1
                    boss_po = False
                    timer = 2000
                    pygame.time.set_timer(pygame.USEREVENT, timer)
                    self.kill()
                    death.play()
                    boss_now = ''
                    if wave == 20:
                        win_game = True
                shoots[i1].delet()
                shoots[i1] = '.'


def createship(group):  # вызов класса появления врагов
    if wave < 5:
        name = choice(enemy)
    elif 5 <= wave <= 10:
        name = choice(enemy5_10)
    elif 10 < wave <= 15:
        name = choice(enemy10_15)
    else:
        name = choice(enemy15)
    x = randint(100, 800)
    return Enemy(x, name, group)


def load_image(name, colorkey=None):  # загрузка картинок
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


def ship_upgrade():  # улучшение корабля
    global ship_lvl, speed, defence, sprite
    if ship_lvl == 1:
        sprite.image = load_image("spaceship_3.png")
        defence = 10
        speed += 2
    elif ship_lvl == 2:
        sprite.image = load_image("spaceship_2.png")
        defence = 20
        speed += 1
    sprite.image = pygame.transform.scale(sprite.image, (100, 100))
    ship_lvl += 1


def bul_remove():  # удаление ненужных снарядов
    for i in range(len(shoots)):
        r = shoots[i]
        if r == '.':
            continue
        r.move()
        if r.get_y() < -20:
            shoots[i] = '.'
        if r.get_y() > 800:
            shoots[i] = '.'
    while '.' in shoots:
        shoots.remove('.')


def boss(group):  # вызов класса появления босса
    global boss_po, timer
    if wave == 10:
        name = 'boss1.png'
    if wave == 20:
        timer = 1500
        name = 'boss2.png'
    boss_po = True
    return Boss(name, group)


def blit_str():
    text = font.render("Score: {}".format(score), True, (255, 0, 0))
    text1 = font.render("Wave: {}".format(wave), True, (255, 0, 0))
    text2 = font.render("Health: {}".format(player_hp), True, (255, 0, 0))
    text3 = font.render("Lives: {}".format(lives), True, (255, 0, 0))
    text4 = font.render("Enemy: {}".format(enemy_count), True, (255, 0, 0))
    screen.blit(text, (text_x, text_y))
    screen.blit(text1, (text1_x, text1_y))
    screen.blit(text2, (text2_x, text2_y))
    screen.blit(text3, (text3_x, text3_y))
    screen.blit(text4, (text4_x, text4_y))


# другие основные перемнные
image = load_image("background.png")
global explosions, all_sprites
all_sprites = pygame.sprite.Group()
sprite = pygame.sprite.Sprite()
sprite.image = load_image("spaceship_1.png")
sprite.image = pygame.transform.scale(sprite.image, (100, 100))
sprite.rect = sprite.image.get_rect()
all_sprites.add(sprite)
explosions = []
sprite.rect.x, sprite.rect.y = 5, 550
image = pygame.transform.scale(image, (1000, 700))
screen = pygame.display.set_mode((1300, 700))

enemy_gr = pygame.sprite.Group()
createship(enemy_gr)

boss_gr = pygame.sprite.Group()

font = pygame.font.Font(None, 60)
font1 = pygame.font.Font(None, 200)
font2 = pygame.font.Font(None, 25)
text1_x = text2_x = text3_x = text4_x = text_x = 1040
text_y, text1_y, text2_y, text3_y, text4_y = 40, 100, 160, 220, 280

text_upgrade_x, text_upgrade_dam_x, text_upgrade_hp_x, text_upgrade_fire_x = 70, 300, 530, 760
text_upgrade_dam_y = text_upgrade_hp_y = text_upgrade_fire_y = text_upgrade_y = 170

text_game_over = font1.render("{}".format('Game Over'), True, (255, 255, 255))
text_game_over_x, text_win_game_x = 250, 300
text_game_over_y = text_win_game_y = 300

text_win_game = font1.render('{}'.format('You win'), True, (255, 255, 255))

text_full_hp_x, text_lives_x = 760, 70
text_full_hp_y = text_lives_y = 270

global shoots
shoots = []
pause_picture = 0
screen.blit(image, (0, 0))
clock = pygame.time.Clock()
fps, speed, cost, fix = 60, 10, 2000, -50
boss_now = ''
global damage, damage_enemy, ship_lvl
ship_lvl = 1
damage, defence, damage_enemy, shot_speed = 70, 0, 10, 5
attack1_count = attack2_count = attack3_count = attack4_count = attack5_count = 0
counter_shot = 100
running = True
win_game = False

pygame.mixer.music.load('sound/fon.mp3')
pygame.mixer.music.set_volume(0.4)
pygame.mixer.music.play(-1)

while running:
    clock.tick(fps)
    if win_game or game_over:  # проверка, пройден ли последний босс
        screen.fill((0, 0, 0))
        if win_game:
            screen.blit(text_win_game, (text_win_game_x, text_win_game_y))
        elif game_over:
            screen.blit(text_game_over, (text_game_over_x, text_game_over_y))
        pygame.mixer.music.stop()
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        continue
    if boss_fight and enemy_count <= 0 and len(boss_gr) != 0:
        enemy_count = 1
    if enemy_count <= 0:  # переход на следующую волну
        wave += 1
        enemy_count = 3 * wave
        damage_enemy = damage_enemy + (5 * wave)
        if wave > 20:
            win_game = True
        if wave == 10 or wave == 20:
            boss_fight = True
            timer = 750
            enemy_count = 1 + len(enemy_gr)
            if player_y < 300:
                sprite.rect.y = 550
        elif wave < 10 or wave > 10:
            boss_fight = False

    counter_shot -= shot_speed
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.USEREVENT and not pause and not boss_fight:
            for i in range(wave // 6 + 1):
                createship(enemy_gr)
        if event.type == pygame.USEREVENT and not pause and boss_fight:
            if boss_now == 'boss1.png':  # атаки босса
                at = choice(boss_attacks)
                if at == 'attack1':
                    for i in range(20):
                        shot = Shoot(randint(-50, 900), 250, 5)
                        shoots.append(shot)
                elif at == 'attack2':
                    a = randint(15, 51)
                    for i in range(63):
                        if a - 10 < i < a + 10:
                            continue
                        else:
                            shot = Shoot(i * 15, 250, 5)
                            shoots.append(shot)
                y = randint(1, 3)
                if y == 1:
                    y1 = randint(1, 3)
                    if y1 == 1:
                        for i in range(11):
                            shot = Shoot(randint(-50, 300), 250, 2)
                            shoots.append(shot)
                            shot = Shoot(randint(600, 900), 250, 2)
                            shoots.append(shot)
                    if y1 == 2:
                        for i in range(11):
                            shot = Shoot(randint(100, 500), 250, 2)
                            shoots.append(shot)
                            shot = Shoot(randint(400, 700), 250, 2)
                            shoots.append(shot)
                    if y1 == 3:
                        for i in range(25):
                            shot = Shoot(randint(300, 600), 250, 2)
                            shoots.append(shot)

            else:
                at = choice(boss_attacks2)
                if (
                        at == 'attack1' or attack1_count != 0) and attack2_count == 0 and attack3_count == 0 and attack4_count == 0 and attack5_count == 0:
                    if attack1_count == 0:
                        pygame.time.set_timer(pygame.USEREVENT, 600)
                        attack1_count = 10
                        prok = randint(20, 44)
                    attack1_count -= 1
                    if randint(0, 1):
                        change = randint(-4, -2)
                    else:
                        change = randint(2, 4)
                    prok += change
                    if prok > 44:
                        prok = 45
                    elif prok < 7:
                        prok = 7
                    for i in range(50):
                        if prok - 5 <= i <= prok + 5:
                            continue
                        shot = Shoot(fix + i * 20, 250, 3)
                        shoots.append(shot)
                    if attack1_count == 0:
                        pygame.time.set_timer(pygame.USEREVENT, timer)
                elif (
                        at == 'attack2' or attack2_count != 0) and attack3_count == 0 and attack4_count == 0 and attack5_count == 0:
                    if attack2_count == 0:
                        pygame.time.set_timer(pygame.USEREVENT, 75)
                        attack2_count = 40
                    attack2_count -= 1
                    for i in range(3):
                        shot = Shoot(fix + (40 - attack2_count) * 10, 250 + 50 * i, 4)
                        shoots.append(shot)
                        shot = Shoot(fix + 1000 - (40 - attack2_count) * 10, 250 + 50 * i, 4)
                        shoots.append(shot)
                    if attack2_count == 0:
                        pygame.time.set_timer(pygame.USEREVENT, timer)
                elif (at == 'attack3' or attack3_count != 0) and attack4_count == 0 and attack5_count == 0:
                    if attack3_count == 0:
                        pygame.time.set_timer(pygame.USEREVENT, 300)
                        attack3_count = 5
                    attack3_count -= 1
                    for i in range(5):
                        rnd = randint(0, 990)
                        shot = Shoot(rnd, 250, 4)
                        shoots.append(shot)
                        shot = Shoot(rnd + 10, 250 - 25, 4)
                        shoots.append(shot)
                        shot = Shoot(rnd - 10, 250 - 25, 4)
                        shoots.append(shot)
                    if attack3_count == 0:
                        pygame.time.set_timer(pygame.USEREVENT, timer)
                elif (at == 'attack4' or attack4_count != 0) and attack5_count == 0:
                    if attack4_count == 0:
                        pygame.time.set_timer(pygame.USEREVENT, 75)
                        attack4_count = 40
                    attack4_count -= 1
                    for i in range(3):
                        shot = Shoot(fix + (89 - attack4_count) * 10, 100 + 50 * i, 4)
                        shoots.append(shot)
                        shot = Shoot(fix + 1000 - (89 - attack4_count) * 10, 100 + 50 * i, 4)
                        shoots.append(shot)
                    if attack4_count == 0:
                        pygame.time.set_timer(pygame.USEREVENT, timer)
        if pause:  # проверка, пауза ли сейчас
            screen.fill((0, 0, 0))
            screen.blit(image, (0, 0))
            pygame.draw.line(screen, (255, 255, 255), (1000, 0), (1000, 700), 10)

            if pause_picture == 0:
                sprite_pause = pygame.sprite.Sprite()
                sprite_pause.image = load_image("pause.jpg")
                sprite_pause.image = pygame.transform.scale(sprite_pause.image, (1000, 700))
                sprite_pause.rect = sprite_pause.image.get_rect()
                all_sprites.add(sprite_pause)
            pause_picture = 1
            all_sprites.draw(screen)
            button = pygame.draw.rect(screen, (255, 255, 255), (60, 150, 200, 50), width=3)
            button = pygame.draw.rect(screen, (255, 255, 255), (290, 150, 200, 50), width=3)
            button = pygame.draw.rect(screen, (255, 255, 255), (520, 150, 200, 50), width=3)
            button = pygame.draw.rect(screen, (255, 255, 255), (750, 150, 200, 50), width=3)
            button = pygame.draw.rect(screen, (255, 255, 255), (60, 250, 200, 50), width=3)
            button = pygame.draw.rect(screen, (255, 255, 255), (750, 250, 200, 50), width=3)
            text_upgrade = font2.render('{}'.format('Ship upgrade' + '   ' + str(cost)), True, (255, 255, 255))
            text_upgrade_dam = font2.render('{}'.format('Damage upgrade' + '   ' + '350'), True, (255, 255, 255))
            text_upgrade_hp = font2.render('{}'.format('Hp upgrade' + '   ' + '200'), True, (255, 255, 255))
            text_upgrade_fire = font2.render('{}'.format('Firerate upgrade' + '   ' + '700'), True, (255, 255, 255))
            text_lives = font2.render('{}'.format('Lives' + '   ' + '250'), True, (255, 255, 255))
            text_full_hp = font2.render('{}'.format('Full hp' + '   ' + '550'), True, (255, 255, 255))
            screen.blit(text_upgrade, (text_upgrade_x, text_upgrade_y))
            screen.blit(text_upgrade_dam, (text_upgrade_dam_x, text_upgrade_dam_y))
            screen.blit(text_upgrade_hp, (text_upgrade_hp_x, text_upgrade_hp_y))
            screen.blit(text_upgrade_fire, (text_upgrade_fire_x, text_upgrade_fire_y))
            screen.blit(text_lives, (text_lives_x, text_lives_y))
            screen.blit(text_full_hp, (text_full_hp_x, text_full_hp_y))
            blit_str()
            if event.type == pygame.MOUSEBUTTONUP:  # покупка
                position = event.pos
                pos_x, pos_y = position[0], position[1]
                if 150 <= pos_y <= 200:
                    if 60 <= pos_x <= 260:
                        if ship_lvl == 1 and score >= cost:
                            score -= cost
                            ship_upgrade()
                            cost = 6000
                        elif ship_lvl == 2 and score >= cost:
                            score -= cost
                            ship_upgrade()
                    elif 290 <= pos_x <= 490 and not boss_fight:
                        if score >= 350:
                            score -= 350
                            damage += 10
                    elif 520 <= pos_x <= 720 and not boss_fight:
                        if score >= 200:
                            score -= 200
                            player_hp += 50
                            max_hp += 50
                    elif 750 <= pos_x <= 950 and not boss_fight:
                        if score >= 700:
                            score -= 700
                            shot_speed += 1
                elif 250 <= pos_y <= 300 and not boss_fight:
                    if 60 <= pos_x <= 260:
                        if score >= 250:
                            score -= 250
                            lives += 1
                    elif 750 <= pos_x <= 950 and not boss_fight:
                        if score >= 550:
                            score -= 50
                            player_hp = max_hp
            pygame.display.flip()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                if not pause:
                    pause = True
                else:
                    pause = False
                    pause_picture = 0
                    all_sprites.remove(sprite_pause)
    if pause:
        continue
    keys = pygame.key.get_pressed()  # движение корабля
    if keys[pygame.K_LEFT]:
        if sprite.rect.x - speed > 0:
            sprite.rect.x -= speed
    if keys[pygame.K_RIGHT]:
        if sprite.rect.x + speed < 900:
            sprite.rect.x += speed
    if keys[pygame.K_UP]:
        if boss_po:
            if sprite.rect.y - speed > 300:
                sprite.rect.y -= speed
        else:
            if sprite.rect.y - speed > 0:
                sprite.rect.y -= speed
    if keys[pygame.K_DOWN]:
        if sprite.rect.y + speed < 610:
            sprite.rect.y += speed
    if keys[pygame.K_w]: #выстрел
        if counter_shot < 0:
            if ship_lvl == 1:
                shoots.append(Shoot(sprite.rect.x, sprite.rect.y, -10))
            elif ship_lvl == 2:
                shoots.append(Shoot(sprite.rect.x - 10, sprite.rect.y, -10))
                shoots.append(Shoot(sprite.rect.x + 10, sprite.rect.y, -10))
            else:
                shoots.append(Shoot(sprite.rect.x, sprite.rect.y, -10))
                shoots.append(Shoot(sprite.rect.x - 20, sprite.rect.y + 15, -10))
                shoots.append(Shoot(sprite.rect.x + 20, sprite.rect.y + 15, -10))
            hit = pygame.mixer.Sound('sound/pew.wav')
            hit.set_volume(0.2)
            hit.play()
            counter_shot = 100
    if player_hp <= 0 or lives <= 0:#игрок умер или кончились жизни
        game_over = True
        continue
    if boss_fight: #идет ли бой с боссом
        if not boss_po:
            boss(boss_gr)
        boss_gr.update()
    bul_remove() #удаление ненужных снарядов
    player_x, player_y = sprite.rect.x, sprite.rect.y
    screen.fill((0, 0, 0))
    screen.blit(image, (0, 0))
    pygame.draw.line(screen, (255, 255, 255), (1000, 0), (1000, 700), 10)
    blit_str()
    for i in explosions:  # эффект взрыва
        i.update()
    for i in range(len(shoots)):
        i1 = int(str(i))
        i = shoots[i1]
        x, y, fly_speed = i.get_x(), i.get_y(), i.get_speed()
        if sprite.rect.x < x < sprite.rect.x + 100 and sprite.rect.y < y < sprite.rect.y + 100 and fly_speed > 0:
            player_hp -= int((damage_enemy - defence) * (100 - defence) / 100)
            expl = Explosion((sprite.rect.x + 50, sprite.rect.y + 50), 'small')
            explosions.append(expl)
            all_sprites.add(expl)
            shoots[i1].delet()
            shoots[i1] = '.'

    enemy_gr.draw(screen)
    boss_gr.draw(screen)
    all_sprites.draw(screen)
    enemy_gr.update()
    pygame.display.flip()

pygame.quit()
