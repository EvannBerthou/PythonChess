import pygame
import time

class UI:
    def last_zone(self):
        return self.zones[self.last_zone_name]

    def add_zone(self,title,name):
        new_y = self.last_zone().y + self.last_zone().get_height() + title.get_height() / 2 if len(self.zones) else 5
        z = Zone(self.x, new_y, title)
        self.zones.update( { name : z })
        self.last_zone_name = name

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

        self.add_zone(self.titleFont.render("Chess", 1, (15,15,15)), "Turn")

        text = "Turn: {}".format("White" if game.board.playingTeam else "Black")
        turn = self.turnFont.render(text, 1, (15,15,15))
        self.zones["Turn"].add_info_text(turn)

        self.add_zone(self.titleFont.render("Score", 1, (15,15,15)), "Score")

        text = "White: {}".format(game.board.whiteScore)
        scoreWhite = self.turnFont.render(text, 1, (15,15,15))
        self.zones["Score"].add_info_text(scoreWhite)

        text = "Black: {}".format(game.board.blackScore)
        scoreBlack = self.turnFont.render(text, 1, (15,15,15))
        self.zones["Score"].add_info_text(scoreBlack)

        self.add_zone(self.titleFont.render("Time", 1, (15,15,15)), "Time")

        text = "{}".format(time.strftime('%M:%S', time.gmtime(game.board.elapsedTime)))
        elapsedTime = self.timeFont.render(text, 1, (15,15,15))
        self.zones["Time"].add_info_text(elapsedTime)

        self.add_zone(self.titleFont.render("Last Moves", 1, (15,15,15)), "Last Moves")

    def draw(self,game):
        pygame.draw.rect(game.win, (200,200,200), (self.x, self.y, self.w, self.h)) #BACKGROUND

        for k,v in self.zones.items(): v.draw(game)
        if game.board.player_in_panel:
            pygame.draw.rect(game.win, (255,255,255), (self.panel.x, self.panel.y, self.panel.w, self.panel.h))
            [btn.draw(game) for btn in self.panel_buttons]

    def add_last_move(self, game,msg):
        if len(self.zones["Last Moves"].info_texts) >= game.board.max_last_moves: self.zones["Last Moves"].remove(0)
        text = msg.msg
        msg = self.turnFont.render(text, 1, (255,255,255) if msg.team else (15,15,15))
        self.zones["Last Moves"].add_info_text(msg)

    def __init__(self, x,y,w,h):
        self.x, self.y, self.w, self.h = x,y,w,h
        self.titleFont = pygame.font.SysFont("Arial", 22)
        self.turnFont = pygame.font.SysFont("Arial", 18)
        self.timeFont = pygame.font.SysFont("Arial", 28)
        self.panel = None
        self.panel_buttons = []
        self.zones = {}
        self.last_zone_name = ""

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


class Zone:
    def __init__(self, x,y,title):
        self.x, self.y = x,y
        self.title = title
        self.info_texts = []
        self.y_offset = 5
        self.bar_offset = 5

    def draw(self, game):
        game.win.blit(self.title, (self.x + game.ui.w / 2- self.title.get_width() / 2, self.y))
        for t in self.info_texts: t.draw(game)
        self.draw_bar(game)

    def add_info_text(self, text):
        last_y = self.info_texts[-1].y if len(self.info_texts) else self.y
        text_offset = self.info_texts[-1].get_height() if len(self.info_texts) else self.title.get_height()
        next_y = last_y + self.y_offset + text_offset
        info_t = info_text(self.x,next_y,text)
        self.info_texts.append(info_t)

    def get_height(self):
        total = self.title.get_height()
        for i in self.info_texts:
            total += i.text.get_height() + self.y_offset
        return (total + self.bar_offset + 2)
    
    def draw_bar(self, game):
        pygame.draw.line(game.win, (15,15,15), (self.x, self.y + self.get_height() + self.bar_offset),(self.x + game.ui.w, self.y + self.get_height() + self.bar_offset), 2)

    def remove(self, id):
        sy = self.info_texts[id].get_height()
        for i in self.info_texts:
            i.y -= (sy + self.y_offset)
        del self.info_texts[id]


class info_text:
    def __init__(self, x,y,text):
        self.x, self.y = x,y
        self.text = text
            
    def draw(self, game):
        game.win.blit(self.text, (self.x, self.y))

    def get_height(self):
        return self.text.get_height()

    def update_text(self, font, text):
        self.text = font.render(text, 1, (15,15,15))
