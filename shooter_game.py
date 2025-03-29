#Создай собственный Шутер!

from pygame import *
from random import randint
window = display.set_mode((700,500))
display.set_caption('Шутер')
class GameSprite(sprite.Sprite):
    def __init__(self,player_image, player_x, player_y, player_width, player_height, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (player_width, player_height))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
        

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x >5:
            self.rect.x -= self.speed
        if keys [ K_RIGHT] and self.rect.x < 635 :
            self.rect.x += self.speed
    def fire(self): 
        bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top, 15 , 20, -15)
        bullets.add(bullet)
        
lost = 0
class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > 635:
            self.rect.x = randint(80, 500)
            self.rect.y = -60
            lost = lost +1
class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0: 
            self.kill()
class Metyor(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y > 635:
            self.rect.x = randint(80,500)
            self.rect.y = -60

background = transform.scale(image.load('galaxy.jpg'),(700,500))

game = True
finish = False
clock = time.Clock()
FPS = 60
mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
player = Player('rocket.png', 260, 400, 60, 100, 10 )
metyor = Metyor('asteroid.png', randint(0,600), -100, 100, 60, 3)
metyors = sprite.Group()
monsters = sprite.Group() 
for i in range(5):
    enemy = Enemy('ufo.png', randint(0, 600), -100, 100 ,60, randint(1,3))
    monsters.add(enemy)
for i in range(3):
    metyor = Metyor('asteroid.png', randint(0,600), -100, 100, 60, 3)
    metyors.add(metyor)

bullets = sprite.Group()


font.init()
font1 = font.SysFont('Arial', 36)
glasses = 0 


lose = font1.render('Проигрыш', True,(255,0,0))
win = font1.render('Выигрыш', True, (255,215,0))
life = font1.render('Жизни', True, (255,215,0))
while game:
    
    for e in event.get():
        if e.type == QUIT:
            game = False
        if e.type == KEYDOWN:
            if e.key == K_SPACE:
                player.fire()
    if finish != True:
        window.blit(background,(0 , 0))
        player.reset()
        player.update()
        metyors.update()
        metyors.draw(window)
        monsters.draw(window)
        monsters.update()
        bullets.draw(window)
        bullets.update()
        text_lose = font1.render('Пропущено:' + str(lost), 1, (255,255,255))
        window.blit(text_lose, (0, 0))
        text_lose = font1.render('Счет:' + str(glasses), 1, (255,255,255))
        window.blit(text_lose, (0, 30))
    
        if sprite.spritecollide(player, monsters, False) or (lost > 3):
            finish = True
            window.blit(lose,(200,200))
        if sprite.spritecollide(player, metyors, False):
            finish = True
            window.blit(lose,(200,200))
        if glasses > 5:
            finish = False
            window.blit(life,(200,200))

        for m in sprite.groupcollide(monsters, bullets, True, True):
            glasses += 1 
            monster = Enemy('ufo.png', randint(0, 600), -100, 100 ,60, randint(1,3))
            monsters.add(monster)
        if glasses > 5:
            finish = True
            window.blit(win,(200,200))
        
        
        
    display.update()
    clock.tick(60)