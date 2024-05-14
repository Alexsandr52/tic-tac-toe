import random
import pygame
import sys
from main import WIDTH, HEIGHT, COLUMNS, ROWS, CELL_SIZE, LINE_WIDTH
import main


# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
GREEN = (0, 250, 154)
RED = (255, 0, 0)

# Создание окна
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("tic")

class Button:
    def __init__(self, surface, x, y, width, height, text, text_color, color, hover_color=None, action=None):
        self.surface = surface
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.text_color = text_color
        self.color = color
        self.hover_color = hover_color if hover_color else color
        self.action = action

    def draw(self):
        pygame.draw.rect(self.surface, self.color, self.rect, border_radius=20)
        font = pygame.font.SysFont(None, 30)
        text_surface = font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        self.surface.blit(text_surface, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                if self.action:
                    self.action()

def create_stars(screen, num_stars):
    for _ in range(num_stars):
        x = random.randint(0, WIDTH)
        y = random.randint(0, HEIGHT)
        size = random.randint(1, 3)
        pygame.draw.circle(screen, WHITE, (x, y), size)

def draw_text(surface, text, font_size, color, x, y, max_width=None):
    font = pygame.font.SysFont(None, font_size)
    words = text.split(' ')
    lines = []
    current_line = ''
    
    # Разбиваем текст на строки, учитывая максимальную ширину
    for word in words:
        if max_width and font.size(current_line + word)[0] > max_width:
            lines.append(current_line)
            current_line = ''
        current_line += word + ' '

    lines.append(current_line)  # Добавляем последнюю строку

    # Получаем высоту текста
    text_height = font.size(' ')[1]

    # Рисуем текст на поверхности
    for i, line in enumerate(lines):
        text_surface = font.render(line, True, color)
        text_rect = text_surface.get_rect()

        # Рассчитываем координату x, чтобы центрировать текст по горизонтали
        text_x = x + (WIDTH - text_surface.get_width()) // 2

        # Рассчитываем координату y, учитывая высоту текста и номер строки
        text_y = y + i * text_height

        surface.blit(text_surface, (text_x, text_y))

def choose_symbol_screen():
    screen.fill(BLACK)
    create_stars(screen, 80)

    # Размеры кнопок
    button_width = 100
    button_height = 70

    # Координаты для расположения кнопок посередине экрана
    button_x = (WIDTH - button_width) // 2
    button_y = (HEIGHT/1.5) # Добавляем отступы между кнопками

    # Создание списка кнопок
    buttons = [
        Button(screen, button_x - button_width, button_y, button_width, button_height, "X", RED, (255, 250, 205), action=main.choose_X),
        Button(screen, button_x + button_width, button_y, button_width, button_height, "O", GREEN, GRAY, action=main.choose_O)
    ]
    text_for_main = 'В галактической схватке "4 в ряд" темные силы (X) сражаются против светлых (O). Сделай свой выбор: стань за порядок и справедливость, или погрузись во тьму и хаос. Время сделать свой ход и решить, кто будет править галактикой.'
    # draw_text(screen, text_for_main, 40, WHITE, WIDTH / 4, HEIGHT / HEIGHT/2)
    draw_text(screen, text_for_main, 30, WHITE, 5, 60, max_width=700)
    
    # Главный цикл игры
    while True:
        # Обработка событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            for button in buttons:
                button.handle_event(event)
        
        # Рисуем кнопки
        for button in buttons:
            button.draw()
        
        # Обновление экрана
        pygame.display.flip()

def draw_X(x, y):
    pygame.draw.line(screen, RED, (x + CELL_SIZE * 0.2, y + CELL_SIZE * 0.2), (x + CELL_SIZE * 0.8, y + CELL_SIZE * 0.8), LINE_WIDTH)
    pygame.draw.line(screen, RED, (x + CELL_SIZE * 0.8, y + CELL_SIZE * 0.2), (x + CELL_SIZE * 0.2, y + CELL_SIZE * 0.8), LINE_WIDTH)

def draw_O(x, y):
    pygame.draw.circle(screen, GREEN, (x + CELL_SIZE // 2, y + CELL_SIZE // 2), int(CELL_SIZE * 0.3), LINE_WIDTH)

def draw_board(board, LINE_COLOR = (255, 255, 255)):
    create_stars(screen, 150)
    screen.fill(BLACK)

    for row in range(ROWS):
        for col in range(COLUMNS):
            rect = pygame.Rect(col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, LINE_COLOR, rect, LINE_WIDTH)
            if board[row][col] == 'X':
                draw_X(col * CELL_SIZE, row * CELL_SIZE)
            elif board[row][col] == 'O':
                draw_O(col * CELL_SIZE, row * CELL_SIZE)

def restart_game():
    global board, player_symbol, bot_symbol
    player_symbol = None
    bot_symbol = None
    board = [[' ' for _ in range(COLUMNS)] for _ in range(ROWS)]
    choose_symbol_screen()

def show_end_game_screen(winner):
    
    if winner == main.player_symbol: message = 'Поздравляем! Вы выиграли.'
    elif winner == main.bot_symbol: message = 'К сожалению, вы проиграли.'
    else: message = 'К сожалению бой не выявил победителя!'
    draw_text(screen, message, 65, WHITE, 10, 120, max_width=700)

    runing = True
    while runing:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN: runing = False

        pygame.display.flip()

    # screen.fill(BG_COLOR)
    screen.fill(BLACK)
    create_stars(screen, 80)
    
    draw_text(screen, 'Что планирует делать дальше?', 40, WHITE, 10, 50, max_width=700)

    # Размеры кнопок
    button_width = 160
    button_height = 70

    # Координаты для расположения кнопок посередине экрана
    button_x = (WIDTH - button_width) // 2
    button_y = (HEIGHT/1.5) # Добавляем отступы между кнопками

    # Создание списка кнопок
    buttons = [
        Button(screen, button_x - button_width, button_y, button_width, button_height, "Играть заново", GREEN, GRAY, action=choose_symbol_screen),
        Button(screen, button_x + button_width, button_y, button_width, button_height, "Выйти", RED, (255, 250, 205), action=quit_game)
    ]

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            for button in buttons:
                button.handle_event(event)
            
            # Рисуем кнопки
            for button in buttons:
                button.draw()
            
            # Обновление экрана
            pygame.display.flip()

def quit_game():
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    choose_symbol_screen()