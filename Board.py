import pygame
import pdb
from Piece import Piece, Blank, Pawn, Rook, Knight, Bishop, Queen, King
from random import randint

BOARD_CASES = 8

class Board:
    
    def num_let(self, number):
        return ["A","B","C","D","E","F","G","H"][number]

    def GetPiece(self, value):
        if value == 0: return Blank
        Pieces = {
                1:Pawn,
                2:Rook,
                3:Knight,
                4:Bishop,
                5:Queen,
                6:King
        }

        team = value > 20 #SI VALUE > 20 ALORS LA PIECE EST NOIRE, SINON ELLE EST BLANCHE
        if team: value -= 20
        else: value -= 10
        piece = Pieces[value]
        return piece

    def CreateBoard(self):
        board =[[22, 23, 24, 25, 26, 24, 23, 22],
                [21, 21, 21, 21, 21, 21, 21, 21],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [11, 11, 11, 11, 11, 11, 11, 11],
                [12, 13, 14, 15, 16, 14, 13, 12]]

        center = self.cell_size / 2 + 7.5

        b = [[0 for _ in range(BOARD_CASES)] for _ in range(BOARD_CASES)]
        for x in range(BOARD_CASES):
            for y in range(BOARD_CASES):
                piece = self.GetPiece(board[x][y])
                b[y][x] = piece(x * self.cell_size, y * self.cell_size, 0 if board[x][y] > 20 else 1)
        return b

    def HasPieceMouse(self, mousex,mousey):
        if self.player_in_panel: return

        x = int((mousex - self.x ) // self.cell_size)
        y = int((mousey - self.y)  // self.cell_size)

        if x < 0 or x > BOARD_CASES - 1 or y < 0 or y > BOARD_CASES - 1: return False

        if (x,y) in self.eatCases:
            px, py = self.selectedCase
            self.board[px][py].eat(self, x,y)
            self.turn()
            self.UnselectCase()
            return
    

        #TODO: PERMET D'ACTIVER LE TOUR PAR TOUR
        # if self.IsOccuped(x,y): return True
        if self.IsOccuped(x,y) and self.board[x][y].team == self.playingTeam: return True

        if (x,y) in self.moveCases:
            px,py = self.selectedCase
            self.game.ui.add_last_move(self.game, Move(self.playingTeam, "{}{} > {}{}".format(self.num_let(px),py+1,self.num_let(x),y+1)))
            self.board[px][py].move(self, x,y)
            self.turn()
    
    def IsOccuped(self, x,y):
        return self.board[int(x)][int(y)].team >= 0

    def GetPieceMouse(self, mousex, mousey):
        x = int((mousex - self.x ) // self.cell_size)
        y = int((mousey - self.y)  // self.cell_size)

        if self.selectedCase == (x,y):
            return self.UnselectCase()

        self.selectedCase = (x,y)
        self.moveCases.clear()
        self.eatCases.clear()
        self.board[x][y].showAvailibleMove(self)

        moves = []
        eats = []
        if self.check_case:
            for move in self.moveCases:
                if move in self.anti_check_moves: moves.append(move)

            for eat in self.eatCases:
                if eat in self.anti_check_eats: eats.append(eat)

            self.moveCases = moves
            self.eatCases = eats
        return self.board[x][y]

    def UnselectCase(self):
        self.selectedCase = None
        self.moveCases.clear()
        self.eatCases.clear()
 
    def can_be_eaten_at(self, x,y): #RETURN TRUE IF THIS PIECE AT POSITION (x,y) CAN BE EATEN
        for i in range(BOARD_CASES):
            for j in range(BOARD_CASES):
                if self.board[i][j].team == -1: continue
                self.board[i][j].showAvailibleMove(self)
                for pos in self.eatCases:
                    if pos == (x,y): return True
        return False
    
    def check(self):
        self.check_case = None
        for i in range(BOARD_CASES):
            for j in range(BOARD_CASES):
                if self.board[i][j].team == -1: continue
                if self.board[i][j].score == 10: #IF THIS PIECE IS THE KING
                    if self.can_be_eaten_at(i,j): #IF THIS KING CAN BE EATEN
                        self.check_case = (i,j)
        self.moveCases.clear()
        self.eatCases.clear()
        return self.check_case != None


    def check_mate(self):
        prev_white_score = self.whiteScore
        prev_black_score = self.blackScore
        self.anti_check_moves.clear()
        self.anti_check_eats.clear()
        for i in range(BOARD_CASES):
            for j in range(BOARD_CASES):
                self.moveCases.clear()
                self.eatCases.clear()
                piece = self.board[i][j]
                if piece.team == -1 or piece.team != self.playingTeam: continue

                last_pos = (i,j)
                piece.showAvailibleMove(self)

                for move in self.moveCases:
                    piece.move(self, move[0], move[1])
                    if not self.check():
                        self.anti_check_moves.append(move)
                    piece.move(self, last_pos[0], last_pos[1]) #UNDO THE MOVE

                piece.showAvailibleMove(self)

                for eat in self.eatCases:
                    previous_piece = self.board[eat[0]][eat[1]]
                    piece.eat(self, eat[0], eat[1])
                    if not self.check():
                        self.anti_check_eats.append(eat)
                    piece.move(self, last_pos[0], last_pos[1])
                    self.board[eat[0]][eat[1]] = previous_piece

        if not self.anti_check_moves and not self.anti_check_eats:
            self.game.ui.zones["Time"].info_texts[0].freeze = True
            print("echec et mat")
        self.whiteScore = prev_white_score
        self.blackScore = prev_black_score

    def turn(self):
        self.playingTeam = (self.playingTeam + 1) % 2
        if self.check():
            self.check_mate()

    def draw(self):
        for i in range(BOARD_CASES):
            for j in range(BOARD_CASES):
                x = self.x + i * self.cell_size
                y = self.y + j * self.cell_size
                color = (112,162,163) if ((i + j) % 2) else (177,228,186)
                pygame.draw.rect(self.game.win, color, (x,y, self.cell_size, self.cell_size))
                if (i,j) == self.selectedCase:
                    pygame.draw.rect(self.game.win, (255,255,255), (x + 1, y + 1, self.cell_size - 1, self.cell_size - 1), 3)
                if (i,j) in self.moveCases:
                    pygame.draw.rect(self.game.win, (100,50,50), (x + 1, y + 1, self.cell_size - 1, self.cell_size - 1), 5)
                if (i,j) in self.eatCases:
                    pygame.draw.rect(self.game.win, (255,50,50), (x + 1, y + 1, self.cell_size - 1, self.cell_size - 1), 5)
                if self.check_case:
                    pygame.draw.rect(self.game.win, (0,0,255), (self.check_case[0] * self.cell_size + 6, self.check_case[1] * self.cell_size + 6, self.cell_size - 1, self.cell_size - 1), 5)
                self.board[i][j].draw(self.game)
        
        if self.player_in_panel:
            if not self.game.ui.panel_buttons:
                self.game.ui.create_buttons(self.game,self.on_line_piece_team)
            self.on_player_in_panel()

    def switch_piece_on_line(self,piece_id):
        new_piece = self.GetPiece(piece_id)
        px,py = self.on_line_piece_position
        self.board[px][py] = new_piece(py * self.cell_size, px * self.cell_size, self.board[px][py].team)

    def on_player_in_panel(self):
        for btn in self.game.ui.panel_buttons:
            if btn.check_clicked(self.game):
                self.switch_piece_on_line(btn.id)
                self.player_in_panel = False
                btn.is_hovered = False

    def __init__(self, x,y,w,h,game):
        self.x, self.y = x,y
        self.w, self.h = w,h
        self.cell_size = self.w / BOARD_CASES
        self.game = game

        self.board = self.CreateBoard()

        self.selectedCase = None
        self.moveCases = []
        self.eatCases = []
        self.check_case = None
        self.anti_check_moves = []
        self.anti_check_eats = []

        self.playingTeam = 1

        self.whiteScore = 0
        self.blackScore = 0

        self.elapsedTime = 0
        self.player_in_panel = False
        self.on_line_piece_position = None
        self.on_line_piece_team = -1

        self.max_last_moves = 5
        self.last_moves = []

class Move:
    def __init__(self, team, msg):
        self.team = team
        self.msg  = msg
