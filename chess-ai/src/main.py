import pygame
import sys

from const import *
from game import Game
from square import Square
from move import Move


class Main:

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH + 300, HEIGHT))  # Extra width for chat section
        pygame.display.set_caption('Chess')
        self.game = Game()
        self.chat_messages = []  
        self.chat_input = "" 
        self.typing = False  

    def draw_chat(self):

        chat_x = WIDTH
        chat_y = 0
        chat_width = 300
        chat_height = HEIGHT
        pygame.draw.rect(self.screen, (50, 50, 50), (chat_x, chat_y, chat_width, chat_height))
        pygame.draw.rect(self.screen, (255, 255, 255), (chat_x + 10, chat_y + 10, chat_width - 20, chat_height - 20), 2)


        font = pygame.font.Font(None, 24)
        y_offset = 20
        for message in self.chat_messages[-15:]:  # Show last 15 messages
            text_surface = font.render(message, True, (255, 255, 255))
            self.screen.blit(text_surface, (chat_x + 20, y_offset))
            y_offset += 20


        input_surface = font.render("> " + self.chat_input, True, (0, 255, 0))
        self.screen.blit(input_surface, (chat_x + 20, chat_height - 30))

    def mainloop(self):
        screen = self.screen
        game = self.game
        board = self.game.board
        dragger = self.game.dragger

        while True:
            game.show_bg(screen)
            game.show_last_move(screen)
            game.show_moves(screen)
            game.show_pieces(screen)
            game.show_hover(screen)

            if dragger.dragging:
                dragger.update_blit(screen)

 #chat
            self.draw_chat()

            for event in pygame.event.get():
                # mouse 
                if event.type == pygame.MOUSEBUTTONDOWN:
                    dragger.update_mouse(event.pos)
                    clicked_row = dragger.mouseY // SQSIZE
                    clicked_col = dragger.mouseX // SQSIZE

                    if board.squares[clicked_row][clicked_col].has_piece():
                        piece = board.squares[clicked_row][clicked_col].piece
                        if piece.color == game.next_player:
                            board.calc_moves(piece, clicked_row, clicked_col, bool=True)
                            dragger.save_initial(event.pos)
                            dragger.drag_piece(piece)
                            game.show_bg(screen)
                            game.show_last_move(screen)
                            game.show_moves(screen)
                            game.show_pieces(screen)

                elif event.type == pygame.MOUSEMOTION:
                    motion_row = event.pos[1] // SQSIZE
                    motion_col = event.pos[0] // SQSIZE
                    game.set_hover(motion_row, motion_col)

                    if dragger.dragging:
                        dragger.update_mouse(event.pos)
                        game.show_bg(screen)
                        game.show_last_move(screen)
                        game.show_moves(screen)
                        game.show_pieces(screen)
                        game.show_hover(screen)
                        dragger.update_blit(screen)

                elif event.type == pygame.MOUSEBUTTONUP:
                    if dragger.dragging:
                        dragger.update_mouse(event.pos)
                        released_row = dragger.mouseY // SQSIZE
                        released_col = dragger.mouseX // SQSIZE

                        initial = Square(dragger.initial_row, dragger.initial_col)
                        final = Square(released_row, released_col)
                        move = Move(initial, final)

                        if board.valid_move(dragger.piece, move):
                            captured = board.squares[released_row][released_col].has_piece()
                            board.move(dragger.piece, move)
                            board.set_true_en_passant(dragger.piece)
                            game.play_sound(captured)
                            game.show_bg(screen)
                            game.show_last_move(screen)
                            game.show_pieces(screen)
                            game.next_turn()

                    dragger.undrag_piece()

                elif event.type == pygame.KEYDOWN:
                    if self.typing:
                        if event.key == pygame.K_RETURN:
                            if self.chat_input.strip():
                                self.chat_messages.append(f"Player: {self.chat_input.strip()}")
                            self.chat_input = ""
                            self.typing = False
                        elif event.key == pygame.K_BACKSPACE:
                            self.chat_input = self.chat_input[:-1]
                        else:
                            self.chat_input += event.unicode
                    elif event.key == pygame.K_c:  # Start typing chat
                        self.typing = True
                    elif event.key == pygame.K_t:
                        game.change_theme()
                    elif event.key == pygame.K_r:
                        game.reset()
                        game = self.game
                        board = self.game.board
                        dragger = self.game.dragger

                elif event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            pygame.display.update()


main = Main()
main.mainloop()
