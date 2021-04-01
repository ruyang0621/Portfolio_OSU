# Author: Ru Yang
# Last Modified: 04/01/2021
# Descirption: This is the main driver file for the program of Janggi Game. It will be responsible for handling user
#              input and displaying the current game state.

import pygame
from Janggi.constants import WIDTH, HEIGHT, OFFSET, PIECE_SIZE, SILVER, WHITE, BUTTON, PASS_GIVEUP, PLAYER_FONT
from Janggi.board import Board
from Janggi.ChessPiece import *
from Janggi.JanggiGame import JanggiGame

FPS = 60
WIN = pygame.display.set_mode((WIDTH, HEIGHT + 2 * OFFSET))
WIN.fill(SILVER)
pygame.display.set_caption('Janggi')

def draw_button(win):
    """Draws pass and reset button on """
    win.blit(BUTTON, (OFFSET // 2, OFFSET // 2 - BUTTON.get_height() // 2))
    draw_button_txt_1 = PASS_GIVEUP.render('PASS', 1, WHITE)
    win.blit(draw_button_txt_1, (81, 25))

    win.blit(BUTTON, (WIDTH - BUTTON.get_width() - OFFSET // 2, OFFSET // 2 - BUTTON.get_height() // 2))
    draw_button_txt_2 = PASS_GIVEUP.render('GIVE UP', 1, WHITE)
    win.blit(draw_button_txt_2, (431, 25))

    win.blit(BUTTON, (OFFSET // 2, HEIGHT + OFFSET + (OFFSET - BUTTON.get_height()) // 2))
    draw_button_txt_3 = PASS_GIVEUP.render('PASS', 1, WHITE)
    win.blit(draw_button_txt_3, (81, OFFSET + HEIGHT + 25))

    win.blit(BUTTON, (WIDTH - BUTTON.get_width() - OFFSET // 2, HEIGHT + OFFSET + (OFFSET - BUTTON.get_height()) // 2))
    draw_button_txt_4 = PASS_GIVEUP.render('GIVE UP', 1, WHITE)
    win.blit(draw_button_txt_4, (431, OFFSET + HEIGHT + 25))

def get_row_col_from_mouse(coord):
    """Returns the coord of the mouse button down place."""
    x, y = coord
    row = (y - OFFSET) // PIECE_SIZE
    col = x // PIECE_SIZE
    return [row, col]

def main():
    run = True
    clock = pygame.time.Clock()
    game = JanggiGame(WIN)
    draw_button(WIN)

    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False 
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                coord = pygame.mouse.get_pos()
                pos = get_row_col_from_mouse(coord)
                
                if pos[0] in range(10) and pos[1] in range(9):        # the coord on the game board.
                    game.select(pos)
                else:
                    if coord[0] in range(35, 181):     
                        if coord[1] in range(10, 61):                 # if the red player wants to pass.
                            game.pass_turn('red')
                        if coord[1] in range(720, 751):               # if the blue player wants to pass.
                            game.pass_turn('blue')
                    if coord[0] in range(400, 541):
                        if coord[1] in range(10, 61):                 # if the red player wants to pass.
                            game.give_up('red')
                        if coord[1] in range(720, 771):               # if the blue player wants to pass.
                            game.give_up('blue')

        game.update()

    pygame.quit()

main()
