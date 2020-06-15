import pygame
import sys
from pygame.locals import *
from random import randint
import numpy as np


class Main(object):
    width = 600
    height = 600
    # 画布大小10*10
    num = 10
    # 目标图形块个数
    tm = 20
    # 目标图形矩阵
    map1 = [[0 for i in range(10)] for j in range(10)]
    # 当前图形矩阵
    map2 = [[0 for i in range(10)] for j in range(10)]
    map = map2
    result = False
    result_text = "黑白迭代"
    # 采用[0]]*n 的方式创建数组，仅仅是创建n个指向[0]的指针，也就是这n个列表指向同一个，修改一个其他均修改
    # map2 = [[0]*num]*num
    def start_game(self):
        # 初始化，加载系统资源
        pygame.init()
        # 绘制界面，返回surface对象
        screen = pygame.display.set_mode((Main.width, Main.height), 0, 32)
        pygame.display.set_caption(Main.result_text)
        self.init_map()
        while True:
            screen.fill((0, 0, 0))
            # screen.blit(self.write_text(), (5, 5))

            Main.draw_map(self, screen, Main.map)
            if Main.result:
                pygame.display.set_caption(Main.result_text)
                Main.result = False
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
                pygame.display.set_caption("黑白迭代")
                if event.key == K_SPACE:
                    Main.map = Main.map1
                if event.key == K_1:
                    Main.tm = 1
                    self.init_map()
                if event.key == K_2:
                    Main.tm = 10
                    self.init_map()
                if event.key == K_3:
                    Main.tm = 15
                    self.init_map()
                if event.key == K_4:
                    Main.tm = 20
                    self.init_map()

            if event.type == KEYUP:
                if event.key == K_SPACE:
                    Main.map = Main.map2
                if event.key == K_r:
                    self.result_compare()

    def draw_map(self, screen, map):
        for i in range(Main.num):
            for j in range(Main.num):
                pygame.draw.rect(screen, (255, 255, 255), [i * 60, j * 60, 59, 59], map[i][j])

    def deal_mousedown(self, p):
        x = p[0]//60
        y = p[1]//60
        Main.map2[x][y] = 0 if Main.map2[x][y] == 1 else 1
        if x-1 >= 0:
            Main.map2[x-1][y] = 0 if Main.map2[x-1][y] == 1 else 1
        if x+1 <= 9:
            Main.map2[x+1][y] = 0 if Main.map2[x+1][y] == 1 else 1
        if y-1 >= 0:
            Main.map2[x][y-1] = 0 if Main.map2[x][y-1] == 1 else 1
        if y+1 <= 9:
            Main.map2[x][y+1] = 0 if Main.map2[x][y+1] == 1 else 1

    def init_map(self):
        for i in range(Main.num):
            for j in range(Main.num):
                Main.map1[i][j] = 0
                Main.map2[i][j] = 0
        # 初始化目标图形矩阵
        for a in range(Main.tm):
            x = randint(0, 4)
            y = randint(0, 9)
            Main.map1[x][y] = 1
            Main.map1[Main.num-1-x][y] = 1

    def result_compare(self):
        a = np.array(Main.map1)
        b = np.array(Main.map2)
        if (a == b).all():
            Main.result_text = "胜利！安琪宝宝真聪明"
        else:
            Main.result_text = "还没有成功，再坚持一下！"
        Main.result = True

    def write_text(self, t):
        # 定义一个字体思源黑体cnbold
        font = pygame.font.SysFont("arial", 65)  # 华文宋体
        # 绘制文字
        # text = font.render("鼠标位置{}:{}".format(1,1), True, (255, 0, 0))
        text = font.render(t, True, (255, 0, 0))
        return text



if __name__ == '__main__':
    game = Main()
    game.start_game()