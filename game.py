"""Game logic for Connect 4 with Minimax AI."""

import math
import copy
import random
import numpy as np
from config import (
    COLUMNS, ROWS, WINDOW_LENGTH,
    DEPTH, SCORE_FOUR, SCORE_THREE, SCORE_TWO,
    SCORE_OPPONENT_THREE, SCORE_WIN, SCORE_LOSS
)


class Connect4:
    """Connect 4 game with AI opponent using Minimax algorithm."""

    def __init__(self, player_symbol='X', bot_symbol='O'):
        """Initialize the game."""
        self.player_symbol = player_symbol
        self.bot_symbol = bot_symbol
        self.board = [[' ' for _ in range(COLUMNS)] for _ in range(ROWS)]
        self.game_over = False
        self.winner = None

    def create_board(self):
        """Create a new empty board."""
        return [[' ' for _ in range(COLUMNS)] for _ in range(ROWS)]

    def drop_piece(self, board, col, piece):
        """Drop a piece into the specified column."""
        for row in range(ROWS - 1, -1, -1):
            if board[row][col] == ' ':
                board[row][col] = piece
                return True
        return False

    def is_valid_location(self, board, col):
        """Check if a column has space for a new piece."""
        return board[0][col] == ' '

    def get_valid_locations(self, board):
        """Get all valid column locations."""
        return [col for col in range(COLUMNS) if self.is_valid_location(board, col)]

    def winning_move(self, board, piece):
        """Check if the given piece has won."""
        # Check horizontal
        for col in range(COLUMNS - 3):
            for row in range(ROWS):
                if all(board[row][col + i] == piece for i in range(4)):
                    return True

        # Check vertical
        for col in range(COLUMNS):
            for row in range(ROWS - 3):
                if all(board[row + i][col] == piece for i in range(4)):
                    return True

        # Check positively sloped diagonals
        for col in range(COLUMNS - 3):
            for row in range(ROWS - 3):
                if all(board[row + i][col + i] == piece for i in range(4)):
                    return True

        # Check negatively sloped diagonals
        for col in range(COLUMNS - 3):
            for row in range(3, ROWS):
                if all(board[row - i][col + i] == piece for i in range(4)):
                    return True

        return False

    def is_terminal_node(self, board):
        """Check if the game has ended."""
        return (self.winning_move(board, self.player_symbol) or
                self.winning_move(board, self.bot_symbol) or
                len(self.get_valid_locations(board)) == 0)

    def evaluate_window(self, window, piece):
        """Evaluate a window of 4 positions."""
        score = 0
        opponent = 'O' if piece == 'X' else 'X'

        if window.count(piece) == 4:
            score += SCORE_FOUR
        elif window.count(piece) == 3 and window.count(' ') == 1:
            score += SCORE_THREE
        elif window.count(piece) == 2 and window.count(' ') == 2:
            score += SCORE_TWO

        if window.count(opponent) == 3 and window.count(' ') == 1:
            score -= SCORE_OPPONENT_THREE

        return score

    def score_position(self, board, piece):
        """Score the current board position for a given piece."""
        score = 0

        # Score center column (prefer center for strategic advantage)
        center_array = [row[COLUMNS // 2] for row in board]
        center_count = center_array.count(piece)
        score += center_count * 3

        # Score horizontal
        for row in range(ROWS):
            row_array = board[row]
            for col in range(COLUMNS - 3):
                window = row_array[col:col + WINDOW_LENGTH]
                score += self.evaluate_window(window, piece)

        # Score vertical
        for col in range(COLUMNS):
            col_array = [board[row][col] for row in range(ROWS)]
            for row in range(ROWS - 3):
                window = col_array[row:row + WINDOW_LENGTH]
                score += self.evaluate_window(window, piece)

        # Score positively sloped diagonals
        for row in range(ROWS - 3):
            for col in range(COLUMNS - 3):
                window = [board[row + i][col + i] for i in range(WINDOW_LENGTH)]
                score += self.evaluate_window(window, piece)

        # Score negatively sloped diagonals
        for row in range(ROWS - 3):
            for col in range(COLUMNS - 3):
                window = [board[row + 3 - i][col + i] for i in range(WINDOW_LENGTH)]
                score += self.evaluate_window(window, piece)

        return score

    def minimax(self, board, depth, alpha, beta, maximizing_player):
        """Minimax algorithm with alpha-beta pruning."""
        valid_locations = self.get_valid_locations(board)
        is_terminal = self.is_terminal_node(board)

        if depth == 0 or is_terminal:
            if is_terminal:
                if self.winning_move(board, self.bot_symbol):
                    return None, SCORE_WIN
                elif self.winning_move(board, self.player_symbol):
                    return None, SCORE_LOSS
                else:
                    return None, 0
            else:
                return None, self.score_position(board, self.bot_symbol)

        # Maximizing player (bot)
        if maximizing_player:
            value = -math.inf
            column = random.choice(valid_locations)

            for col in valid_locations:
                board_copy = copy.deepcopy(board)
                self.drop_piece(board_copy, col, self.bot_symbol)
                new_score = self.minimax(board_copy, depth - 1, alpha, beta, False)[1]

                if new_score > value:
                    value = new_score
                    column = col

                alpha = max(alpha, value)
                if alpha >= beta:
                    break

            return column, value

        # Minimizing player (human)
        else:
            value = math.inf
            column = random.choice(valid_locations)

            for col in valid_locations:
                board_copy = copy.deepcopy(board)
                self.drop_piece(board_copy, col, self.player_symbol)
                new_score = self.minimax(board_copy, depth - 1, alpha, beta, True)[1]

                if new_score < value:
                    value = new_score
                    column = col

                beta = min(beta, value)
                if alpha >= beta:
                    break

            return column, value

    def get_bot_move(self):
        """Get the best move for the bot using Minimax."""
        col, score = self.minimax(self.board, DEPTH, -math.inf, math.inf, True)

        if col is None:
            valid_locations = self.get_valid_locations(self.board)
            if valid_locations:
                col = random.choice(valid_locations)

        return col

    def make_move(self, col, piece):
        """Make a move on the board."""
        if self.drop_piece(self.board, col, piece):
            if self.winning_move(self.board, piece):
                self.game_over = True
                self.winner = piece
            return True
        return False

    def is_board_full(self):
        """Check if the board is full."""
        return len(self.get_valid_locations(self.board)) == 0
