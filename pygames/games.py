import pygame,sys


class TankMain(object):
    def startGame(self):
        pygame.display.set_mode((600,500), 0, 32)
        pygame.display.set_caption("坦克大战")


    def stopGame(self):
        sys.exit()


if __name__ == '__main__':
    game = TankMain()
    game.startGame()