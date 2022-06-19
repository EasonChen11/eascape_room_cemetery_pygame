# https://www.youtube.com/watch?v=61eX0bFAsYs&ab_channel=GrandmaCan-%E6%88%91%E9%98%BF%E5%AC%A4%E9%83%BD%E6%9C%83
# image https://drive.google.com/drive/folders/10-SA2Fiyf5cm3jUNW2s1zskh0-2eQl9V
# 字體 https://www.pkstep.com/archives/5693
# 字體 https://www.twfont.com/chinese/
# _*_ coding: utf-8 _*_
import time
import pygame
import random
import os
from math import *
FPS = 60    # 60針
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
FINISH_COLOR = (255, 240, 212)
WIDTH = 1530
HEIGHT = 780
image_scale = 900

# 遊戲初始化 and 創建視窗
pygame.init()
# 視窗大小
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("escape room")    # 視窗標題
icon_image = pygame.image.load("./img/icon.png").convert()
pygame.display.set_icon(icon_image)
all_sprites = pygame.sprite.Group()

# 背景音樂
pygame.mixer.init()
pygame.mixer.music.load(f"./music/{random.randrange(0, 6)}.mp3")
pygame.mixer.music.play()

# FPS
clock = pygame.time.Clock()

font_name = os.path.join("./Terror.ttf")  # 取的字型
number_name = pygame.font.match_font('arial')

class list_TEXT:

    def __init__(self):
        self.x = WIDTH/4-100
        self.y = 100
        self.length = 0

    def reset(self):
        self.x = WIDTH/4-55
        self.y = 100
        self.length = 0

    def update(self):
        self.x += 65
        self.length += 1

    def change_line(self):
        self.x = WIDTH/4-55
        self.y += 55
        self.length = 0

    def draw(self, surface, text, size, color):
        font = pygame.font.Font(font_name, size)  # 給定字型和大小# font:字型 render:使成為
        self.text_surface = font.render(text, True, color)  # 製造文字平面(文字,Anti-aliasing{抗鋸齒文字},字體顏色)
        self.text_rect = self.text_surface.get_rect()
        self.text_rect.centerx = self.x
        self.text_rect.centery = self.y
        surface.blit(self.text_surface, self.text_rect)

    def show_screen(self):
        self.reset()
        global index
        for i in ans_list:
            if i in need_list[0:index+1:]:
                locate_text.draw(screen, f"{i}", 50, RED)
            else:
                locate_text.draw(screen, f"{i}", 50, BLACK)
            locate_text.update()
            if locate_text.length > 5:
                locate_text.change_line()
        # bottom_line.reset(locate_text.length, len(ans_list)//6)
        if need_list[index] == ans_list[-1]:
            index += 1


need_list = [2, 10, 14]
game = True
ans_list = [5]
index = 0

icon_image = pygame.transform.scale(icon_image, (image_scale, image_scale))
icon_image_rect = icon_image.get_rect()
icon_image_rect.center = (WIDTH/2, HEIGHT/2)
while game:
    # initial_game()
    # set origin
    index = 0
    running = True
    ans_list = [5]
    '''
    check_list = {5: True}
    which_button_click = False
    click_rule = Rule()
    if first_start:
        show_rule()
        first_start = False
    # create sprites
    add5 = button((image_scale / 2 - 16, HEIGHT - image_scale / 2), 5)
    all_sprites.add(add5)
    add7 = button((WIDTH / 2 + 4, HEIGHT - image_scale / 2), 7)
    all_sprites.add(add7)
    Sqrt = button((WIDTH - image_scale / 2 + 17, HEIGHT - image_scale / 2), 'sqrt')
    all_sprites.add(Sqrt)
    bottom_line = BottomLine()
    all_sprites.add(bottom_line)
    '''
    locate_text = list_TEXT()
    # for event in pygame.event.get():  # 回傳所有動作
    #     if event.type == pygame.MOUSEBUTTONUP:  # 如果按下X ,pygame.QUIT 是按下X後的型態
    '''    
    if game:
        running = True
    '''
    # 遊戲迴圈
    while running and index < 3:
        screen.fill(WHITE)
        screen.blit(icon_image, icon_image_rect)
        clock.tick(FPS)                     # 一秒最多刷新FPS次(1秒跑最多幾次while)
        # 取得輸入
        for event in pygame.event.get():     # 回傳所有動作
            if event.type == pygame.QUIT:    # 如果按下X ,pygame.QUIT 是按下X後的型態
                running = False             # 跳出迴圈
                game = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_5:
                    ans_list.append(ans_list[-1]+5)
                if event.key == pygame.K_7:
                    ans_list.append(ans_list[-1]+7)
                if event.key == pygame.K_s:
                    save = sqrt(ans_list[-1])
                    if save - int(save) > 0:
                        ans_list.append(save)
                    else:
                        ans_list.append(int(save))
        '''        
        # 更新顯示
        screen.blit(background, (0, 0))     # blit(畫) 第一個是圖片，第二個是位置
        click_rule.update()
        '''
        all_sprites.update()
        locate_text.show_screen()
        '''            
            if index < 3:
                great = Great()
                all_sprites.add(great)
        '''
        all_sprites.draw(screen)
        pygame.display.flip()                      # 更新畫面=pygame.display.flip()更新全部，update可以有參數

pygame.mixer.music.stop()
pygame.quit()
