import pygame
import sys
from pygame.locals import *


class TankMain(object):
    width = 600
    height = 500
    def start_game(self):
        # 初始化，加载系统资源
        pygame.init()
        # 绘制界面，返回surface对象
        screen = pygame.display.set_mode((TankMain.width, TankMain.height), 0, 32)
        my_tank = MyTank(screen, 275, 400)
        pygame.display.set_caption("坦克大战")
        while True:
            screen.fill((0, 0, 0))
            screen.blit(self.write_text(), (0, 5))
            self.get_event(my_tank)

            my_tank.showTank()
            #显示重置
            pygame.display.update()

    def get_event(self, my_tank):
        for event in pygame.event.get():
            if event.type == QUIT:
                self.stop_game()
            if event.type == KEYDOWN:
                if event.key == K_LEFT:
                    my_tank.direction = "L"
                    my_tank.move()
                if event.key == K_RIGHT:
                    my_tank.direction = "R"
                    my_tank.move()
                if event.key == K_UP:
                    my_tank.direction = "U"
                    my_tank.move()
                if event.key == K_DOWN:
                    my_tank.direction = "D"
                    my_tank.move()
                if event.key == K_ESCAPE:
                    self.stop_game()

    def stop_game(self):
        sys.exit()

    # 在界面中写字
    def write_text(self):
        # 定义一个字体思源黑体cnbold
        font = pygame.font.SysFont("思源黑体cnbold", 15)
        # 绘制文字
        text = font.render("敌方数量：{}".format(5), True, (255, 0, 0))
        return text


class BaseItem(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)


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

    def showTank(self):
        self.image = self.images[self.direction]
        self.screen.blit(self.image, self.rect)

    def move(self):
        pass

    def fire(self):
        pass


class MyTank(Tank):
    def __init__(self, screen, left, top):
        self.images = {"L": pygame.image.load(r"images/mytank_l.png"),
                       "R": pygame.image.load(r"images/mytank_r.png"),
                       "D": pygame.image.load(r"images/mytank_d.png"),
                       "U": pygame.image.load(r"images/mytank_u.png")}
        super().__init__(screen, left, top, self.images)

    def move(self):
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



if __name__ == '__main__':
    game = TankMain()
    game.start_game()
