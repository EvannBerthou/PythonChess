import pygame
from pygame.locals import *
from Board import Board
from UI import UI

class Game:
    def __init__(self):
        pygame.init()
        self.w, self.h = 1000,800
        self.win = pygame.display.set_mode((self.w, self.h))
        self.board = Board(5,5,790,790, self)
        self.ui = UI(800,5,195,790)
        self.ui.create_panel(self)
        self.mouse_position = (0,0)
        self.mouse_button_down = False

    def run(self):
        clock = pygame.time.Clock()
        while True:
            dt = clock.tick(30)
            self.board.elapsedTime += dt / 1000
            self.mouse_position = pygame.mouse.get_pos()
            self.mouse_button_down = False

            self.win.fill((150,150,150))
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    quit()

                if event.type == MOUSEBUTTONDOWN:

                    self.mouse_button_down = True

                    if self.board.HasPieceMouse(self.mouse_position[0], self.mouse_position[1]):
                        self.board.GetPieceMouse(self.mouse_position[0], self.mouse_position[1])
                    else:
                        self.board.UnselectCase()

            self.board.draw()
            self.ui.draw(self)
            pygame.display.update()

game = Game()
game.run()


"""
TODO:
    Non support du Rock
"""
