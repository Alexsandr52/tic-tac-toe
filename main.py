import numpy as np
import random
import pygame
import sys
import math
import copy
import front

# Инициализация Pygame
pygame.init()

# Константы
COLUMNS = 7
ROWS = 6
WINDOW_LENGTH = 4
WIDTH = 700
HEIGHT = 600
CELL_SIZE = WIDTH // COLUMNS
LINE_WIDTH = 4
BG_COLOR = (28, 170, 156)
LINE_COLOR = (23, 145, 135)

# Чем больше глубина тем сложнее играть, честно я 2 не побеждаю почти 
# При этом я норм могу запустить 5-6 и будет бытро и вообще топ 
# Если выше может начать думать дольше, но и точность подскочит
# Тестил с ии с инета они почти в ничью вышли на глубине 5 у этой
# Думаю в ничью они бы съиграли на глубине 6-7
# https://connect4.gamesolver.org/ru/?pos=444343746564661171611612223

DEPTH = 5

# Задал по умелчанию что бы обойтись без лишних проверок
player_symbol = 'X'
bot_symbol = 'O'
win_symbol = ''

# Старт / При выборе зпустят main()
def choose_X():
    global player_symbol, bot_symbol
    player_symbol = 'X'
    bot_symbol = 'O'
    main()

def choose_O():
    global player_symbol, bot_symbol
    player_symbol = 'O'
    bot_symbol = 'X'
    main()

# Функции для работы с игровым процессом
def apply_gravity(board, col, turn):
    for row in range(ROWS-1, -1, -1):
        if board[row][col] == ' ':
            board[row][col] = turn
            return True
    return False

# Поиск доступных позицый
def is_valid_location(board, col):
	return board[0][col] == ' '

def get_valid_locations(board):
	valid_locations = []
	for col in range(COLUMNS):
		if is_valid_location(board, col):
			valid_locations.append(col)
	return valid_locations

# Окончена ли игра
def winning_move(board, symbol):
	
	for c in range(COLUMNS-3):
		for r in range(ROWS):
			if board[r][c] == symbol and board[r][c+1] == symbol and board[r][c+2] == symbol and board[r][c+3] == symbol:
				return True

	for c in range(COLUMNS):
		for r in range(ROWS-3):
			if board[r][c] == symbol and board[r+1][c] == symbol and board[r+2][c] == symbol and board[r+3][c] == symbol:
				return True

	for c in range(COLUMNS-3):
		for r in range(ROWS-3):
			if board[r][c] == symbol and board[r+1][c+1] == symbol and board[r+2][c+2] == symbol and board[r+3][c+3] == symbol:
				return True
               
	for c in range(COLUMNS-3):
		for r in range(3, ROWS):
			if board[r][c] == symbol and board[r-1][c+1] == symbol and board[r-2][c+2] == symbol and board[r-3][c+3] == symbol:
				return True
	return False

def is_terminal_node(board):
	return winning_move(board, player_symbol) or winning_move(board, bot_symbol) or len(get_valid_locations(board)) == 0

# Оценка позиции для выбраного игрока(символа) 
def evaluate_window(window, symbol):
	score = 0
	opponent_symbol = 'O' if symbol == 'X' else 'X'

	if window.count(symbol) == 4: score += 100
	elif window.count(symbol) == 3 and window.count(' ') == 1: score += 5
	elif window.count(symbol) == 2 and window.count(' ') == 2: score += 2
	if window.count(opponent_symbol) == 3 and window.count(' ') == 1: score -= 4

	return score

def score_position(board, symbol):
	score = 0

	## Score center column
	center_array = [i for i in list(board[:, COLUMNS//2])]
     
	center_count = center_array.count(symbol)
	score += center_count * 3

	## Score Horizontal
	for r in range(ROWS):
		row_array = [i for i in list(board[r,:])]
		for c in range(COLUMNS-3):
			window = row_array[c:c+WINDOW_LENGTH]
			score += evaluate_window(window, symbol)

	## Score Vertical
	for c in range(COLUMNS):
		col_array = [i for i in list(board[:,c])]
		for r in range(ROWS-3):
			window = col_array[r:r+WINDOW_LENGTH]
			score += evaluate_window(window, symbol)

	## Score posiive sloped diagonal
	for r in range(ROWS-3):
		for c in range(COLUMNS-3):
			window = [board[r+i][c+i] for i in range(WINDOW_LENGTH)]
			score += evaluate_window(window, symbol)

	for r in range(ROWS-3):
		for c in range(COLUMNS-3):
			window = [board[r+3-i][c+i] for i in range(WINDOW_LENGTH)]
			score += evaluate_window(window, symbol)

	return score

# Минимакс с альфа-бета отсечением
def minimax(board, depth, alpha, beta, maximizingPlayer):
    valid_locations = get_valid_locations(board)
    is_terminal = is_terminal_node(board)
    
    # Если мы дошли до конца глубины или позиция на доске привела законченая
    if depth == 0 or is_terminal:
        if is_terminal:
            if winning_move(board, bot_symbol): return (None, 100000000000000)
            elif winning_move(board, player_symbol): return (None, -10000000000000)
            else: return (None, 0)
        else: return (None, score_position(np.array(board), bot_symbol))

    #Проверка на лучший ход бота
    if maximizingPlayer:
        value = -math.inf
        column = random.choice(valid_locations)
          
        for col in valid_locations:
            b_copy = copy.deepcopy(board)
            
            apply_gravity(b_copy, col, bot_symbol)
            new_score = minimax(b_copy, depth-1, alpha, beta, False)[1]
            
            if new_score > value:
                value = new_score
                column = col

            alpha = max(alpha, value)
            if alpha >= beta: break
        return column, value
    
    # Проверка на лучший ход игрока
    else:
        value = math.inf
        column = random.choice(valid_locations)
        for col in valid_locations:

            b_copy = copy.deepcopy(board)
            apply_gravity(b_copy, col, player_symbol)
            new_score = minimax(b_copy, depth-1, alpha, beta, True)[1]
			
            if new_score < value:
                value = new_score
                column = col
			
            beta = min(beta, value)
            if alpha >= beta: break
        return column, value

# Интеграция Минимакса в ход бота
def bot_move():
    col, score= minimax(board, DEPTH, -float('inf'), float('inf'), True)
    print(f'Bot move: col={col}, score={score}')

    # Если minimax не нашел выгодного хода
    if col is None:
        # Проверяем каждую колонку на наличие хотя бы одной свободной ячейки
        available_cols = get_valid_locations(board)
        if available_cols:  # Если есть доступные колонки
            col = random.choice(available_cols)
            print(f'Random move: col={col}')
        else:  # Если нет доступных ходов
            print('No available moves.')
            return False
		
    elif col is not None:
        apply_gravity(board, col, bot_symbol)
        return True
    
    return False

#  Основной игровой цикл
def main():
    global board, player_symbol, bot_symbol
    board = [[' ' for _ in range(COLUMNS)] for _ in range(ROWS)]
    turn = player_symbol if player_symbol == 'X' else bot_symbol
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and turn != bot_symbol:
                x, y = event.pos
                col = x // CELL_SIZE
                if apply_gravity(board, col, turn):
                    if winning_move(board, turn):
                        running = False
                        win_symbol = turn

                    turn = bot_symbol if turn == player_symbol else player_symbol
            elif turn == bot_symbol:
                bot_move()
                if winning_move(board, turn):
                    running = False
                    win_symbol = turn

                turn = player_symbol if turn == bot_symbol else bot_symbol
        front.draw_board(board)
        pygame.display.flip()

        if is_terminal_node(board):
              front.draw_board(board, LINE_COLOR = (61,61,61))
              front.show_end_game_screen(win_symbol)            

if __name__ == '__main__':
    front.choose_symbol_screen()
    # front.show_end_game_screen('X')
 