"""UI components for Connect 4 game."""

import pygame
import sys
import random
from config import (
    WIDTH, HEIGHT, COLUMNS, ROWS, CELL_SIZE, LINE_WIDTH,
    WHITE, BLACK, GRAY, GREEN, RED
)


class Button:
    """A clickable button widget."""

    def __init__(self, surface, x, y, width, height, text, text_color,
                 color, hover_color=None, action=None):
        """Initialize button."""
        self.surface = surface
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.text_color = text_color
        self.color = color
        self.hover_color = hover_color if hover_color else color
        self.action = action

    def draw(self):
        """Draw the button on the surface."""
        pygame.draw.rect(self.surface, self.color, self.rect, border_radius=20)
        font = pygame.font.SysFont(None, 30)
        text_surface = font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        self.surface.blit(text_surface, text_rect)

    def handle_event(self, event):
        """Handle button events."""
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos) and self.action:
                self.action()


class UI:
    """User interface for Connect 4 game."""

    def __init__(self):
        """Initialize the UI."""
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Galactic Connect 4")

    def create_stars(self, num_stars=80):
        """Draw random stars on the screen."""
        for _ in range(num_stars):
            x = random.randint(0, WIDTH)
            y = random.randint(0, HEIGHT)
            size = random.randint(1, 3)
            pygame.draw.circle(self.screen, WHITE, (x, y), size)

    def draw_text(self, text, font_size, color, x, y, max_width=None):
        """Draw wrapped text on the screen."""
        font = pygame.font.SysFont(None, font_size)
        words = text.split(' ')
        lines = []
        current_line = ''

        for word in words:
            test_line = current_line + word + ' '
            if max_width and font.size(test_line)[0] > max_width:
                lines.append(current_line)
                current_line = word + ' '
            else:
                current_line = test_line

        if current_line:
            lines.append(current_line)

        text_height = font.size(' ')[1]

        for i, line in enumerate(lines):
            text_surface = font.render(line, True, color)
            text_x = x + (WIDTH - text_surface.get_width()) // 2
            text_y = y + i * text_height
            self.screen.blit(text_surface, (text_x, text_y))

    def draw_x(self, x, y):
        """Draw X symbol at given position."""
        margin = CELL_SIZE * 0.2
        pygame.draw.line(
            self.screen, RED,
            (x + margin, y + margin),
            (x + CELL_SIZE - margin, y + CELL_SIZE - margin),
            LINE_WIDTH
        )
        pygame.draw.line(
            self.screen, RED,
            (x + CELL_SIZE - margin, y + margin),
            (x + margin, y + CELL_SIZE - margin),
            LINE_WIDTH
        )

    def draw_o(self, x, y):
        """Draw O symbol at given position."""
        radius = int(CELL_SIZE * 0.3)
        center = (x + CELL_SIZE // 2, y + CELL_SIZE // 2)
        pygame.draw.circle(self.screen, GREEN, center, radius, LINE_WIDTH)

    def draw_board(self, board, line_color=WHITE):
        """Draw the game board."""
        self.screen.fill(BLACK)
        self.create_stars(150)

        for row in range(ROWS):
            for col in range(COLUMNS):
                rect = pygame.Rect(col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(self.screen, line_color, rect, LINE_WIDTH)

                piece = board[row][col]
                if piece == 'X':
                    self.draw_x(col * CELL_SIZE, row * CELL_SIZE)
                elif piece == 'O':
                    self.draw_o(col * CELL_SIZE, row * CELL_SIZE)

    def get_column_from_click(self, pos):
        """Get column index from mouse click position."""
        x, _ = pos
        return x // CELL_SIZE

    def show_symbol_selection(self):
        """Show symbol selection screen and return selected symbol."""
        intro_text = (
            'In the galactic battle of "Connect 4", the dark forces (X) '
            'fight against the light (O). Make your choice: stand for order '
            'and justice, or embrace the darkness and chaos. Time to make '
            'your move and decide who will rule the galaxy.'
        )

        button_width = 100
        button_height = 70
        button_x = (WIDTH - button_width) // 2
        button_y = HEIGHT / 1.5

        symbols = ['X', 'O']
        selected = [None]

        def select_x():
            selected[0] = 'X'

        def select_o():
            selected[0] = 'O'

        buttons = [
            Button(self.screen, button_x - button_width, button_y,
                   button_width, button_height, "X", RED, (255, 250, 205),
                   action=select_x),
            Button(self.screen, button_x + button_width, button_y,
                   button_width, button_height, "O", GREEN, GRAY,
                   action=select_o)
        ]

        while True:
            self.screen.fill(BLACK)
            self.create_stars(80)
            self.draw_text(intro_text, 30, WHITE, 5, 60, max_width=700)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                for button in buttons:
                    button.handle_event(event)

            for button in buttons:
                button.draw()

            pygame.display.flip()

            if selected[0]:
                return selected[0]

    def show_end_screen(self, winner):
        """Show end game screen with winner announcement."""
        if winner == 'X':
            message = 'Dark forces prevail! X wins!'
        elif winner == 'O':
            message = 'Light triumphs! O wins!'
        else:
            message = 'The battle ends in a draw!'

        self.draw_text(message, 65, WHITE, 10, 120, max_width=700)

        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    waiting = False

            pygame.display.flip()

        self.screen.fill(BLACK)
        self.create_stars(80)
        self.draw_text('What will you do next?', 40, WHITE, 10, 50, max_width=700)

        button_width = 160
        button_height = 70
        button_x = (WIDTH - button_width) // 2
        button_y = HEIGHT / 1.5

        choice = [None]

        def play_again():
            choice[0] = 'again'

        def quit_game():
            choice[0] = 'quit'

        buttons = [
            Button(self.screen, button_x - button_width, button_y,
                   button_width, button_height, "Play Again", GREEN, GRAY,
                   action=play_again),
            Button(self.screen, button_x + button_width, button_y,
                   button_width, button_height, "Exit", RED, (255, 250, 205),
                   action=quit_game)
        ]

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                for button in buttons:
                    button.handle_event(event)

            for button in buttons:
                button.draw()

            pygame.display.flip()

            if choice[0]:
                return choice[0]

    def update(self):
        """Update the display."""
        pygame.display.flip()
