from random import *
from pygame import *

font.init()
font1 = font.Font(None, 36)
font2 = font.Font(None, 70)
mixer.init()
menu_channel = mixer.Channel(0)
game_channel = mixer.Channel(1)
menu_music = mixer.Sound('space.ogg')
game_music = mixer.Sound('Zombotany.ogg')
window = display.set_mode((700, 500))
display.set_caption("шутер")
def show_menu():
    global menu_channel, game_channel
    game_channel.stop()
    menu_channel.play(menu_music)
def main():
    global menu_channel, game_channel
    menu_channel.stop()
    game_channel.play(game_music, loops =-1)
class GameSprite(sprite.Sprite):
    def __init__(self, filename, w, h, speed, x, y):
        super().__init__()
        self.image = transform.scale(image.load(filename), (w, h))
        self.speed = speed
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
class Player(GameSprite):
    def __init__(self, filename, w, h, speed, x, y):
        super().__init__(filename, w, h, speed, x, y)
        self.is_parrying = False
        self.parry_duration = 30
        self.parry_timer = 2000
        self.life = 100
    def update(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[K_a] and self.rect.x > 0:
            self.rect.x -= self.speed
        if keys_pressed[K_s] and self.rect.x > 0:
            self.rect.x -= 20
        if keys_pressed[K_d] and self.rect.x < 700 - 65:
            self.rect.x += self.speed
        if keys_pressed[K_w] and self.rect.x < 700 - 65:
            self.rect.x += 20
        if self.is_parrying:
            self.parry_timer -= 1
            if self.parry_timer <= 0:
                self.is_parrying = False
    def fire(self):
        bullet = Bullet("bullet.png", 10, 30, 20, self.rect.centerx, self.rect.top)
        bullets.add(bullet)
    def parry(self):
        if not self.is_parrying:
            self.is_parrying = True
            self.parry_timer = self.parry_duration
class Enemy(GameSprite):  
    def __init__(self, filename, w, h, speed, x, y):
        super().__init__(filename, w, h, speed, x, y)
        self.last_shot_time = time.get_ticks()
        self.shoot_interval = 2500  
        self.damage = 20
    def update(self):
        global lost
        self.rect.y += self.speed
        if self.rect.y >= 500:
            self.rect.y = -80
            self.rect.x = randint(100, 700 - self.rect.w)
            self.speed = randint(1, 3)
            lost += 1
    def shoot(self):
        current_time = time.get_ticks()
        if current_time - self.last_shot_time > self.shoot_interval:
            self.last_shot_time = current_time
            enemybullet = EnemyBullet("bullet.png", 10, 30, 20, self.rect.centerx, self.rect.bottom)
            enemybullets.add(enemybullet)
class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y <= 0:
            self.kill()
class EnemyBullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y  >= 500:
            self.kill()

player = Player("inkay.png", 80, 65, 10, 130, 440)
enemy1 = Enemy("skorupi.png", 80, 80, randint(1, 3), randint(100, 620), 0)
enemy2 = Enemy("skorupi.png", 80, 80, randint(1, 3), randint(100, 620), 0)
enemy3 = Enemy("skorupi.png", 80, 80, randint(1, 3), randint(100, 620), 0)
enemy4 = Enemy("skorupi.png", 80, 80, randint(1, 3), randint(100, 620), 0)
enemy5 = Enemy("skorupi.png", 80, 80, randint(1, 3), randint(100, 620), 0)
btn = GameSprite("start.png", 225, 100, 0, 250, 350)
monsters = sprite.Group()
monsters.add(enemy1, enemy2, enemy3, enemy4, enemy5)
bullets = sprite.Group()
enemybullets = sprite.Group()
buffs = sprite.Group()
game = True
clock = time.Clock()
FPS = 60
background = transform.scale(image.load("galaxy.jpg"), (700, 500))
finish = False
menu = True
menubackground = transform.scale(image.load("megabackground.jpg"), (700, 500))
lost = 0
killed = 0
text_victory = font2.render("Победа!", 1, (0, 255, 0))
text_defeat = font2.render("Поражение", 1, (255, 0, 0))
def pause():
    global menu
    menu = True
    btn.reset
while game:
    if menu:
        window.blit(menubackground, (0, 0))
        btn.reset()
        show_menu()
        for e in event.get():
            if e.type == QUIT:
                game = False
            if e.type == MOUSEBUTTONDOWN:
                x, y = e.pos
                if btn.rect.collidepoint(x, y):
                    menu = False
                    main()
    if finish == False and menu == False:
        window.blit(background, (0, 0))
        player.update()
        player.reset()
        monsters.draw(window)
        monsters.update()
        bullets.draw(window)
        bullets.update()
        text_lose = font1.render("Пропущено:" + str(lost), 1, (255, 0, 0))
        window.blit(text_lose, (10, 50))
        text_win = font1.render("Счёт:" + str(killed), 1, (0, 255, 0))
        window.blit(text_win, (10, 10))
        sprites_list = sprite.groupcollide(monsters, bullets, True, True)
        sprites_list2 = sprite.spritecollide(player, monsters, True)
        sprites_list3 = sprite.spritecollide(player, enemybullets, True)
        for monster in monsters:
            monster.shoot()
        enemybullets.draw(window)
        enemybullets.update()
        for monster in sprites_list:
            killed += 1
            enemy1 = Enemy("skorupi.png", 80, 80, randint(1, 4), randint(100, 620), 0)
            monsters.add(enemy1)
        if killed >= 25:
            finish = True
            window.blit(text_victory, (200, 200))
        for monster in sprites_list2:
            killed += 1
            enemy1 = Enemy("skorupi.png", 80, 80, randint(1, 4), randint(100, 620), 0)
            monsters.add(enemy1)
            if not player.is_parrying:
                player.life -= monster.damage
                finish = True
                window.blit(text_defeat, (200, 200))
                game_channel.stop()
            else:
                print("Attack parried!")
        if lost >= 3 or player.life <= 0:
            finish = True
            window.blit(text_defeat, (200, 200))
        if lost >= 3 or player.life <= 0:
            finish = True
            window.blit(text_defeat, (200, 200))
        for enemybullet in sprites_list3:
            if not player.is_parrying:
                player.life -= 50
                finish = True
                window.blit(text_defeat, (200, 200))
            else:
                print("Attack parried!")
        for e in event.get():
            if e.type == QUIT:
                game = False
            if e.type == KEYDOWN:
                if e.key == K_SPACE:
                    player.fire()
                if e.key== K_p:
                    player.parry()
                if e.key == K_r:
                    pause()
            if e.type == MOUSEBUTTONDOWN:
                player.fire()          
    if finish == True and menu == False:
        for e in event.get():
            if e.type == QUIT:
                game = False
    display.update()
    clock.tick(FPS)
