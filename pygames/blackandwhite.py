import pygame
import sys
from pygame.locals import *
from random import randint


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
    # 采用[0]]*n 的方式创建数组，仅仅是创建n个指向[0]的指针，也就是这n个列表指向同一个，修改一个其他均修改
    # map2 = [[0]*num]*num
    def start_game(self):
        # 初始化，加载系统资源
        pygame.init()
        # 绘制界面，返回surface对象
        screen = pygame.display.set_mode((Main.width, Main.height), 0, 32)
        pygame.display.set_caption("黑白迭代")
        self.init_map()
        while True:
            screen.fill((0, 0, 0))
            # screen.blit(self.write_text(), (5, 5))

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
                if event.key == K_SPACE:
                    Main.map = Main.map1
            if event.type == KEYUP:
                if event.key == K_SPACE:
                    Main.map = Main.map2

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


    def write_text(self):
        # 定义一个字体思源黑体cnbold
        font = pygame.font.SysFont("思源黑体cnbold", 15)  # 华文宋体
        # 绘制文字
        text = font.render("鼠标位置{}:{}".format(1,1), True, (255, 0, 0))
        return text


if __name__ == '__main__':
    game = Main()
    game.start_game()