"""Configuration constants for Connect 4 game."""

# Game board dimensions
COLUMNS = 7
ROWS = 6
WINDOW_LENGTH = 4

# Window settings
WIDTH = 700
HEIGHT = 600
CELL_SIZE = WIDTH // COLUMNS
LINE_WIDTH = 4

# Colors
BG_COLOR = (28, 170, 156)
LINE_COLOR = (23, 145, 135)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
GREEN = (0, 250, 154)
RED = (255, 0, 0)

# AI Difficulty
# Higher depth = harder gameplay
# Depth 5-6 provides good balance of difficulty and performance
# Depth 7+ may take longer but provides near-perfect play
DEPTH = 5

# Minimax scoring values
SCORE_FOUR = 100
SCORE_THREE = 5
SCORE_TWO = 2
SCORE_OPPONENT_THREE = -4
SCORE_WIN = 100000000000000
SCORE_LOSS = -10000000000000
