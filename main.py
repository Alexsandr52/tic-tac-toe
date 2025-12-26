"""Main entry point for Galactic Connect 4 game."""

import pygame
import sys
from game import Connect4
from front import UI


class GameApp:
    """Main game application."""

    def __init__(self):
        """Initialize the game application."""
        self.ui = UI()
        self.game = None
        self.player_symbol = 'X'
        self.bot_symbol = 'O'

    def run(self):
        """Run the main game loop."""
        while True:
            # Symbol selection
            self.player_symbol = self.ui.show_symbol_selection()
            self.bot_symbol = 'O' if self.player_symbol == 'X' else 'X'

            # Initialize game
            self.game = Connect4(self.player_symbol, self.bot_symbol)

            # Determine who goes first
            current_player = self.player_symbol
            if self.bot_symbol == 'X':
                current_player = self.bot_symbol

            # Game loop
            self.game_loop(current_player)

            # End screen
            winner = self.game.winner
            choice = self.ui.show_end_screen(winner)

            if choice == 'quit':
                pygame.quit()
                sys.exit()

    def game_loop(self, current_player):
        """Main game loop."""
        running = True
        clock = pygame.time.Clock()

        while running:
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                # Player's turn
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if current_player == self.player_symbol:
                        col = self.ui.get_column_from_click(event.pos)
                        if self.game.is_valid_location(self.game.board, col):
                            self.game.make_move(col, current_player)

                            if self.game.game_over:
                                running = False
                            else:
                                current_player = self.bot_symbol

            # Bot's turn
            if current_player == self.bot_symbol and not self.game.game_over:
                pygame.time.wait(100)  # Small delay for better UX
                col = self.game.get_bot_move()

                if col is not None:
                    self.game.make_move(col, current_player)

                if self.game.game_over:
                    running = False
                else:
                    current_player = self.player_symbol

            # Check for draw
            if self.game.is_board_full() and not self.game.game_over:
                running = False

            # Draw the board
            line_color = (61, 61, 61) if self.game.game_over else (255, 255, 255)
            self.ui.draw_board(self.game.board, line_color=line_color)
            self.ui.update()

            clock.tick(30)


def main():
    """Main entry point."""
    app = GameApp()
    app.run()


if __name__ == '__main__':
    main()
