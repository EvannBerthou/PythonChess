import pygame

BLANK = -1
BLACK = 0
WHITE = 1

class Piece:
    def __init__(self, x,y, team, score):
        self.x = x + 25
        self.y = y + 30
        self.team = team
        self.score = score

    def draw(self, game):
        game.win.blit(self.sprite, (self.y, self.x))

    def move(self, board,x,y):
        #CURRENT PIECE POSITION
        px = int(self.x / board.cell_size)
        py = int(self.y / board.cell_size)
        if board.board[x][y].team == BLANK:
            board.board[py][px] = Blank(0,0,0)
            Piece.__init__(self, y * board.cell_size, x * board.cell_size, self.team, self.score)
            board.board[x][y] = self
    
    def checkMoveAndEat(self, board, cx,cy):
        if cx >= 0 and cy >= 0 and cx < 8 and cy < 8:
            if board.IsOccuped(cy,cx):
                if board.board[cy][cx].team != self.team:
                    board.eatCases.append((cy,cx))
                return True
            board.moveCases.append((cy,cx))

    def eat(self, board,x,y):
        px = int(self.x / board.cell_size)
        py = int(self.y / board.cell_size)

        if self.team == WHITE: board.whiteScore += board.board[x][y].score
        if self.team == BLACK: board.whiteScore += board.board[x][y].score

        board.board[x][y] = self
        Piece.__init__(self, y * board.cell_size, x * board.cell_size, self.team, self.score)
        board.board[py][px] = Blank(0,0,0)

class Blank:
    def __init__(self,x,y,team):
        self.team = BLANK
    def draw(self, game):
        pass

class Pawn(Piece):
    def __init__(self, x,y, team):
        Piece.__init__(self, x,y,team, 1)
        spriteName = "{}Pawn.png".format("black" if team == BLACK else "white")
        self.sprite = pygame.image.load(spriteName).convert_alpha()
        self.firstMove = True

    def on_end_line(self, board):
        px = int(self.x / board.cell_size)
        if px == 0 or px == 7: return True
    
    def move(self, board, x,y):
        #CURRENT PIECE POSITION
        px = int(self.x / board.cell_size)
        py = int(self.y / board.cell_size)
        if board.board[x][y].team == BLANK:
            board.board[py][px] = Blank(0,0,0)
            Piece.__init__(self, y * board.cell_size, x * board.cell_size, self.team, 1)
            board.board[x][y] = self
            self.firstMove = False

        if self.on_end_line(board) and not board.check_case:
            board.on_line_piece_position = (x,y)
            board.on_line_piece_team = self.team
            board.player_in_panel = True

    def showAvailibleMove(self, board):
        x = int(self.x / board.cell_size)
        y = int(self.y / board.cell_size)

        direction = 1 if self.team == 0 else -1
        if x + direction >= 8 or x + direction < 0: return

        for d in [1,-1]:
            if y + d < 0 or y + d >= 8: continue
            if board.IsOccuped(y + d, x + direction) and board.board[y + d][x + direction].team != self.team:
                board.eatCases.append((y + d,x + direction))
        if not board.IsOccuped(y, x + direction):
            board.moveCases.append((y, x + direction))
            if self.firstMove and not board.IsOccuped(y, x + direction * 2):
                board.moveCases.append((y, x + direction * 2))



class King(Piece):
    def __init__(self, x,y, team):
        Piece.__init__(self, x,y,team, 10)
        spriteName = "{}King.png".format("black" if team == BLACK else "white")
        self.sprite = pygame.image.load(spriteName).convert_alpha()

    def showAvailibleMove(self, board):
        x = int(self.x / board.cell_size)
        y = int(self.y / board.cell_size)

        for cx in [x - 1, x, x + 1]:
            for cy in [y - 1, y, y + 1]:
                if x == cx and y == cy: continue
                if self.checkOtherKing(board, cx,cy): continue
                self.checkMoveAndEat(board, cx,cy)

    def checkOtherKing(self, board, x,y):
        for cx in [x - 1, x, x + 1]:
            for cy in [y - 1, y, y + 1]:
                if cx == x and cy == y: continue
                if cx < 0 or cy < 0 or cx >= 8 or cy >= 8: continue
                if board.IsOccuped(cy,cx):
                    if board.board[cy][cx].score == self.score and board.board[cy][cx].team != self.team:
                        return True
        return False


class Queen(Piece):
    def __init__(self, x,y, team):
        Piece.__init__(self, x,y,team, 9)
        spriteName = "{}Queen.png".format("black" if team == BLACK else "white")
        self.sprite = pygame.image.load(spriteName).convert_alpha()

    def showAvailibleMove(self, board): 
        x = int(self.x / board.cell_size)
        y = int(self.y / board.cell_size)

        #TOWER MOUVEMENT
        for d in [(1,0),(0,1),(-1,0),(0,-1)]: 
            for v in range(8):
                cx = x + d[0] * v
                cy = y + d[1] * v
                if cx == x and cy == y: continue
                if self.checkMoveAndEat(board, cx,cy): break

        #BISHOP MOUVEMENT
        for dx in [1,-1]:
            for dy in [1,-1]:
                for v in range(8):
                    cx = x + dx * v
                    cy = y + dy * v
                    if cx == x and cy == y: continue
                    if self.checkMoveAndEat(board, cx,cy): break

class Rook(Piece):
    def __init__(self, x,y, team):
        Piece.__init__(self, x,y,team, 5)
        spriteName = "{}Rook.png".format("black" if team == BLACK else "white")
        self.sprite = pygame.image.load(spriteName).convert_alpha()

    def showAvailibleMove(self, board): 
        x = int(self.x / board.cell_size)
        y = int(self.y / board.cell_size)

        for d in [(1,0),(0,1),(-1,0),(0,-1)]:
            for v in range(8):
                
                cx = x + d[0] * v
                cy = y + d[1] * v

                if cx == x and cy == y: continue
                if self.checkMoveAndEat(board, cx,cy): break

class Bishop(Piece):
    def __init__(self, x,y, team):
        Piece.__init__(self, x,y,team, 3)
        spriteName = "{}Bishop.png".format("black" if team == BLACK else "white")
        self.sprite = pygame.image.load(spriteName).convert_alpha()

    def showAvailibleMove(self, board):
        x = int(self.x / board.cell_size)
        y = int(self.y / board.cell_size)

        for dx in [1,-1]:
            for dy in [1,-1]:
                for v in range(8):
                    cx = x + dx * v
                    cy = y + dy * v
                    if cx == x and cy == y: continue
                    if self.checkMoveAndEat(board, cx,cy): break

class Knight(Piece):
    def __init__(self, x,y, team):
        Piece.__init__(self, x,y,team, 3)
        spriteName = "{}Knight.png".format("black" if team == BLACK else "white")
        self.sprite = pygame.image.load(spriteName).convert_alpha()

    def showAvailibleMove(self, board):
        x = int(self.x / board.cell_size)
        y = int(self.y / board.cell_size)
        for d in [(1,2),(2,1),(2,-1),(1,-2),(-1,-2),(-2,-1),(-2,1),(-1,2)]:
            cx = x + d[0]
            cy = y + d[1]

            if cx == x and cy == y: continue
            if cx >= 0 and cy >= 0 and cx < 8 and cy < 8:
                if board.IsOccuped(cy,cx): 
                    if board.board[cy][cx].team != self.team:
                        board.eatCases.append((cy,cx))
                else:
                    board.moveCases.append((cy,cx))

