import pygame
import time

class UI:
    def __init__(self, x,y,w,h):
        self.x, self.y, self.w, self.h = x,y,w,h
        self.titleFont = pygame.font.SysFont("Arial", 22)
        self.turnFont = pygame.font.SysFont("Arial", 18)
        self.timeFont = pygame.font.SysFont("Arial", 28)
    
    def draw(self,game):
        pygame.draw.rect(game.win, (200,200,200), (self.x, self.y, self.w, self.h))

        text = "Chess"
        title = self.titleFont.render(text, 1, (15,15,15))
        sx,sy = self.titleFont.size(text)
        game.win.blit(title, (self.x + self.w / 2 - sx / 2, self.y))

        text = "Turn: {}".format("White" if game.board.playingTeam else "Black")
        turn = self.turnFont.render(text, 1, (15,15,15))
        sx,sy = self.titleFont.size(text)
        game.win.blit(turn, (self.x, self.y + 2 * sy))

        #BAR
        pygame.draw.line(game.win, (15,15,15), (self.x, 120),(self.x + self.w, 120), 2)

        text = "Score"
        score = self.titleFont.render(text, 1, (15,15,15))
        sx,sy = self.titleFont.size(text)
        game.win.blit(score, (self.x + self.w / 2 - sx / 2, 125))

        text = "White: {}".format(game.board.whiteScore)
        scoreWhite = self.turnFont.render(text, 1, (15,15,15))
        sx,sy = self.titleFont.size(text)
        game.win.blit(scoreWhite, (self.x, 120 + 2 * sy))

        text = "Black: {}".format(game.board.blackScore)
        scoreBlack = self.turnFont.render(text, 1, (15,15,15))
        sx,sy = self.titleFont.size(text)
        game.win.blit(scoreBlack, (self.x, 143 + 2 * sy))

        #BAR
        pygame.draw.line(game.win, (15,15,15), (self.x, 250),(self.x + self.w, 250), 2)

        text = "Temps"
        temps = self.titleFont.render(text, 1, (15,15,15))
        sx,sy = self.titleFont.size(text)
        game.win.blit(temps, (self.x + self.w / 2 - sx / 2, 255))

        text = "{}".format(time.strftime('%M:%S', time.gmtime(game.board.elapsedTime)))
        elapsedTime = self.timeFont.render(text, 1, (15,15,15))
        sx,sy = self.timeFont.size(text)
        game.win.blit(elapsedTime, (self.x + self.w / 2 - sx / 2, 290))
