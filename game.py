#!/usr/bin/env python3

__author__ ='Etern'

'''
显示玩家飞机（代码中使用的 resources/image/shoot.png 图里包含多种飞机，
只需要使用 pygame.image 的 subsurface API 根据位置截取 shoot.png 中所需的图片）

pygame.image.load(filename) 用于加载指定图像，并且返回一个 pygame.Surface 对象。
值得注意的是，我们通常还使用 Surface.convert() 方法来获取原图像的副本，
因为这个副本能在窗口屏幕上以更快的速度绘制。另外，
对于包含透明通道的图片（PNG）我们还必须使用 Surface.convert_alpha() 
方法来确保透明通道信息被正确加载。
'''

'''
子弹由玩家飞机发出，并以一定速度向界面上方移动。

详细步骤

生成子弹，需要控制发射频率
以固定速度移动子弹
移动出屏幕后删除子弹
'''

'''
敌机需要随机在界面上方产生，并以一定速度向下移动。

详细步骤

生成敌机，需要控制生成频率
移动敌机
敌机与玩家飞机碰撞效果处理
移动出屏幕后删除敌机
敌机被子弹击中效果处理
'''

# pygame 坐标系为左上角原点,右为X正向,下为Y正向
# cocos则是坐标系为左下角原点,右为X正向,上为Y正向
import pygame
from sys import exit
from entity import Player, Bullet, Enemy, enemy1_rect
from constants import SCREEN_HEIGHT, SCREEN_WIDTH
from random import randint





# 1. 初始化 pygame
pygame.init()

#2. 设置游戏界面大小、背景图片及标题
# 游戏界面像素大小
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# 游戏界面标题
pygame.display.set_caption('飞机大战')

# 背景图
background = pygame.image.load('resources/image/background.png').convert_alpha()

# Game Over 背景图
game_over = pygame.image.load('resources/image/gameover.png').convert_alpha()


player = Player()

enemies1 = pygame.sprite.Group()

# 存储被击毁的飞机，用来渲染击毁动画
enemies_down = pygame.sprite.Group()

# 初始化敌机生成频率
enemy_frequency = 0

# 玩家飞机被击中后的效果处理
player_down_index = 16

# 初始化分数
score = 0

# 游戏循环帧率设置
clock = pygame.time.Clock()

# 判断游戏循环退出的参数
running = True

# 游戏主循环
#3. 游戏主循环内需要处理游戏界面的初始化、更新及退出
while running:
    # 控制游戏最大帧率为 60
    clock.tick(60)

    player.update()

    # 生成敌机，需要控制生成频率
    if enemy_frequency % 50 == 0:
        enemy_pos = [randint(0, SCREEN_WIDTH - enemy1_rect.width), 0]
        enemy1 = Enemy(init_pos=enemy_pos)
        enemies1.add(enemy1)
    enemy_frequency += 1
    if enemy_frequency >= 100:
        enemy_frequency = 0

    for enemy in enemies1:
        enemy.update(player, enemies1, enemies_down)

    # 初始化游戏屏幕
    screen.fill(0)
    screen.blit(background, (0, 0))

    # 绘制玩家飞机
    if not player.is_hit:
        screen.blit(player.image[player.img_index], player.rect)
    
    # 显示子弹
    player.bullets.draw(screen)
    # 显示敌机
    enemies1.draw(screen)

    # 更新屏幕
    pygame.display.update()

    # 游戏退出事件
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()