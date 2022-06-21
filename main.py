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
image_scale = 1000
button_5 = 5
button_7 = 7
button_sqrt = 'sqrt'
# 遊戲初始化 and 創建視窗
pygame.init()
# 視窗大小
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("escape room")    # 視窗標題
icon_image = pygame.image.load("./img/icon.png").convert()
icon_image.set_colorkey(BLACK)
pygame.display.set_icon(icon_image)
all_sprites = pygame.sprite.Group()

# 背景音樂
pygame.mixer.init()
pygame.mixer.music.load(f"./music/{random.randrange(0, 6)}.mp3")
#pygame.mixer.music.play()

# FPS
clock = pygame.time.Clock()

# 取得字型
font_name = os.path.join("./Terror.ttf")
number_name = pygame.font.match_font('arial')

# 載入所需圖片
nuber_list_background = pygame.image.load("./img/icon2.jpg").convert()
nuber_list_background.set_colorkey(BLACK)
# rule_image = pygame.image.load("./img/").convert()
# rule_image.set_colorkey(BLACK)
button_images = {button_5: [], button_7: [], button_sqrt: []}
for which_button in button_images:
    for number_of_pictures in range(2):
        save_image = pygame.image.load(f"./img/{which_button}_{number_of_pictures}.jpg").convert()
        save_image.set_colorkey(WHITE)
        save_image = pygame.transform.scale(save_image, (image_scale/7, image_scale/7))
        button_images[which_button].append(save_image)


class list_TEXT:

    def __init__(self):
        self.ans_list = [5]
        self.check_list = {5: True}
        self.x = WIDTH*3/5+80
        self.y = 300
        self.length = 0
        self.change_line_llu = 4
        self.change_line_times = 0
        self.small_change_y = (0, 5, -5)
        self.random_index = random.randrange(0, self.small_change_y.__sizeof__(), 1)
        self.small_change_y_index = self.random_index

    def reset(self):
        self.x = WIDTH*3/5+80
        self.y = 300
        self.length = 0
        self.change_line_times = 0
        self.small_change_y_index = self.random_index
        self.change_line_llu = 4

    def update(self):
        self.x += 85
        self.length += 1
        self.small_change_y_index += 1

    def change_line(self):
        if self.change_line_times > 4:
            self.change_line_llu = 3
            self.x = WIDTH*3/5+130
        else:
            self.x = WIDTH*3/5+80
        self.y += 55
        self.length = 0

    def draw(self, surface, text, size, color):
        font = pygame.font.Font(font_name, size)  # 給定字型和大小# font:字型 render:使成為
        self.text_surface = font.render(text, True, color)  # 製造文字平面(文字,Anti-aliasing{抗鋸齒文字},字體顏色)
        self.text_rect = self.text_surface.get_rect()
        self.text_rect.centerx = self.x
        self.text_rect.centery = self.y+self.small_change_y[self.small_change_y_index % 3]
        surface.blit(self.text_surface, self.text_rect)

    def show_screen(self):
        self.reset()
        global index
        for i in self.ans_list:
            if i in need_list[0:index+1:]:
                self.draw(screen, f"{i}", 50, RED)
            else:
                self.draw(screen, f"{i}", 50, BLACK)
            self.update()
            if self.length >= self.change_line_llu:
                self.change_line_times += 1
                self.change_line()
        # bottom_line.reset(locate_text.length, len(ans_list)//6)
        if need_list[index] == self.ans_list[-1]:
            index += 1


class button (pygame.sprite.Sprite):
    def __init__(self, center, button_name):
        self.click = False
        pygame.sprite.Sprite.__init__(self)
        self.frame = 0
        self.name = button_name
        self.image = button_images[self.name][self.frame]
        self.rect = self.image.get_rect()
        self.basis_center = center
        self.rect.center = self.basis_center

    def update(self):
        global each_button_click
        if self.click:
            if not pygame.mouse.get_pressed()[0]:
                self.frame = 0
                self.image = button_images[self.name][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = self.basis_center
                self.click = False
                each_button_click = False
        else:
            mouse_press = pygame.mouse.get_pos()
            if self.rect.collidepoint(mouse_press):
                if pygame.mouse.get_pressed()[0]:
                    if not each_button_click:
                        global locate_text
                        each_button_click = True
                        self.click = True
                        self.frame = 1
                        self.image = button_images[self.name][self.frame]
                        self.rect = self.image.get_rect()
                        self.rect.center = self.basis_center
                        # input
                        if self.name == 5:
                            locate_text.ans_list.append(locate_text.ans_list[-1] + 5)
                        if self.name == 7:
                            locate_text.ans_list.append(locate_text.ans_list[-1] + 7)
                        if self.name == 'sqrt':
                            append_number = round(sqrt(locate_text.ans_list[-1]), 2)  # round 四捨五入到小數兩位
                            if append_number - int(append_number) == 0:
                                locate_text.ans_list.append(int(append_number))
                            else:
                                locate_text.ans_list.append(append_number)
                        # check error
                        global running
                        if locate_text.check_list.get(locate_text.ans_list[-1]):
                            running = False
                            which_error["repeat"][1] = True
                        else:
                            locate_text.check_list[locate_text.ans_list[-1]] = True
                        if locate_text.ans_list[-1] - int(locate_text.ans_list[-1]) != 0:
                            running = False
                            which_error["decimal"][1] = True
                        if locate_text.ans_list[-1] > 50:
                            running = False
                            which_error["big than 50"][1] = True


locate_text = list_TEXT()
each_button_click = False
# check_list = {5: True}
# ans_list = [5]
need_list = [2, 10, 14]
which_error = {"repeat": ["數字重複啦", False], "decimal": ["啥?有小數點", False], "big than 50": ["數字>50啦", False]}
game = True
index = 0
nuber_list_background = pygame.transform.scale(nuber_list_background, (image_scale+600, image_scale))
nuber_list_background_rect = nuber_list_background.get_rect()
nuber_list_background_rect.center = (WIDTH*3/4-50, HEIGHT/2+20)
while game:
    # initial_game()
    # set origin
    each_button_click = False
    index = 0
    running = True
    # ans_list = [5]
    # check_list = {5: True}
    add5 = button((WIDTH*3/4-150, HEIGHT*5/6+50), button_5)
    add7 = button((WIDTH*3/4, HEIGHT*5/6+50), button_7)
    Sqrt = button((WIDTH*3/4+150, HEIGHT*5/6+50), button_sqrt)
    all_sprites.add(add5)
    all_sprites.add(add7)
    all_sprites.add(Sqrt)
    '''
    check_list = {5: True}
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
    # for event in pygame.event.get():  # 回傳所有動作
    #     if event.type == pygame.MOUSEBUTTONUP:  # 如果按下X ,pygame.QUIT 是按下X後的型態
    '''    
    if game:
        running = True
    '''
    # 遊戲迴圈
    while running and index < 3:
        screen.fill(BLACK)
        screen.blit(nuber_list_background, nuber_list_background_rect)
        clock.tick(FPS)                     # 一秒最多刷新FPS次(1秒跑最多幾次while)
        # 取得輸入
        for event in pygame.event.get():     # 回傳所有動作
            if event.type == pygame.QUIT:    # 如果按下X ,pygame.QUIT 是按下X後的型態
                running = False             # 跳出迴圈
                game = False
            '''            
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
    if game:
        add5.kill()
        add7.kill()
        Sqrt.kill()
        locate_text.__init__()

pygame.mixer.music.stop()
pygame.quit()
