import pygame
from pygame.locals import *
from Board import Board
from UI import UI

class Game:
    def __init__(self):
        pygame.init()
        self.w, self.h = 1000,800
        self.win = pygame.display.set_mode((self.w, self.h))
        self.board = Board(5,5,790,790)
        self.ui = UI(800,5,195,790)

    def run(self):
        clock = pygame.time.Clock()
        while True:
            dt = clock.tick(30)
            self.board.elapsedTime += dt / 1000
            mousePosition = pygame.mouse.get_pos()

            self.win.fill((150,150,150))
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    quit()

                if event.type == MOUSEBUTTONDOWN:
                    if self.board.HasPieceMouse(mousePosition[0], mousePosition[1]):
                        self.board.GetPieceMouse(mousePosition[0], mousePosition[1])
                    else:
                        self.board.UnselectCase()

            self.board.draw(self)
            self.ui.draw(self)
            pygame.display.update()

game = Game()
game.run()


"""
TODO:
    Non support du Rock
    La partie ne se termine jamais
"""
