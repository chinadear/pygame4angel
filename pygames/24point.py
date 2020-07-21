import pygame
import sys
from pygame.locals import *
import random
import time
import copy
import json


class Main(object):
    width = 600
    height = 600
    # 分数
    score = 0
    # 4个数字
    nums = []
    # 加减乘除符号
    flag = ['p', 'j', 'x', 'c']
    # 已选数字，放在下放
    save = None
    # 已选符号
    save_flag = None
    # 备份本局数字，用于重置
    nums_bak = []
    # 是否显示成功图片
    success = False
    # 是否显示失败图片
    fail = False
    background = pygame.image.load(r"images/background.png")
    # 首页 500*375
    mainpage = pygame.image.load(r"images/mainpage.png")
    # 计时器，时间限制
    time_count = 10
    time_count_bak = 0
    # 当前时间
    current_time = 0
    # 开始计时
    startflag = False
    # 由于利用pygame.time.get_ticks() 获得了从启动pygame就开始连续计时的计时器，这个时间是连续不间断的
    # 所以记录开始的时间，用连续时间减去基础的开始时间，从而实现从0计时
    # 记录当前计时器时间，作为基础时间
    sch1 = 0
    # 持久化数据
    load_data = {}

    def start_game(self):
        # 初始化，加载系统资源
        pygame.init()
        # 绘制界面，返回surface对象
        screen = pygame.display.set_mode((Main.width, Main.height), 0, 32)
        # 显示标题
        pygame.display.set_caption("24点(说明：胜利一局加1分，换一局减1分)")
        self.init_play()
        self.read_data()
        while True:
            # screen.fill((0, 0, 0))
            screen.blit(self.background, (0, 0))
            if self.startflag:  # startflag 为True游戏开始
                for i, text in enumerate(self.write_text(), 0):
                    screen.blit(text, (15, 5 + (15 * i)))
                # 退出 100*40
                exit = Digital("exit", 10, 300, screen)
                exit.show()
                # 重新开始
                restart = Digital("restart", 10, 400, screen)
                restart.show()
                # 换一局
                flush = Digital("flush", 10, 500, screen)
                flush.show()
                for ind, n in enumerate(self.nums):
                    # 5=125；4=160；3=195；2=230；1=265  /均差35
                    d = Digital(n, 100, (5-len(self.nums))*35+125 + 70 * ind, screen)
                    d.show()
                for ind, n in enumerate(self.flag):
                    f = Digital(n, 295, 210+45*ind, screen)
                    f.show()
                store = Digital(self.save, 440, 250, screen)
                store.show()
                store_flag = Digital(self.save_flag, 465, 320, screen)
                store_flag.show()

                if self.current_time == self.time_count:
                    self.startflag = False
                if self.success:
                    succ = Digital("success", 150, 100, screen)
                    succ.show()
                    pygame.display.update()
                    self.flush()
                    time.sleep(1)
                    self.success = False
                if self.fail:
                    fai = Digital("fail", 150, 200, screen)
                    fai.show()
                    pygame.display.update()
                    self.flush()
                    time.sleep(1)
                    self.fail = False
            else:
                screen.blit(self.mainpage, (50, 112))
                for i, text in enumerate(self.write_main(), 0):
                    if i == 0:
                        screen.blit(text, (173, 135))
                    else:
                        screen.blit(text, (173, 176))
                self.deal_data()
            self.get_event()
            pygame.time.Clock().tick(40)
            pygame.display.update()

    def get_event(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                if pygame.mouse.get_focused():
                    p = pygame.mouse.get_pos()
                    self.onclick(p)
            if event.type == KEYDOWN:
                if event.key == K_SPACE:
                    pass
            if event.type == KEYUP:
                if event.key == K_SPACE:
                    pass

    def init_play(self):
        self.nums = random.sample(['1', '2', '3', '4', '5', '6', '7', '8', '9'], 4)
        self.nums_bak = self.nums.copy()

    def flush(self):
        self.init_play()
        self.save = None
        self.save_flag = None

    def restart(self):
        self.nums = self.nums_bak.copy()
        self.save = None
        self.save_flag = None

    def write_text(self):
        # 定义一个字体思源黑体cnbold
        font = pygame.font.SysFont("SimHei", 15)
        # 绘制文字
        text = font.render("得分：{}".format(self.score), True, (255, 0, 0))
        if self.startflag:
            self.current_time = pygame.time.get_ticks()//1000-self.sch1
        else:
            self.current_time = 0
        text1 = font.render("倒计时：{}秒".format(self.current_time), True, (255, 0, 0))
        return text, text1

    # 首页的分数展示
    def write_main(self):
        # 定义一个字体思源黑体cnbold
        font = pygame.font.SysFont("SimHei", 15)
        # 绘制文字
        text = font.render("{}分".format(self.load_data["maxScore"]), True, (255, 0, 0))
        text1 = font.render("{}分".format(self.score), True, (255, 0, 0))
        return text, text1

    # 处理分数，计算历史最高分
    def deal_data(self):
        max_score = self.load_data['maxScore']
        if self.score > int(max_score):
            if self.time_count != -1: # 证明不是练习
                self.load_data["maxScore"] = self.score
                self.write_data()

    def onclick(self, p):
        x = p[0]  # left
        y = p[1]  # top
        if self.startflag:
            if 255 > x > 210 and 340 > y > 295:  # 加
                if self.save is not None:
                    self.save_flag = "p"
            elif 300 > x > 255 and 340 > y > 295:  # 减
                if self.save is not None:
                    self.save_flag = "j"
            elif 345 > x > 300 and 340 > y > 295:  # 乘
                if self.save is not None:
                    self.save_flag = "x"
            elif 390 > x > 345 and 340 > y > 295:  # 除
                if self.save is not None:
                    self.save_flag = "c"
            elif 50 > y > 10 and 400 > x > 300:  # 退出
                self.startflag = False
            elif 50 > y > 10 and 500 > x > 400:  # 重新开始
                self.restart()
            elif 50 > y > 10 and 600 > x > 500:  # 换一局
                if self.time_count >= 0:
                    self.score -= 1
                self.flush()

            # 数字点取
            if len(self.nums) == 4:  # ==================================4个数的时候
                if 230 > x > 160 and 195 > y > 100:  # 第1个数
                    self.save = self.nums[0]
                    del self.nums[0]
                elif 300 > x > 230 and 195 > y > 100:  # 第2个数
                    self.save = self.nums[1]
                    del self.nums[1]
                elif 370 > x > 300 and 195 > y > 100:  # 第3个数
                    self.save = self.nums[2]
                    del self.nums[2]
                elif 440 > x > 370 and 195 > y > 100:  # 第4个数
                    self.save = self.nums[3]
                    del self.nums[3]
            elif len(self.nums) == 3:  # ==================================3个数的时候
                if 265 > x > 195 and 195 > y > 100:  # 第1个数
                    if self.save_flag is not None and self.save is not None:
                        r = self.js(int(self.save), int(self.nums[0]), self.save_flag)
                        if r > 0:
                            del self.nums[0]
                            self.nums.append(str(r))
                            self.clear_save()
                    elif self.save is None:
                        self.save = self.nums[0]
                        del self.nums[0]
                    else:  # save is not None and save_flag is None
                        self.nums.append(self.save)
                        self.save = self.nums[0]
                        del self.nums[0]
                elif 335 > x > 265 and 195 > y > 100:  # 第2个数
                    if self.save_flag is not None and self.save is not None:
                        r = self.js(int(self.save), int(self.nums[1]), self.save_flag)
                        if r > 0:
                            del self.nums[1]
                            self.nums.append(str(r))
                            self.clear_save()
                    elif self.save is None:
                        self.save = self.nums[1]
                        del self.nums[1]
                    else:  # save is not None and save_flag is None
                        self.nums.append(self.save)
                        self.save = self.nums[1]
                        del self.nums[1]
                elif 405 > x > 335 and 195 > y > 100:  # 第3个数
                    if self.save_flag is not None and self.save is not None:
                        r = self.js(int(self.save), int(self.nums[2]), self.save_flag)
                        if r > 0:
                            del self.nums[2]
                            self.nums.append(str(r))
                            self.clear_save()
                    elif self.save is None:
                        self.save = self.nums[2]
                        del self.nums[2]
                    else:  # save is not None and save_flag is None
                        self.nums.append(self.save)
                        self.save = self.nums[2]
                        del self.nums[2]
            elif len(self.nums) == 2:  # =====================================2个数的时候
                if 300 > x > 230 and 195 > y > 100:  # 第1个数
                    if self.save_flag is not None and self.save is not None:
                        r = self.js(int(self.save), int(self.nums[0]), self.save_flag)
                        if r > 0:
                            del self.nums[0]
                            self.nums.append(str(r))
                            self.clear_save()
                    elif self.save is None:
                        self.save = self.nums[0]
                        del self.nums[0]
                    else:  # save is not None and save_flag is None
                        self.nums.append(self.save)
                        self.save = self.nums[0]
                        del self.nums[0]
                elif 370 > x > 300 and 195 > y > 100:  # 第2个数
                    if self.save_flag is not None and self.save is not None:
                        r = self.js(int(self.save), int(self.nums[1]), self.save_flag)
                        if r > 0:
                            del self.nums[1]
                            self.nums.append(str(r))
                            self.clear_save()
                    elif self.save is None:
                        self.save = self.nums[1]
                        del self.nums[1]
                    else:  # save is not None and save_flag is None
                        self.nums.append(self.save)
                        self.save = self.nums[1]
                        del self.nums[1]
            elif len(self.nums) == 1:  # =====================================1个数的时候
                if 335 > x > 265 and 195 > y > 100:  # 就1个数
                    if self.save_flag is not None and self.save is not None:
                        r = self.js(int(self.save), int(self.nums[0]), self.save_flag)
                        if r > 0:
                            del self.nums[0]
                            self.nums.append(str(r))
                            self.clear_save()
                            if r != 24:
                                self.fail = True
                    elif self.save is not None and self.save_flag is None:
                        self.nums.append(self.save)
                        self.save = self.nums[0]
                        del self.nums[0]
        else:
            if 382 > x > 230 and 364 > y > 311:  # 开始
                self.startflag = True
                self.sch1 = copy.copy(pygame.time.get_ticks())//1000
                self.time_count = copy.copy(self.time_count_bak)
                self.score = 0
            elif 529 > x > 432 and 162 > y > 122:  # 练习
                self.startflag = True
                self.sch1 = copy.copy(pygame.time.get_ticks()) // 1000
                self.time_count = -1
                self.score = 0

    # 计算，c是符号
    def js(self, a, b, c):
        result = 0
        if c == 'p':
            result = a+b
        elif c == 'j':
            if a-b > 0:
                result = a-b
            else:
                result = -1
        elif c == 'x':
            result = a*b
        elif c == 'c':
            if a % b == 0:
                result = a//b
            else:
                result = -1
        if result == 24:  # 成功后增加分数
            self.success = True
            if self.time_count >= 0:
                self.score += 1
        return result

    # 清楚中间过程缓存
    def clear_save(self):
        self.save_flag = None
        self.save = None

    # 读取数据
    def read_data(self):
        with open("json/data.json", 'r') as load_f:
            self.load_data = json.load(load_f)
            self.time_count = int(self.load_data["time"])
            self.time_count_bak = copy.copy(self.time_count)

    # 写入数据
    def write_data(self):
        with open("json/data.json", "w") as f:
            json.dump(self.load_data, f)


class BaseItem(pygame.sprite.Sprite):
    # 0-1=70*95  +-*/=45*45
    images = {"0": pygame.image.load(r"images/0.png"),
              "1": pygame.image.load(r"images/1.png"),
              "2": pygame.image.load(r"images/2.png"),
              "3": pygame.image.load(r"images/3.png"),
              "4": pygame.image.load(r"images/4.png"),
              "5": pygame.image.load(r"images/5.png"),
              "6": pygame.image.load(r"images/6.png"),
              "7": pygame.image.load(r"images/7.png"),
              "8": pygame.image.load(r"images/8.png"),
              "9": pygame.image.load(r"images/9.png"),
              "0_s": pygame.image.load(r"images/0_s.png"),
              "1_s": pygame.image.load(r"images/1_s.png"),
              "2_s": pygame.image.load(r"images/2_s.png"),
              "3_s": pygame.image.load(r"images/3_s.png"),
              "4_s": pygame.image.load(r"images/4_s.png"),
              "5_s": pygame.image.load(r"images/5_s.png"),
              "6_s": pygame.image.load(r"images/6_s.png"),
              "7_s": pygame.image.load(r"images/7_s.png"),
              "8_s": pygame.image.load(r"images/8_s.png"),
              "9_s": pygame.image.load(r"images/9_s.png"),
              "p": pygame.image.load(r"images/p.png"),
              "j": pygame.image.load(r"images/j.png"),
              "x": pygame.image.load(r"images/x.png"),
              "c": pygame.image.load(r"images/c.png"),
              "d": pygame.image.load(r"images/d.png"),
              "restart": pygame.image.load(r"images/restart.png"),
              "flush": pygame.image.load(r"images/flush.png"),
              "exit": pygame.image.load(r"images/exit.png"),
              "success": pygame.image.load(r"images/success.png"),
              "fail": pygame.image.load(r"images/fail.png")}

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

    def show(self):
        if self.f is None:
            return
        elif self.f != "p" and self.f != "j" and self.f != "x" and self.f != "c" and self.f != "restart"\
                and self.f != "exit" and self.f != "flush" and self.f != "success" and self.f != "fail":
            if int(self.f) > 9:
                for i,s in enumerate(self.f):
                    self.image = self.images[s+"_s"]
                    self.rect = self.image.get_rect()
                    self.rect.left = self.left+(35*i)
                    self.rect.top = self.top
                    self.screen.blit(self.image, self.rect)
            else:
                self.image = self.images[self.f]
                self.rect = self.image.get_rect()
                self.rect.left = self.left
                self.rect.top = self.top
                self.screen.blit(self.image, self.rect)
        else:
            self.image = self.images[self.f]
            self.rect = self.image.get_rect()
            self.rect.left = self.left
            self.rect.top = self.top
            self.screen.blit(self.image, self.rect)


class Digital(BaseItem):
    def __init__(self, f, top, left,screen):
        super().__init__()
        self.f = f
        self.left = left
        self.top = top
        self.screen = screen


if __name__ == '__main__':
    main = Main()
    main.start_game()
