import pygame
from random import randint, random
from constants import SCREEN_HEIGHT, SCREEN_WIDTH

# 初始化

# 飞机图片 
plane_img = pygame.image.load('resources/image/shoot.png')
# 设置玩家飞机不同状态的图片列表，多张图片展示为动画效果
player_rect = []
player_rect.append(pygame.Rect(0, 99, 102, 126)) # 玩家飞机图片
player_rect.append(pygame.Rect(165, 360, 102, 126))
player_rect.append(pygame.Rect(165, 234, 102, 126)) # 玩家爆炸图片
player_rect.append(pygame.Rect(330, 624, 102, 126))
player_rect.append(pygame.Rect(330, 498, 102, 126))
player_rect.append(pygame.Rect(432, 624, 102, 126))
# 飞机初始位置
player_pos = [200, 600]

# 子弹图片
bullet_rect = pygame.Rect(1004, 987, 9, 21)
bullet_img = plane_img.subsurface(bullet_rect)

# 敌机不同状态的图片列表，多张图片展示为动画效果
enemy_img = plane_img.subsurface(pygame.Rect(534, 612, 57, 43))
enemy_down_imgs = []
enemy_down_imgs.append(plane_img.subsurface(pygame.Rect(267, 347, 57, 43)))
enemy_down_imgs.append(plane_img.subsurface(pygame.Rect(873, 697, 57, 43)))
enemy_down_imgs.append(plane_img.subsurface(pygame.Rect(267, 296, 57, 43)))
enemy_down_imgs.append(plane_img.subsurface(pygame.Rect(930, 697, 57, 43)))
enemy_img_group = []
enemy_img_group.append([enemy_img, enemy_down_imgs])
enemy_img = plane_img.subsurface(pygame.Rect(168, 747, 168, 248))
enemy_down_imgs = []
enemy_down_imgs.append(plane_img.subsurface(pygame.Rect(0, 490, 168, 248)))
enemy_down_imgs.append(plane_img.subsurface(pygame.Rect(0, 227, 168, 248)))
enemy_down_imgs.append(plane_img.subsurface(pygame.Rect(167, 487, 168, 248)))
enemy_down_imgs.append(plane_img.subsurface(pygame.Rect(670, 750, 168, 248)))
enemy_img_group.append([enemy_img, enemy_down_imgs])
# end 初始化

#子弹类
class Bullet(pygame.sprite.Sprite):
    def __init__(self, player, bullet_img, init_pos):
        super(Bullet, self).__init__()
        self.player = player
        self.image = bullet_img
        self.rect = bullet_img.get_rect()
        self.rect.midbottom = init_pos
        self.speed = 10
    
    def move(self):
        self.rect.top -= self.speed
    
    def update(self):
        # 以固定速度移动子弹
        self.move()
        # 移动出屏幕后删除子弹
        if self.rect.bottom < 0:
            self.player.bullets.remove(self)


# 玩家飞机类
class Player(pygame.sprite.Sprite):
    def __init__(self, plane_img=plane_img, player_rect=player_rect, init_pos=player_pos):
        super(Player, self).__init__()
        self.image = [plane_img.subsurface(rect).convert_alpha() for rect in player_rect] # 用来存储玩家飞机图片的列表
        self.rect = player_rect[0] # 初始化图片所在的矩形,默认第一个为玩家飞机种类
        self.rect.topleft = init_pos # # 初始化矩形的左上角坐标
        self.speed = 8 # 初始化玩家飞机速度，这里是一个确定的值
        self.bullets = pygame.sprite.Group() # 玩家飞机所发射的子弹的集合
        self.img_index = 0 # 玩家飞机图片索引
        self.is_hit = False # 玩家是否被击中
        self.shoot_frequency = 0 # 初始化射击频率

    # 发射子弹
    def shoot(self, bullet_img=bullet_img):
        bullet = Bullet(self, bullet_img, self.rect.midtop)
        self.bullets.add(bullet)
    
    def update(self):
        # 更换图片索引使飞机有动画效果
        self.img_index = self.shoot_frequency // 8
        # 生成子弹，需要控制发射频率
        # 首先判断玩家飞机没有被击中
        if not self.is_hit:
            if self.shoot_frequency % 15 == 0:
                self.shoot(bullet_img)
            self.shoot_frequency += 1
            if self.shoot_frequency >= 15:
                self.shoot_frequency = 0
        for bullet in self.bullets:
            bullet.update()

    # 向上移动,需要判定边界
    def moveUp(self):
        self.rect.top = max(self.rect.top - self.speed, 0)
    
    # 向下移动，需要判断边界
    def moveDown(self):
        self.rect.top = min(self.rect.top + self.speed, SCREEN_HEIGHT - self.rect.height)

    # 向左移动，需要判断边界
    def moveLeft(self):
        self.rect.left = max(self.rect.left - self.speed, 0)
    
    # 向右移动，需要判断边界
    def moveRight(self):
        self.rect.left = min(self.rect.left + self.speed, SCREEN_WIDTH - self.rect.width)

# 敌机类
class Enemy(pygame.sprite.Sprite):
    def __init__(self, enemy_img_group=enemy_img_group):
        super(Enemy, self).__init__()
        self.ridx = 0 if random() > 0.2 else 1
        self.image = enemy_img_group[self.ridx][0]
        self.rect = self.image.get_rect()
        self.rect.topleft = [randint(0, SCREEN_WIDTH - self.rect.width), 0]
        self.down_imgs = enemy_img_group[self.ridx][1]
        self.speed = 2
        self.down_index = 0
        self.moving = False
        self.direction = 1 # -1向左,1向右
        self.count = 30 # 移动持续时间计数
    
    # 敌机移动，边界判断及删除在游戏主循环里处理
    def move(self):
        self.rect.top += self.speed
        if self.ridx:
            return
        if not self.moving:
            self.moving = random() > 0.6
            self.direction = randint(0, 1) * 2 - 1
        if self.moving and self.count:
            self.count -= 1
            self.rect.left = min(max(0, self.rect.left + self.speed * self.direction), SCREEN_WIDTH - self.rect.width)
        else:
            self.moving = False
            self.count = 30
    
    def update(self, player, enemies, enemies_down):
        #2. 移动敌机
        self.move()
        #3. 敌机与玩家飞机碰撞效果处理
        if pygame.sprite.collide_circle(self, player):
            enemies_down.add(self)
            enemies.remove(self)
            player.is_hit = True
        #4. 移动出屏幕后删除飞机    
        if self.rect.top < 0:
            enemies.remove(self)
        
        #敌机被子弹击中效果处理
        # 将被击中的敌机对象添加到击毁敌机 Group 中，用来渲染击毁动画
        for enemy_down in pygame.sprite.groupcollide(enemies, player.bullets, 1, 1):
            enemies_down.add(enemy_down)