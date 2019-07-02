import pygame
import time

class UI:
    def create_buttons(self, game, team):
        self.panel_buttons.clear()
        cell_size = 150
        for i in range(4):
            id = i + 2 + 10 * (team + 1)
            sprite = game.board.GetPiece(id)(0,0,team).sprite
            self.panel_buttons.append(Button(self.panel.x + i * cell_size + 5, self.panel.y + 5, cell_size,cell_size, sprite, id))

    def create_panel(self, game):
        panel_width, panel_height = 150*4+10, 160
        board_rect = pygame.Rect(5,5, game.board.w, game.board.h)
        panel_rect = pygame.Rect(0,0, panel_width, panel_height)
        panel_rect.center = board_rect.center
        self.panel = panel_rect

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

        #BAR
        pygame.draw.line(game.win, (15,15,15), (self.x, 330),(self.x + self.w, 330), 2)

        text = "Last moves"
        moves = self.titleFont.render(text, 1, (15,15,15))
        sx,sy = self.titleFont.size(text)
        game.win.blit(moves, (self.x + self.w / 2 - sx / 2, 335))

        for i in range(game.board.max_last_moves):
            if i >= len(game.board.last_moves): break
            text = game.board.last_moves[i].msg
            msg = self.turnFont.render(text, 1, (255,255,255) if game.board.last_moves[i].team else (15,15,15))
            sx,sy = self.titleFont.size(text)
            game.win.blit(msg, (self.x, 365 + sy*i))


        if game.board.player_in_panel:
            pygame.draw.rect(game.win, (255,255,255), (self.panel.x, self.panel.y, self.panel.w, self.panel.h))
            [btn.draw(game) for btn in self.panel_buttons]

    def __init__(self, x,y,w,h):
        self.x, self.y, self.w, self.h = x,y,w,h
        self.titleFont = pygame.font.SysFont("Arial", 22)
        self.turnFont = pygame.font.SysFont("Arial", 18)
        self.timeFont = pygame.font.SysFont("Arial", 28)
        self.panel = None
        self.panel_buttons = []

class Button:
    def __init__(self, x,y,w,h,sprite, id):
        self.x,self.y,self.w,self.h = x,y,w,h
        self.sprite = pygame.transform.scale(sprite, (self.w, self.h))
        self.is_hovered = False
        self.id = id

    def set_hovered(self,game):
        self.is_hovered = self.x + self.w > game.mouse_position[0] > self.x and self.y + self.h > game.mouse_position[1] > self.y

    def check_clicked(self, game):
        return self.is_hovered and game.mouse_button_down

    def draw(self, game):
        self.set_hovered(game)
        pygame.draw.rect(game.win, (0,0,0), (self.x,self.y,self.w,self.h), 1) #DRAW BORDER
        if self.is_hovered:
            pygame.draw.rect(game.win, (0,255,0), (self.x + 1, self.y + 1, self.w - 2, self.h - 2))
        game.win.blit(self.sprite, (self.x, self.y))
