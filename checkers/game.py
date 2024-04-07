import pygame
from checkers.constants import *
from checkers.board import Board


class Game:

    def __init__(self, win, difficulty, player_col):
        self._init()
        self.win = win
        if difficulty == "Easy":
            self.difficulty = 2
        if difficulty == "Medium":
            self.difficulty = 3
        if difficulty == "Hard":
            self.difficulty = 4
        self.stalemate = False
        self.player_col = player_col

    def update(self):
        if self.board.stalemate == True:
            self.stalemate = True
        self.board.draw(self.win)
        self.draw_valid_moves(self.valid_moves)

    def turn_to_text(self):
        if self.turn == BLACK:
            return 'Black'
        else:
            return 'White'

    def text_to_turn(self, text):
        if text == 'Black':
            return BLACK
        else:
            return WHITE

    def _init(self):
        self.has_selected = None
        self.bot_selected = None
        self.board = Board()
        self.turn = BLACK
        self.valid_moves = {}
        self.valid_bot_moves = {}

    def reset(self):
        self._init()

    def winner(self):
        if self.board.black_left <= 0:
            print("Final score: " + str(self.evaluate(self.board) * (-1)))
            print("White wins!")
        elif self.board.white_left <= 0:
            print("Final score: " + str(self.evaluate(self.board)))
            print("Black wins!")
        return self.board.winner()

    def select(self, row, col):
        if self.has_selected:
            result = self._move(row, col)
            if not result:
                self.has_selected = None
                self.select(row, col)
        piece = self.board.get_piece(row, col)
        if piece != 0 and piece.color == self.turn:
            self.has_selected = piece
            self.valid_moves = self.board.get_valid_moves(piece)

           # print(self.valid_moves)
            return True

        return False

    def _move(self, row, col):
        piece = self.board.get_piece(row, col)
        if self.has_selected and piece == 0 and (row, col) in self.valid_moves:
            self.board.move(self.has_selected, row, col)
            skipped = self.valid_moves[(row, col)]
            if skipped:
                self.board.remove(skipped)
            self.board.check_stalemate(self.has_selected)
            self.change_turn()
            return True
        else:
            return False

    def bot_move(self, row, col):
        if self.bot_selected:
            self.board.move(self.bot_selected, row, col)
            skipped = self.valid_bot_moves[(row, col)]
            if self.player_col == 'Black':
                print("Bot removed pieces: ")
                for piece in skipped:
                    print("(" + str(piece.row) + ", " + str(piece.col) + ")")
            else:
                print("Bot removed pieces: ")
                for piece in skipped:
                    print("(" + str(ROWS - piece.row - 1) + ", " + str(COLS - piece.col -  1) + ")")
            if skipped:
                self.board.remove(skipped)
            self.board.check_stalemate(self.bot_selected)
            self.change_turn()
            return True
        else:
            return False

    def draw_valid_moves(self, moves):
        for move in moves:
            row, col = move
            pygame.draw.circle(self.win, BLUE,
                               (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2), 15)

    def change_turn(self):
        self.valid_moves = {}
        if self.turn == BLACK:
            self.turn = WHITE
            print("Turn: White")
        else:
            self.turn = BLACK
            print("Turn: Black")

    def evaluate(self, board):
        if board.stalemate:
            return 0
        else:
            return board.black_left - board.white_left + (board.black_special - board.white_special) * 0.5

    def minimax(self, board, depth, maximizingPlayer, alpha, beta):
        if depth == 0 or board.winner() is not None:
            return self.evaluate(board), None
        if maximizingPlayer:  # Black
            maxEval = float('-inf')
            best_move = None
            for move in board.get_all_moves(BLACK):
                evaluation = self.minimax(move, depth - 1, False, alpha, beta)[0]
                if evaluation > maxEval:
                    maxEval = evaluation
                    best_move = move
                alpha = max(alpha, evaluation)
                if beta <= alpha:
                    break
            start_coord = self.board.get_coord_start(best_move, BLACK)
            move_coord = self.board.get_coord_final(best_move)
            return maxEval, move_coord, start_coord
        else:  # White
            minEval = float('inf')
            best_move = None
            for move in board.get_all_moves(WHITE):
                evaluation = self.minimax(move, depth - 1, True, alpha, beta)[0]
                if evaluation < minEval:
                    minEval = evaluation
                    best_move = move
                beta = min(beta, evaluation)
                if beta <= alpha:
                    break
            start_coord = self.board.get_coord_start(best_move, WHITE)
            move_coord = self.board.get_coord_final(best_move)
            return minEval, move_coord, start_coord

    def ai_move(self):
        if self.player_col == 'White':
            ai_col = BLACK
            maximizing = True
        if self.player_col == 'Black':
            ai_col = WHITE
            maximizing = False
        if self.turn == ai_col:
            _, move_coord, start_coord = self.minimax(self.board, self.difficulty, maximizing, float('-inf'),
                                                      float('inf'))
            if move_coord:
                piece = self.board.get_piece(start_coord[0], start_coord[1])
                self.bot_selected = piece
                self.valid_bot_moves = self.board.get_valid_moves(piece)
                if (self.player_col == 'Black'):
                    print("Bot went from " + str(start_coord) + " to " + str(move_coord))
                else:
                    start_x, start_y = start_coord
                    move_x, move_y = move_coord
                    print("Bot went from (" + str(ROWS - start_x - 1) + ", " + str(COLS - start_y - 1) + ") to (" + str(ROWS - move_x - 1) + ", " + str(COLS - move_y - 1) + ")")  # pentru imaginea rotita cand jucam cu alb
                self.bot_move(move_coord[0], move_coord[1])
