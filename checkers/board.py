import copy

import pygame
from checkers.constants import *
from checkers.piece import Piece

class Board:
    def __init__(self):
        self.black_left = self.white_left = 12
        self.board = []
        self.selected_piece = None
        self.black_special = self.white_special = 0
        self.create_board()
        self.black_possible_moves = 100
        self.white_possible_moves = 100
        self.stalemate = False


    def calc_black_moves(self):
        check = 0
        for piecech in self.get_all_pieces(BLACK):
            check += len(self.get_valid_moves(piecech))
        return check

    def calc_white_moves(self):
        check = 0
        for piecech in self.get_all_pieces(WHITE):
            check += len(self.get_valid_moves(piecech))
        return check


    def copy(self):
        new_board = Board()
        new_board.board = copy.deepcopy(self.board)
        new_board.black_left = self.black_left
        new_board.white_left = self.white_left
        new_board.black_special = self.black_special
        new_board.white_special = self.white_special
        new_board.calc_black_moves()
        new_board.calc_white_moves()
        new_board.stalemate = self.stalemate
        return new_board

    def __repr__(self):
        print(self.board)
        return " "

    def draw_squares(self, win):
        win.fill(BLACK)
        for row in range(ROWS):
            for col in range(row % 2, ROWS, 2):
                pygame.draw.rect(win, WOOD, (row * SQUARE_SIZE, col * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

    def move(self, piece, row, col):
        self.board[piece.row][piece.col], self.board[row][col] = self.board[row][col], self.board[piece.row][piece.col]
        piece.move(row, col)
        if row == ROWS - 1 or row == 0:
            piece.make_special()
            if piece.color == WHITE:
                self.white_special += 1
            else:
                self.black_special += 1


    def check_stalemate(self, piece):
        if ((self.calc_black_moves() == 0 and piece.color == WHITE) or (self.calc_white_moves() == 0 and piece.color == BLACK)) and self.winner() is None:
            self.stalemate = True
    def get_piece(self, row, col):
        return self.board[row][col]

    def get_all_pieces(self, color):
        piece_list = []
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.get_piece(row, col)
                if piece == 0:
                    continue
                if piece.color == color:
                    piece_list.append(piece)
        return piece_list


    def create_board(self):
        for row in range(ROWS):
            self.board.append([])
            for col in range(COLS):
                if col % 2 == ((row + 1) % 2):
                    if row < 3:
                        self.board[row].append(Piece(row, col, WHITE))
                    elif row > 4:
                        self.board[row].append(Piece(row, col, BLACK))
                    else:
                        self.board[row].append(0)
                else:
                    self.board[row].append(0)

    def draw(self, win):
        self.draw_squares(win)
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board[row][col]
                if piece != 0:
                    piece.draw(win)

    def remove(self, pieces):
        for piece in pieces:
            self.board[piece.row][piece.col] = 0
            if piece != 0:
                if piece.color == BLACK:
                    self.black_left -= 1
                else:
                    self.white_left -= 1

    #def evaluate(self):
       # return self.black_left - self.white_left + (self.black_special - self.white_special) * 0.5 - int(self.stalemate) * 10

    def winner(self):
        if self.black_left <= 0:
            return WHITE
        elif self.white_left <= 0:
            return BLACK

        return None



    def get_valid_moves(self, piece):
        moves = {}
        left = piece.col - 1
        right = piece.col + 1
        row = piece.row

        if piece.color == BLACK or piece.special:
            moves.update(self._traverse_left(row - 1, max(row - 3, -1), -1, piece.color, left))
            moves.update(self._traverse_right(row - 1, max(row - 3, -1), -1, piece.color, right))
        if piece.color == WHITE or piece.special:
            moves.update(self._traverse_left(row + 1, min(row + 3, ROWS), 1, piece.color, left))
            moves.update(self._traverse_right(row + 1, min(row + 3, ROWS), 1, piece.color, right))

        return moves

    def get_all_moves(self, color):
        moves = []
        for piece in self.get_all_pieces(color):
            valid_moves = self.get_valid_moves(piece)
            for move, skipped in valid_moves.items():
                temp_board = self.copy()
                temp_piece = temp_board.get_piece(piece.row, piece.col)
                temp_board.move(temp_piece, move[0], move[1])
                if skipped:
                    temp_board.remove(skipped)
                moves.append(temp_board)
        return moves

    def get_coord_start(self, temp_board, color):
        for row in range(ROWS):
            for col in range(COLS):
                try:
                    if self.board[row][col] != 0 and temp_board.board[row][col] == 0 and self.board[row][col].color == color:
                        return row, col
                except:
                    pass


    def get_coord_final(self, temp_board):
        for row in range(ROWS):
            for col in range(COLS):
                try:
                    if self.board[row][col] == 0 and temp_board.board[row][col] != 0:
                        return row, col
                except:
                    pass

    def _traverse_left(self, start, stop, step, color, left, skipped=[]):
        moves = {}
        last = []
        for r in range(start, stop, step):
            if left < 0:
                break

            current = self.board[r][left]
            if current == 0:
                if skipped and not last:
                    break
                elif skipped:
                    moves[(r, left)] = last + skipped
                else:
                    moves[(r, left)] = last

                if last:
                    if step == -1:
                        row = max(r - 3, -1)
                    else:
                        row = min(r + 3, ROWS)
                    moves.update(self._traverse_left(r + step, row, step, color, left - 1, skipped=last))
                    moves.update(self._traverse_right(r + step, row, step, color, left + 1, skipped=last))
                break
            elif current.color == color:
                break
            else:
                last = [current]

            left -= 1

        return moves

    def _traverse_right(self, start, stop, step, color, right, skipped=[]):
        moves = {}
        last = []
        for r in range(start, stop, step):
            if right >= COLS:
                break

            current = self.board[r][right]
            if current == 0:
                if skipped and not last:
                    break
                elif skipped:
                    moves[(r, right)] = last + skipped
                else:
                    moves[(r, right)] = last

                if last:
                    if step == -1:
                        row = max(r - 3, -1)
                    else:
                        row = min(r + 3, ROWS)
                    moves.update(self._traverse_left(r + step, row, step, color, right - 1, skipped=last))
                    moves.update(self._traverse_right(r + step, row, step, color, right + 1, skipped=last))
                break
            elif current.color == color:
                break
            else:
                last = [current]

            right += 1

        return moves

