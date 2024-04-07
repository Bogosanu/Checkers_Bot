

import pygame
from checkers.constants import *
from checkers.board import Board
from checkers.game import Game
from checkers.menu import DropdownMenu
import copy
import time


FPS = 60
def selection_screen(win):
    pygame.font.init()
    font = pygame.font.SysFont(None, 30)
    difficulty_menu = DropdownMenu(50, 300, 200, 30, font, "Select Difficulty", ["Easy", "Medium", "Hard"])
    player_color_menu = DropdownMenu(300, 300, 200, 30, font, "Select Color", ["White", "Black"])


    selecting = True
    while selecting:
        win.fill((0, 0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return None
            difficulty_menu.handle_event(event)
            player_color_menu.handle_event(event)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN and difficulty_menu.get_selected_option() is not None and player_color_menu.get_selected_option() is not None:
                selecting = False

        difficulty_menu.draw(win)
        player_color_menu.draw(win)
        pygame.display.flip()

    return difficulty_menu.get_selected_option(), player_color_menu.get_selected_option()

def get_mouse_pos(pos):
    x, y = pos
    row = y // SQUARE_SIZE
    col = x // SQUARE_SIZE
    return row, col


def main():
    pygame.init()
    WIN = pygame.display.set_mode((WIDTH, HEIGHT))

    pygame.display.set_caption('Checkers')

    selections = selection_screen(WIN)
    difficulty, player_color = selections

    game = Game(WIN, difficulty, player_color)

    if player_color == 'White':
        flipped = True
    else:
        flipped = False
    run = True
    clock = pygame.time.Clock()

    start_time = time.time()

    while run:

        clock.tick(FPS)
        if game.winner() != None:
            end_time = time.time()
            print("Match duration: " + str(round(end_time - start_time, 2)) + " seconds")
            pygame.time.wait(5000)
            run = False

        if game.stalemate == True:
            print("Stalemate")
            end_time = time.time()
            print("Match duration: " + str(round(end_time - start_time, 2)) + " seconds")
            pygame.time.wait(5000)
            run = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if game.turn_to_text() == game.player_col:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    orx, ory = pygame.mouse.get_pos()
                    if flipped:
                        pos = (WIDTH - orx, HEIGHT - ory)
                    else:
                        pos = (orx, ory)
                    row, col = get_mouse_pos(pos)
                    game.select(row, col)
                    # update screen
            else:
                pygame.time.delay(500)
                game.ai_move()
        game.update()
        if flipped:
            rotated_surface = pygame.transform.rotate(WIN, 180)
            WIN.blit(rotated_surface, (0, 0))
            pygame.display.flip()
        if not flipped:
            pygame.display.update()

    pygame.quit()

main()
