import pygame
from checkers.constants import *

class Piece:
    PADDING = 15
    OUTLINE = 2

    def __init__(self, row, col, color):
        self.row = row
        self.col = col
        self.color = color
        self.x = SQUARE_SIZE * col + SQUARE_SIZE // 2
        self.y = SQUARE_SIZE * row + SQUARE_SIZE // 2
        self.special = False



    def update_pos(self):
        self.x = SQUARE_SIZE * self.col + SQUARE_SIZE // 2
        self.y = SQUARE_SIZE * self.row + SQUARE_SIZE // 2


    def make_special(self):
        self.special = True



    def draw(self, win):
        radius = SQUARE_SIZE // 2 - self.PADDING
        pygame.draw.circle(win, self.color, (self.x, self.y), radius + self.OUTLINE)
        if(self.color == BLACK):
            pygame.draw.circle(win, DARK_BROWN, (self.x, self.y), radius)
        else:
            pygame.draw.circle(win, WHITE, (self.x, self.y), radius)
        if self.special:
            win.blit(CROWN, (self.x - CROWN.get_width() // 2, self.y - CROWN.get_height() // 2))

    def move(self, row, col):
        self.row = row
        self.col = col
        self.update_pos()

    def __repr__(self):
        return "(" + str(self.row) + ", " + str(self.col) + ")"

