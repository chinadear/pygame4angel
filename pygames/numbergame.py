import os

import pygame
import sys
from pygame.locals import *
from random import randint


class Main(object):
    width = 800
    height = 400
    map = [[0 for i in range(20)] for j in range(5)]
    map_num = [[0 for i in range(20)] for j in range(5)]
    tips_text = ""
    tips_text2 = ""
    click_num = 3
    target_num = randint(1, 100)
    image1 = pygame.image.load(r"ngame/timg.png")  # 隐藏
    image2 = pygame.image.load(r"ngame/2.png")      # 展示
    image = image1
    result = 0  # 0进行中，1成功,2失败

    def start_game(self):
        # 初始化，加载系统资源
        pygame.init()
        # 绘制界面，返回surface对象
        screen = pygame.display.set_mode((Main.width, Main.height), 0, 32)
        pygame.display.set_caption("数字侦探")
        self.init_map()
        self.auto_tips()
        while True:
            screen.fill((0, 0, 0))  # 填充白色
            screen.blit(self.write_text(u"提示信息:" + Main.tips_text, 20), (10, 130))
            if Main.tips_text2 != "":
                screen.blit(self.write_text(u"提示信息:" + Main.tips_text2, 20), (10, 150))
            screen.blit(self.write_text(u"剩余次数:" + str(Main.click_num), 24), (10, 10))
            self.show_image(screen, Main.image)
            if Main.result > 0:
                if Main.target_num > 10:
                    screen.blit(self.write_text(str(Main.target_num), 32), (385, 23))
                else:
                    screen.blit(self.write_text(str(Main.target_num), 32), (392, 23))
                if Main.result == 1:
                    screen.blit(self.write_text("胜利", 48), (500, 10))
                else:
                    screen.blit(self.write_text("失败", 48), (500, 10))
            Main.draw_map(self, screen, Main.map)

            self.get_event()
            pygame.time.Clock().tick(50)
            pygame.display.update()

    def get_event(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                if pygame.mouse.get_focused():
                    p = pygame.mouse.get_pos()
                    self.deal_mousedown(p)
            if event.type == KEYDOWN:
                if event.key == K_1:
                    self.restart()
                if event.key == K_2:
                    self.tips_too()

    def init_map(self):
        for i in range(5):
            for j in range(20):
                Main.map[i][j] = 0
                Main.map_num[i][j] = i*20+j+1

    def restart(self):
        self.init_map()
        Main.target_num = randint(1, 100)
        Main.click_num = 3
        Main.result = 0
        Main.image = Main.image1
        pygame.display.set_caption("数字侦探")
        self.auto_tips()
        Main.tips_text2 = ""

    def auto_tips(self):
        # 奇偶校验
        Main.tips_text = "这个数是一个{}".format("偶数" if Main.target_num%2 == 0 else "奇数")
        Main.tips_text += ",在10以内的数中，它只可以被"
        l = []
        # 整除校验
        for m in range(1,10):
            if Main.target_num%m == 0:
                l.append(m)
        Main.tips_text += l.__str__()+"整除"

    def tips_too(self):
        if Main.target_num > 9:
            Main.tips_text2 += "它是一个两位数,"
            s = str(Main.target_num)
            i1 = 0 if int(s[0])%2 == 0 else 1
            i2 = 0 if int(s[1])%2 == 0 else 1
            i = i1+i2
            if i == 0:
                Main.tips_text2 += "并且两个位数都是偶数"
            elif i == 1:
                Main.tips_text2 += "并且两个位数一奇一偶"
            elif i == 2:
                Main.tips_text2 += "并且两个位数都是奇数"
        else:
            Main.tips_text2 += "它小于10"

    def num2flag(self, num):
        x = 0
        y = 0
        if num%20 == 0:
            x = num//20-1
            y = 19
        else:
            x = num//20
            y = num%20 -1
        Main.map[x][y] = 1

    def draw_map(self, screen, map):
        for i in range(5):  # range=0开始，5-1结束
            for j in range(20):
                # rect=[left, top, width, height]
                pygame.draw.rect(screen, (255, 255, 255), [j * 40, i * 40+200, 39, 39], map[i][j])
                # 在图形上绘制数字
                screen.blit(self.write_text(str(Main.map_num[i][j]), 20), (j * 40+5, i * 40+200+5,))

    def deal_mousedown(self, p):
        if p[1] >= 200:  # 点击在下方数字格范围内有效，否则无效点击
            if Main.click_num > 0:
                Main.click_num -= 1
                x = p[0]//40
                y = p[1]//40-5
                n = Main.map_num[y][x]
                if Main.target_num > n:
                    for m in range(1, n+1):
                        self.num2flag(m)
                elif Main.target_num < n:
                    for m in range(n, 101):
                        self.num2flag(m)
                else:  # Main.target_num == n 则成功
                    Main.map[y][x] = 1
                    Main.result = 1
                    Main.image = Main.image2
                    pygame.display.set_caption("胜利,找到了正确的数字{}".format(Main.target_num))
                if Main.click_num == 0 and Main.result != 1:
                    pygame.display.set_caption("失败了,机会已经用完，没有找到正确的数字{}".format(Main.target_num))
                    Main.image = Main.image2
                    Main.result = 2
            else:
                pygame.display.set_caption("失败了,机会已经用完，没有找到正确的数字{}".format(Main.target_num))
                Main.image = Main.image2
                Main.result = 2
        else:
            pass

    def write_text(self, t, size):
        # 定义一个字体思源黑体cnbold
        # font = pygame.font.SysFont("黑体", 65)  # 华文宋体
        # 绘制文字
        pygame.font.init()
        font = pygame.font.Font(r"ngame/simheittf.ttf", size)
        # text = font.render("鼠标位置{}:{}".format(1,1), True, (255, 0, 0))
        text = font.render(t, True, (125, 125, 0))
        return text

    def show_image(self, screen, image):
        rect = image.get_rect()
        rect.left = 370
        rect.top = 10
        screen.blit(image, rect)


if __name__ == '__main__':
    game = Main()
    game.start_game()
