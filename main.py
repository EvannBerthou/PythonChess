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
                    if self.board.HasPieceMouse(self.mouse_position[0], self.mouse_position[1]):
                        self.board.GetPieceMouse(self.mouse_position[0], self.mouse_position[1])
                    else:
                        self.board.UnselectCase()

                if event.type == MOUSEBUTTONDOWN:
                    self.mouse_button_down = True

            self.board.draw(self)
            self.ui.draw(self)
            pygame.display.update()

game = Game()
game.run()


"""
TODO:
    Non support du Rock

    La partie ne se termine jamais:
        A la fin d'un tour, vérifier pour toute les pièces du joueur adverse si elle peut manger le roi:
            Si oui:
                Désactiver le mouvement des pièces qui ne permettent pas le roi de sortir de l'échec 
                Pour toutes les cases autour du roi en échec, vérifier si le roi se fait toujours manger sur cette case:
                    Si oui:
                        Si toutes les cases ne permettent pas au roi de bouger:
                            Échec et mat
                    Si non:
                        Ajouter cette case aux cases possibles dans le mouvement
            Si non: 
                ne rien faire
"""
