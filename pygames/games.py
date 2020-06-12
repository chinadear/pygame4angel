import time
from builtins import range
from random import randint

import pygame
import sys
from pygame.locals import *


# 游戏主界面
class TankMain(object):
    width = 600
    height = 500
    enamy_list = pygame.sprite.Group()
    my_missibles = []
    boom_list = []
    enamy_num = 20
    def start_game(self):
        # 初始化，加载系统资源
        pygame.init()
        # 绘制界面，返回surface对象
        screen = pygame.display.set_mode((TankMain.width, TankMain.height), 0, 32)
        my_tank = MyTank(screen, 275, 400)

        for i in range(1, TankMain.enamy_num):
            TankMain.enamy_list.add(EnamyTank(screen))
        pygame.display.set_caption("坦克大战")
        # 刷新渲染动作
        while True:
            screen.fill((0, 0, 0))
            for i, text in enumerate(self.write_text(), 0):
                screen.blit(text, (0, 5+(15*i)))
            self.get_event(my_tank)

            my_tank.show()
            my_tank.move()

            for enamy in TankMain.enamy_list:
                if enamy.live:
                    enamy.show()
                    enamy.radom_move()
                else:
                    TankMain.enamy_list.remove(enamy)

            for m in TankMain.my_missibles:
                if m.live:
                    m.show()
                    m.hit_tank()
                    m.move()
                else:
                    TankMain.my_missibles.remove(m)

            for b in TankMain.boom_list:
                b.show()
            #显示重置
            # time.sleep(0.05) # 刷新率
            pygame.display.update()

    def get_event(self, my_tank):
        for event in pygame.event.get():
            if event.type == QUIT:
                self.stop_game()
            if event.type == KEYDOWN:
                if event.key == K_LEFT:
                    my_tank.direction = "L"
                    my_tank.stop = False
                    # my_tank.move()
                if event.key == K_RIGHT:
                    my_tank.direction = "R"
                    my_tank.stop = False
                    # my_tank.move()
                if event.key == K_UP:
                    my_tank.direction = "U"
                    my_tank.stop = False
                    # my_tank.move()
                if event.key == K_DOWN:
                    my_tank.direction = "D"
                    my_tank.stop = False
                    # my_tank.move()
                if event.key == K_ESCAPE:
                    self.stop_game()
                if event.key == K_SPACE:
                    m = my_tank.fire()
                    m.good = True
                    TankMain.my_missibles.append(m)
            if event.type == KEYUP:
                if event.key == K_LEFT:
                    if my_tank.direction == "L":
                        my_tank.stop = True
                elif event.key == K_RIGHT:
                    if my_tank.direction == "R":
                        my_tank.stop = True
                elif event.key == K_UP:
                    if my_tank.direction == "U":
                        my_tank.stop = True
                elif event.key == K_DOWN:
                    if my_tank.direction == "D":
                        my_tank.stop = True

    def stop_game(self):
        sys.exit()

    # 在界面中写字
    def write_text(self):
        # 定义一个字体思源黑体cnbold
        font = pygame.font.SysFont("思源黑体cnbold", 15)
        # 绘制文字
        text1 = font.render("敌方数量：{}".format(TankMain.enamy_list.__len__()), True, (255, 0, 0))
        text2 = font.render("炮弹数量：{}".format(TankMain.my_missibles.__len__()), True, (255, 0, 0))
        return text1, text2


class BaseItem(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

    def show(self):
        if self.live:
            self.image = self.images[self.direction]
            self.screen.blit(self.image, self.rect)


class Tank(BaseItem):
    width = 50
    height = 50

    def __init__(self, screen, left, top, images):
        self.screen = screen
        super().__init__()
        self.direction = "D"
        self.speed = 5
        self.images = images
        self.image = self.images[self.direction]
        self.rect = self.image.get_rect()
        self.rect.left = left
        self.rect.top = top

        self.live = True  # 坦克存活状态

    def move(self):
        if not self.stop:
            if self.direction == "L":
                if self.rect.left > 0:
                    self.rect.left -= self.speed
                else:
                    self.rect.left = 0
            elif self.direction == "R":
                if self.rect.right < TankMain.width:
                    self.rect.right += self.speed
            elif self.direction == "U":
                if self.rect.top > 0:
                    self.rect.top -= self.speed
                else:
                    self.rect.top = 0
            elif self.direction == "D":
                if self.rect.bottom < TankMain.height:
                    self.rect.bottom += self.speed

    def fire(self):
        m = Missibl(self.screen, self)
        return m


class MyTank(Tank):
    def __init__(self, screen, left, top):
        self.images = {"L": pygame.image.load(r"images/mytank_l.png"),
                       "R": pygame.image.load(r"images/mytank_r.png"),
                       "D": pygame.image.load(r"images/mytank_d.png"),
                       "U": pygame.image.load(r"images/mytank_u.png")}
        super().__init__(screen, left, top, self.images)
        self.stop = True


class EnamyTank(Tank):
    def __init__(self, screen):
        self.images = {"L": pygame.image.load(r"images/tank_l.png"),
                       "R": pygame.image.load(r"images/tank_r.png"),
                       "D": pygame.image.load(r"images/tank_d.png"),
                       "U": pygame.image.load(r"images/tank_u.png")}
        super().__init__(screen, randint(1, 5)*100, 200, self.images)
        self.stop = True
        self.step = 15

    def random_direction(self):
        r = randint(0, 3)
        if r == 3:
            self.direction = "L"
            self.stop = False
        elif r == 2:
            self.direction = "R"
            self.stop = False
        elif r == 1:
            self.direction = "U"
            self.stop = False
        elif r == 0:
            self.direction = "D"
            self.stop = False

    def radom_move(self):
        if self.live:
            if self.step == 0:
                self.random_direction()
                self.move()
                self.step = 15
            else:
                self.move()
                self.step -= 1


class Missibl(BaseItem):
    width = 20
    height = 20

    def __init__(self, screen, tank):
        self.screen = screen
        self.tank = tank
        super().__init__()
        self.images = {"L": pygame.image.load(r"images/padan_l.png"),
                       "R": pygame.image.load(r"images/padan_r.png"),
                       "D": pygame.image.load(r"images/padan_d.png"),
                       "U": pygame.image.load(r"images/padan_u.png")}
        self.direction = tank.direction
        self.speed = 12
        self.image = self.images[self.direction]
        self.rect = self.image.get_rect()
        self.rect.left = tank.rect.left + (tank.width - self.width)/2
        self.rect.top = tank.rect.top + (tank.width - self.width)/2

        self.live = True  # 炮弹存活状态
        self.good = False

    def move(self):
        if self.live:
            if self.direction == "L":
                if self.rect.left > 0:
                    self.rect.left -= self.speed
                else:
                    self.live = False
            elif self.direction == "R":
                if self.rect.right < TankMain.width:
                    self.rect.right += self.speed
                else:
                    self.live = False
            elif self.direction == "U":
                if self.rect.top > 0:
                    self.rect.top -= self.speed
                else:
                    self.live = False
            elif self.direction == "D":
                if self.rect.bottom < TankMain.height:
                    self.rect.bottom += self.speed
                else:
                    self.live = False

    def hit_tank(self):
        if self.good:
            hit_list = pygame.sprite.spritecollide(self, TankMain.enamy_list, False)
            for e in hit_list:
                e.live = False
                self.live = False
                boom = Boom(self.screen, e.rect)
                TankMain.boom_list.append(boom)


class Boom(BaseItem):

    def __init__(self, screen, rect):
        super().__init__()
        self.screen = screen
        self.live = True
        self.images = [pygame.image.load(r"images/boom20.png"),
                       pygame.image.load(r"images/boom40.png"),
                       pygame.image.load(r"images/boom60.png"),
                       pygame.image.load(r"images/boom70.png")]
        self.step = 0
        self.rect = rect

    def show(self):
        if self.live:
            if self.step == len(self.images):
                self.live = False
            else:
                self.image = self.images[self.step]
                self.screen.blit(self.image, self.rect)
                self.step += 1
        else:
            pass


if __name__ == '__main__':
    game = TankMain()
    game.start_game()
