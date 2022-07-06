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


# FPS
clock = pygame.time.Clock()

# 取得字型
number_font = os.path.join("./Terror.ttf")
normal_font = pygame.font.match_font('arial')
rule_font = os.path.join("./Brush.ttf")
# 載入所需圖片
nuber_list_background = pygame.image.load("./img/nuber_list_background.jpg").convert()
nuber_list_background.set_colorkey(BLACK)
nuber_list_background = pygame.transform.scale(nuber_list_background, (image_scale-400, image_scale-250))

rule_background = pygame.image.load("./img/rule_background_high.jpg").convert()
rule_background.set_colorkey(BLACK)

# try again images load
try_again_images = {"normal": [], "again": []}
for do_again in range(6):
    try_again_image = pygame.image.load(f"./img/fire/normal_{do_again}.png")
    try_again_image = pygame.transform.scale(try_again_image, (image_scale / 4, image_scale / 4))
    try_again_images["normal"].append(try_again_image)
for do_again in range(2):
    try_again_image = pygame.image.load(f"./img/fire/again_{do_again}.png")
    try_again_image = pygame.transform.scale(try_again_image, (image_scale / 4, image_scale / 4))
    try_again_images["again"].append(try_again_image)

# button images load
button_images = {button_5: [], button_7: [], button_sqrt: []}
for which_button in button_images:
    for number_of_pictures in range(2):
        save_image = pygame.image.load(f"./img/button/{which_button}_{number_of_pictures}.jpg").convert()
        save_image.set_colorkey(WHITE)
        save_image = pygame.transform.scale(save_image, (image_scale/7, image_scale/7))
        button_images[which_button].append(save_image)

# bat images load
bat_image = pygame.image.load("./img/bat/bat.png")

# moon images load
moon_images = {'yellow': [], 'red': []}
for color_moon in moon_images:
    moon_image = pygame.image.load(f"./img/moon/moon_{color_moon}.png")
    moon_image = pygame.transform.scale(moon_image, (image_scale/2, image_scale/3))
    moon_image.set_colorkey(BLACK)
    moon_images[color_moon].append(moon_image)

# text image
finish_text = []
for do_again in range(5):
    message_image = pygame.image.load(f"./img/text/finish_{do_again}.png")
    message_image = pygame.transform.scale(message_image, (image_scale, image_scale))
    finish_text.append(message_image)
which_error = {"repeat": [], "decimal": [], "big than 50": []}
for which_message in which_error:
    message_image = pygame.image.load(f"./img/text/{which_message}.png")
    message_image = pygame.transform.scale(message_image, (image_scale / 2, image_scale / 3))
    which_error[which_message].append(message_image)
    which_error[which_message].append(False)

# start image
start_images = {"first": [], "second": []}
for which_start in start_images:
    for do_again in range(5):
        start_image = pygame.image.load(f"./img/text/{which_start}_{do_again}.png")
        start_image = pygame.transform.scale(start_image, (image_scale*3/5, image_scale*3/5))
        start_image = pygame.transform.rotate(start_image, -20)
        start_images[which_start].append(start_image)


class ListText:

    def __init__(self):
        self.background = nuber_list_background.copy()
        self.rect = self.background.get_rect()
        self.rect.center = (WIDTH * 3 / 4 + 20, HEIGHT / 2)
        self.ans_list = [5]
        self.check_list = {5: True}
        self.x = self.rect.left
        self.y = self.rect.bottom
        self.length = 0
        self.change_line_llu = 5
        self.change_line_times = 0
        self.small_change_y = (0, 5, -5)
        self.size = 50
        self.font = pygame.font.Font(number_font, self.size)  # 給定字型和大小# font:字型 render:使成為
        self.random_index = random.randrange(0, self.small_change_y.__sizeof__(), 1)
        self.small_change_y_index = self.random_index
        self.index = 1

    def reset(self):
        self.background = nuber_list_background.copy()
        self.x = self.rect.width/12+50
        self.y = self.rect.height/3+30
        self.length = 0
        self.change_line_times = 0
        self.small_change_y_index = self.random_index
        self.change_line_llu = 5
        self.index = 1

    def update(self):
        self.x += 85
        self.length += 1
        self.small_change_y_index += 1

    def change_line(self):
        if self.change_line_times > 1:
            self.change_line_llu = 4
            self.x = self.rect.width / 12 + 90
        else:
            self.x = self.rect.width / 12 + 50
        self.y += 60
        self.length = 0

    def draw(self, text, color):
        text_surface = self.font.render(text, True, color)  # 製造文字平面(文字,Anti-aliasing{抗鋸齒文字},字體顏色)
        # text_surface.fill(WHITE)
        text_rect = text_surface.get_rect()
        text_rect.centerx = self.x
        text_rect.centery = self.y+self.small_change_y[self.small_change_y_index % 3]
        self.background.blit(text_surface, text_rect)

    def show_screen(self):
        self.reset()
        global index
        for i in self.ans_list:
            if i in need_list[0:self.index:]:
                self.draw(f"{i}", RED)
                if self.index < index:
                    self.index += 1
            else:
                self.draw(f"{i}", BLACK)
            self.update()
            if self.length >= self.change_line_llu:
                self.change_line_times += 1
                self.change_line()
        # bottom_line.reset(locate_text.length, len(ans_list)//6)


class Button(pygame.sprite.Sprite):
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
                self.check_which_error()
        else:
            mouse_press = pygame.mouse.get_pos()
            if self.rect.collidepoint(mouse_press):
                if pygame.mouse.get_pressed()[0]:
                    if not each_button_click:
                        each_button_click = True
                        self.click = True
                        self.frame = 1
                        self.image = button_images[self.name][self.frame]
                        self.rect = self.image.get_rect()
                        self.rect.center = self.basis_center
                        self.input_number()

    def input_number(self):
        # input
        global locate_text, index
        if self.name == 5:
            locate_text.ans_list.append(locate_text.ans_list[-1] + 5)
        elif self.name == 7:
            locate_text.ans_list.append(locate_text.ans_list[-1] + 7)
        elif self.name == 'sqrt':
            append_number = round(sqrt(locate_text.ans_list[-1]), 2)  # round 四捨五入到小數兩位
            if append_number - int(append_number) == 0:
                locate_text.ans_list.append(int(append_number))
            else:
                locate_text.ans_list.append(append_number)
        if need_list[index] == locate_text.ans_list[-1]:
            index += 1
            moon.red_moon()
        else:
            moon.__init__()

    def check_which_error(self):
        global running, try_again, locate_text
        if locate_text.ans_list[-1] - int(locate_text.ans_list[-1]) != 0:
            running = False
            try_again.force_click = True
            which_error["decimal"][1] = True
        elif locate_text.ans_list[-1] > 50:
            running = False
            try_again.force_click = True
            which_error["big than 50"][1] = True
        elif locate_text.check_list.get(locate_text.ans_list[-1]):
            running = False
            try_again.force_click = True
            which_error["repeat"][1] = True
        else:
            locate_text.check_list[locate_text.ans_list[-1]] = True


class Tryagain(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.frame = 0
        self.tick = 300
        self.fire_name = "normal"
        self.image = try_again_images[self.fire_name][self.frame]
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH-80, HEIGHT-100)
        self.text = pygame.image.load("./img/again.jpg")
        self.text.set_colorkey(WHITE)
        self.text = pygame.transform.scale(self.text, (image_scale/10, image_scale/10))
        self.text_rect = self.text.get_rect()
        self.basis_center = self.rect.center
        self.now = pygame.time.get_ticks()
        self.last_update = self.now
        self.click = False
        self.force_click = False
        self.back = False

    def update(self):
        screen.blit(self.text, (WIDTH-130, HEIGHT-120))
        global each_button_click, running
        self.animation()
        if self.click:
            if not pygame.mouse.get_pressed()[0]:
                self.tick = 300
                self.frame = 0
                self.fire_name = "normal"
                self.image = try_again_images[self.fire_name][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = self.basis_center
                self.click = False
                each_button_click = False
                global running
                running = False
        else:
            mouse_press = pygame.mouse.get_pos()
            if self.rect.collidepoint(mouse_press) and pygame.mouse.get_pressed()[0]:
                if not each_button_click:
                    each_button_click = True
                    self.click = True
                    self.tick = 100
                    self.frame = 0
                    self.fire_name = "again"
                    self.image = try_again_images[self.fire_name][self.frame]
                    self.rect = self.image.get_rect()
                    self.rect.center = self.basis_center

    def animation(self):
        screen.blit(self.text, (WIDTH-130, HEIGHT-120))
        now = pygame.time.get_ticks()
        if now - self.last_update > self.tick:  # 瞬間當下時間 跟 創建時間差 到換圖時間(ex.時間差到50ms時換下張圖)
            self.last_update = now
            if not self.back:
                self.frame += 1
                if self.frame < len(try_again_images[self.fire_name]):
                    self.image = try_again_images[self.fire_name][self.frame]
                    center = self.rect.center
                    self.rect = self.image.get_rect()
                    self.rect.center = center
                else:
                    self.back = True
            else:
                self.frame -= 1
                if self.frame >= 0:
                    self.image = try_again_images[self.fire_name][self.frame]
                    center = self.rect.center
                    self.rect = self.image.get_rect()
                    self.rect.center = center
                else:
                    self.back = False

    def force_doing(self):
        self.animation()
        mouse_press = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_press):
            if pygame.mouse.get_pressed()[0]:
                self.frame = 0
                self.fire_name = "normal"
                self.image = try_again_images[self.fire_name][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = self.basis_center
                self.force_click = False


class Rule(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = rule_background
        self.image = pygame.transform.scale(self.image, (image_scale-50, image_scale-250))
        self.big_image = self.image.copy()
        self.rect = self.image.get_rect()
        self.rect.center = (450, 400)
        self.text = ["1.面板有三個骨頭，+5, +7 和開根號",
                     "2.用滑鼠按下骨頭完成謎題",
                     "3.計數從5開始",
                     "4.顯示器上要必須依序出現",
                     "  2, 10, 14這三個數字，可不必連續",
                     "   (如:1,2,8,10,18,14...)",
                     "5.顯示器上可以顯示任何數字，",
                     "  但有些條件:",
                     "  a)同一個數字不能出現兩次",
                     "    (包含第一個5)",
                     "  b)顯示器上的數字不能大於50",
                     "  c)不能出現小數(開根號不能有小數)",
                     "6.可以按下銘文碑放大規則",
                     "7.可以按下右下角火焰重新開始"]
        self.size = 35
        self.font = pygame.font.Font(rule_font, self.size)
        self.color = WHITE
        self.click = False
        self.y_change = 40
        self.draw(self.image, self.rect.left+self.rect.width/5+10, self.rect.top+self.rect.height/5+10)

    def update(self):
        global each_button_click
        mouse_press = pygame.mouse.get_pos()
        if self.click:
            show_rule()
            self.click = False
            each_button_click = False
        elif self.rect.collidepoint(mouse_press) and pygame.mouse.get_pressed()[0]:
            if not each_button_click:
                self.click = True
                each_button_click = True

    def draw(self, surface, x, y):
        for text in self.text:
            text_surface = self.font.render(text, True, self.color)  # 製造文字平面(文字,Anti-aliasing{抗鋸齒文字},字體顏色)
            text_rect = text_surface.get_rect()
            text_rect.left = x
            text_rect.centery = y-40
            surface.blit(text_surface, text_rect)
            y += self.y_change


class Moon:
    def __init__(self):
        self.image = moon_images['yellow'][0]
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH/2-100, 10)

    def red_moon(self):
        self.image = moon_images['red'][0]
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH/2-100, 10)

class Bat:
    def __init__(self):
        self.image = pygame.transform.rotate(bat_image.copy(), 30)
        self.image = pygame.transform.scale(self.image, (image_scale / 5, image_scale / 5))
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH*3/5-20, 30)


class ErrorMessage:
    def __init__(self, wrong_message):
        self.origin_image = which_error[wrong_message][0]
        self.rect = self.origin_image.get_rect(center=(WIDTH/2, HEIGHT/2))
        # self.rect.center = (WIDTH/2, HEIGHT/2)
        self.angle = 0
        self.angle_speed = 20
        self.scale = 0
        self.scale_speed = image_scale/18
        self.new_image = pygame.transform.scale(self.origin_image, (self.scale, self.scale))
        self.last_update = pygame.time.get_ticks()
        self.tick = 20
        self.times = 18
        self.move = 450

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.tick and self.times:
            self.last_update = now
            self.times -= 1
            self.scale += self.scale_speed
            self.angle += self.angle_speed
            self.new_image = pygame.transform.scale(self.origin_image, (self.scale, self.scale))
            self.new_image = pygame.transform.rotate(self.new_image, self.angle)
            self.rect = self.new_image.get_rect(center=(WIDTH/2-self.move, HEIGHT/2-self.move))
        if not self.times:
            self.tick = 1100
            if now - self.last_update > self.tick:
                self.new_image = pygame.transform.scale(self.origin_image, (0, 0))


class FinishMessage:
    def __init__(self):
        self.run = True
        self.frame = 0
        self.tick = 100
        self.image = finish_text[self.frame]
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH/2, HEIGHT/2)
        self.basis_center = self.rect.center
        self.last_update = pygame.time.get_ticks()
        self.back = False

    def animation(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.tick:  # 瞬間當下時間 跟 創建時間差 到換圖時間(ex.時間差到50ms時換下張圖)
            self.last_update = now
            if not self.back:
                self.frame += 1
                if self.frame < len(finish_text):
                    self.image = finish_text[self.frame]
                    self.rect = self.image.get_rect(center=self.basis_center)
                else:
                    self.back = True
            else:
                self.frame -= 1
                if self.frame >= 0:
                    self.image = finish_text[self.frame]
                    self.rect = self.image.get_rect(center=self.basis_center)
                else:
                    self.back = False


class StartMessage:
    def __init__(self, name):
        self.name = name
        self.run = True
        self.frame = 0
        self.tick = 100
        self.image = start_images[self.name][self.frame]
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH/2, HEIGHT/2)
        self.basis_center = self.rect.center
        self.last_update = pygame.time.get_ticks()
        self.back = False

    def animation(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.tick:  # 瞬間當下時間 跟 創建時間差 到換圖時間(ex.時間差到50ms時換下張圖)
            self.last_update = now
            if not self.back:
                self.frame += 1
                if self.frame < len(start_images[self.name]):
                    self.image = start_images[self.name][self.frame]
                    self.rect = self.image.get_rect(center=self.basis_center)
                else:
                    self.back = True
            else:
                self.frame -= 1
                if self.frame >= 0:
                    self.image = start_images[self.name][self.frame]
                    self.rect = self.image.get_rect(center=self.basis_center)
                else:
                    self.back = False


def try_again_func():
    global try_again, running, game, which_message
    try_again.frame = 0
    try_again.fire_name = "again"
    try_again.tick = 100
    for which_message in which_error:
        if which_error[which_message][1]:
            break
    error = ErrorMessage(which_message)
    while try_again.force_click:
        clock.tick(FPS)                     # 一秒最多刷新FPS次(1秒跑最多幾次while)
        for try_again_event in pygame.event.get():     # 回傳所有動作
            if try_again_event.type == pygame.QUIT:    # 如果按下X ,pygame.QUIT 是按下X後的型態
                running = False             # 跳出迴圈
                game = False
                try_again.force_click = False
        screen.fill(BLACK)
        try_again.force_doing()  # 檢查按下
        screen.blit(moon.image, moon.rect.center)
        screen.blit(locate_text.background, locate_text.rect)
        screen.blit(bat.image, bat.rect.center)
        all_sprites.draw(screen)
        error.update()
        screen.blit(error.new_image, error.rect.center)
        screen.blit(try_again.text, (WIDTH-130, HEIGHT-120))
        pygame.display.update()                      # 更新畫面=pygame.display.flip()更新全部，update可以有參數
    time.sleep(0.2)


def finish_func():
    global try_again, running, game
    add7.__init__((WIDTH*3/4, HEIGHT*5/6+50), button_7)
    finish = FinishMessage()
    while finish.run:
        clock.tick(FPS)                     # 一秒最多刷新FPS次(1秒跑最多幾次while)
        for finish_event in pygame.event.get():     # 回傳所有動作
            if finish_event.type == pygame.QUIT:    # 如果按下X ,pygame.QUIT 是按下X後的型態
                running = False             # 跳出迴圈
                game = False
                finish.run = False
        screen.fill(BLACK)
        screen.blit(moon.image, moon.rect.center)
        screen.blit(locate_text.background, locate_text.rect)
        screen.blit(bat.image, bat.rect.center)
        finish.animation()
        try_again.animation()
        all_sprites.draw(screen)
        screen.blit(finish.image, (350, -100))
        screen.blit(try_again.text, (WIDTH-130, HEIGHT-120))
        pygame.display.update()                      # 更新畫面=pygame.display.flip()更新全部，update可以有參數
    time.sleep(0.2)


def show_rule():
    global running, game, rule, first_run
    if first_run:
        start = StartMessage("first")
    else:
        start = StartMessage("second")
        time.sleep(0.5)
    rule.font = pygame.font.Font(rule_font, 50)
    rule.big_image = pygame.transform.scale(rule.big_image, (image_scale*1.5, image_scale*0.8))
    rule.y_change = 45
    rule.draw(rule.big_image, WIDTH/5, HEIGHT/4-10)
    rule_run = True
    relax = False   # 第一次放開
    click = False   # 第二次放開
    while rule_run:
        clock.tick(FPS)                     # 一秒最多刷新FPS次(1秒跑最多幾次while)
        for finish_event in pygame.event.get():     # 回傳所有動作
            if finish_event.type == pygame.QUIT:    # 如果按下X ,pygame.QUIT 是按下X後的型態
                running = False             # 跳出迴圈
                game = False
                rule_run = False
        if not pygame.mouse.get_pressed()[0]:
            relax = True
        if relax and pygame.mouse.get_pressed()[0]:
            click = True
        if click and not pygame.mouse.get_pressed()[0]:
            rule_run = False
        screen.fill(BLACK)
        start.animation()
        screen.blit(rule.big_image, (0, 0))
        screen.blit(start.image, (830, 200))
        pygame.display.update()                      # 更新畫面=pygame.display.flip()更新全部，update可以有參數
    rule.__init__()
    time.sleep(0.2)


locate_text = ListText()
rule = Rule()
all_sprites.add(rule)
moon = Moon()
bat = Bat()
each_button_click = False
need_list = [2, 10, 14]
game = True
index = 0
first_run = True
while game:
    # initial_game()
    # set origin
    moon.__init__()
    each_button_click = False
    index = 0
    running = True
    for which_message in which_error:
        which_error[which_message][1] = False
    # create sprites
    add5 = Button((WIDTH*3/4-150, HEIGHT*5/6+50), button_5)
    add7 = Button((WIDTH*3/4, HEIGHT*5/6+50), button_7)
    Sqrt = Button((WIDTH*3/4+150, HEIGHT*5/6+50), button_sqrt)
    all_sprites.add(add5)
    all_sprites.add(add7)
    all_sprites.add(Sqrt)
    try_again = Tryagain()
    all_sprites.add(try_again)
    if first_run:
        show_rule()
        first_run = False
    # 遊戲迴圈
    while running and index < 3:
        clock.tick(FPS)                     # 一秒最多刷新FPS次(1秒跑最多幾次while)
        screen.fill(BLACK)
        screen.blit(moon.image, moon.rect.center)
        screen.blit(locate_text.background, locate_text.rect)
        all_sprites.draw(screen)
        screen.blit(bat.image, bat.rect.center)
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
        pygame.display.flip()                      # 更新畫面=pygame.display.flip()更新全部，update可以有參數
    if game:
        if index < 3:
            if try_again.force_click:
                try_again_func()
            try_again.kill()
            add5.kill()
            add7.kill()
            Sqrt.kill()
            locate_text.__init__()
        else:
            finish_func()
            try_again.kill()
            add5.kill()
            add7.kill()
            Sqrt.kill()
pygame.quit()
