import sys
import pygame
import numpy as np

# Khởi tạo
pygame.init()

# Định nghĩa màu sắc
GRAY = (180, 180, 180)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)  
BLUE = (0, 0, 255) 
BLACK = (0, 0, 0)  

# Kích thước màn hình kết quả
WIDTH = 700
HEIGHT = 800  
PADDING = 100  

# Kích thước các ô
BOARD_ROWS = 3
BOARD_COLS = 3
LINE_WIDTH = 5
SQUARE_SIZE = WIDTH // BOARD_COLS
CIRCLE_RADIUS = SQUARE_SIZE // 3
CIRCLE_WIDTH = 15
CROSS_WIDTH = 25

# Khởi tạo màn hình ban đầu
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Tic Tac Toe AI')
screen.fill(WHITE)

# Font tiêu đề và thông báo
pygame.font.init()
title_font = pygame.font.Font('freesansbold.ttf', 40)  
subtitle_font = pygame.font.Font(None, 36) 
message_font = pygame.font.Font(None, 60)  

# Tên game và tên nhóm
title_text = title_font.render("Tic Tac Toe - AI Minimax Algorithm", True, BLACK)
subtitle_text = subtitle_font.render("Gr7 - Nhan/Trung/Dinh Project", True, BLACK)

# Game board
board = np.zeros((BOARD_ROWS, BOARD_COLS))

# Vẽ tiêu đề và tên nhóm
def draw_banners():
    screen.blit(title_text, ((WIDTH - title_text.get_width()) // 2, 20))
    screen.blit(subtitle_text, ((WIDTH - subtitle_text.get_width()) // 2, 60))
    separator_y = 60 + subtitle_text.get_height() + 10  
    pygame.draw.line(screen, BLACK, (0, separator_y), (WIDTH, separator_y), 5)

# Vẽ các ô trong game
def draw_lines(color=BLACK):
    for i in range(1, BOARD_ROWS):
        pygame.draw.line(screen, color, (0, PADDING + SQUARE_SIZE * i), (WIDTH, PADDING + SQUARE_SIZE * i), LINE_WIDTH)
        pygame.draw.line(screen, color, (SQUARE_SIZE * i, PADDING), (SQUARE_SIZE * i, HEIGHT - (HEIGHT - PADDING - WIDTH)), LINE_WIDTH)

# Vẽ các lượt của người chơi (X-O)
def draw_figures():
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == 1:  # Lượt người chơi (X)
                pygame.draw.line(screen, BLUE,
                                 (col * SQUARE_SIZE + SQUARE_SIZE // 4, PADDING + row * SQUARE_SIZE + SQUARE_SIZE // 4),
                                 (col * SQUARE_SIZE + 3 * SQUARE_SIZE // 4, PADDING + row * SQUARE_SIZE + 3 * SQUARE_SIZE // 4),
                                 CROSS_WIDTH)
                pygame.draw.line(screen, BLUE,
                                 (col * SQUARE_SIZE + SQUARE_SIZE // 4, PADDING + row * SQUARE_SIZE + 3 * SQUARE_SIZE // 4),
                                 (col * SQUARE_SIZE + 3 * SQUARE_SIZE // 4, PADDING + row * SQUARE_SIZE + SQUARE_SIZE // 4),
                                 CROSS_WIDTH)
            elif board[row][col] == 2:  # Lượt di của AI (O)
                pygame.draw.circle(screen, RED,
                                   (int(col * SQUARE_SIZE + SQUARE_SIZE // 2),
                                    int(PADDING + row * SQUARE_SIZE + SQUARE_SIZE // 2)),
                                   CIRCLE_RADIUS, CIRCLE_WIDTH)

# Đánh dấu ô nếu có ô đã được đánh dấu
def mark_square(row, col, player):
    board[row][col] = player

# Kiểm tra ô còn trống
def available_square(row, col):
    return board[row][col] == 0

# Kiểm tra bảng có còn ô trống
def is_board_full():
    return not (board == 0).any()

# Tìm người chiến thắng
def check_win(player):
    for col in range(BOARD_COLS):
        if board[0][col] == player and board[1][col] == player and board[2][col] == player:
            return True

    for row in range(BOARD_ROWS):
        if board[row][0] == player and board[row][1] == player and board[row][2] == player:
            return True

    if board[0][0] == player and board[1][1] == player and board[2][2] == player:
        return True

    if board[0][2] == player and board[1][1] == player and board[2][0] == player:
        return True

    return False

# Thuật toán minimax cho AI
def minimax(minimax_board, depth, is_maximizing):
    if check_win(2):
        return float('inf')
    elif check_win(1):
        return float('-inf')
    elif is_board_full():
        return 0

    if is_maximizing:
        best_score = -float('inf')
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS):
                if minimax_board[row][col] == 0:
                    minimax_board[row][col] = 2
                    score = minimax(minimax_board, depth + 1, False)
                    minimax_board[row][col] = 0
                    best_score = max(score, best_score)
        return best_score
    else:
        best_score = float('inf')
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS):
                if minimax_board[row][col] == 0:
                    minimax_board[row][col] = 1
                    score = minimax(minimax_board, depth + 1, True)
                    minimax_board[row][col] = 0
                    best_score = min(score, best_score)
        return best_score

# Tìm kiếm nước đi tốt nhất cho AI
def best_move(player):
    best_score = -float('inf')
    move = (-1, -1)
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == 0:
                board[row][col] = player
                score = minimax(board, 0, False if player == 2 else True)
                board[row][col] = 0
                if score > best_score:
                    best_score = score
                    move = (row, col)

    if move != (-1, -1):
        mark_square(move[0], move[1], player)
        return True
    return False

# Khởi tạo lại trò chơi
def restart_game():
    screen.fill(WHITE)
    draw_banners()
    draw_lines()
    board.fill(0)

# Hiển thị thông báo cuối trò chơi
def display_end_screen(message, color=WHITE):
    MESSAGE_WIDTH = WIDTH - 200
    MESSAGE_HEIGHT = 200
    overlay_rect = pygame.Rect(50, PADDING + 50, MESSAGE_WIDTH, MESSAGE_HEIGHT)
    pygame.draw.rect(screen, WHITE, overlay_rect)
    pygame.draw.rect(screen, BLACK, overlay_rect, 5)

    text = message_font.render(message, True, color)
    text_rect = text.get_rect(center=(MESSAGE_WIDTH // 2 + 40, PADDING + 100))
    screen.blit(text, text_rect)

    button_rect = pygame.Rect(MESSAGE_WIDTH // 2 - 40, PADDING + 150, 150, 50)
    pygame.draw.rect(screen, GRAY, button_rect)
    pygame.draw.rect(screen, WHITE, button_rect, 3)

    button_text = subtitle_font.render("Play Again", True, BLACK)
    button_text_rect = button_text.get_rect(center=button_rect.center)
    screen.blit(button_text, button_text_rect)  

    return button_rect

# Quay lại menu chính
def back_to_menu_button():
    button_rect = pygame.Rect(50, HEIGHT - 100, 200, 50)
    pygame.draw.rect(screen, GRAY, button_rect)
    pygame.draw.rect(screen, WHITE, button_rect, 3)

    button_text = subtitle_font.render("Back to Menu", True, BLACK)
    button_text_rect = button_text.get_rect(center=button_rect.center)
    screen.blit(button_text, button_text_rect)

    return button_rect

# Hiển thị lựa chọn chế độ chơi
def draw_game_mode_selection():
    screen.fill(WHITE)
    draw_banners()
    
    # Vẽ các lựa chọn chế độ
    title_text = subtitle_font.render("Choose Game Mode", True, BLACK)
    screen.blit(title_text, ((WIDTH - title_text.get_width()) // 2, PADDING))

    pygame.draw.rect(screen, GRAY, pygame.Rect(150, 200, 400, 60))
    pygame.draw.rect(screen, WHITE, pygame.Rect(150, 200, 400, 60), 5)
    screen.blit(subtitle_font.render("Player vs Player", True, BLACK), (250, 210))

    pygame.draw.rect(screen, GRAY, pygame.Rect(150, 280, 400, 60))
    pygame.draw.rect(screen, WHITE, pygame.Rect(150, 280, 400, 60), 5)
    screen.blit(subtitle_font.render("Player vs AI", True, BLACK), (250, 290))

    pygame.draw.rect(screen, GRAY, pygame.Rect(150, 360, 400, 60))
    pygame.draw.rect(screen, WHITE, pygame.Rect(150, 360, 400, 60), 5)
    screen.blit(subtitle_font.render("AI vs AI", True, BLACK), (250, 370))

# Main game loop
game_mode = None
player = 1
game_over = False
winner_message = ""

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if game_mode is None:
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouseX, mouseY = event.pos
                if 150 <= mouseX <= 550:
                    if 200 <= mouseY <= 260:
                        game_mode = "Player vs Player"
                    elif 280 <= mouseY <= 340:
                        game_mode = "Player vs AI"
                    elif 360 <= mouseY <= 420:
                        game_mode = "AI vs AI"

        if game_mode == "Player vs Player" or game_mode == "Player vs AI":
            if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
                mouseX = event.pos[0] // SQUARE_SIZE
                mouseY = (event.pos[1] - PADDING) // SQUARE_SIZE
                if 0 <= mouseY < BOARD_ROWS and available_square(mouseY, mouseX):
                    mark_square(mouseY, mouseX, player)
                    if check_win(player):
                        game_over = True
                        winner_message = "Player Wins!" if player == 1 else "AI Wins!"
                    elif is_board_full():
                        game_over = True
                        winner_message = "It's a Draw!"
                    player = 3 - player

                    if not game_over and game_mode == "Player vs AI" and player == 2:
                        pygame.time.wait(100)
                        if best_move(2):
                            if check_win(2):
                                game_over = True
                                winner_message = "AI Wins!"
                            elif is_board_full():
                                game_over = True
                                winner_message = "It's a Draw!"
                            player = 3 - player

        if game_mode == "AI vs AI":
            if not game_over:
                if best_move(1):  # AI 1 (X)
                    if check_win(1):
                        game_over = True
                        winner_message = "AI 1 (X) Wins!"
                    elif is_board_full():
                        game_over = True
                        winner_message = "It's a Draw!"
                    player = 3 - player
                if best_move(2):  # AI 2 (O)
                    if check_win(2):
                        game_over = True
                        winner_message = "AI 2 (O) Wins!"
                    elif is_board_full():
                        game_over = True
                        winner_message = "It's a Draw!"
                    player = 3 - player

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                restart_game()
                game_over = False
                player = 1
                winner_message = ""

        # Hiển thị lựa chọn và nút quay lại
        if game_mode is None:
            draw_game_mode_selection()
        else:
            screen.fill(WHITE)
            draw_banners()
            draw_lines()
            draw_figures()

            if game_over:
                button_rect = display_end_screen(winner_message, GREEN if winner_message == "Player Wins!" else RED)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if button_rect.collidepoint(event.pos):
                        restart_game()
                        game_over = False
                        player = 1
                        winner_message = ""

                back_button_rect = back_to_menu_button()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if back_button_rect.collidepoint(event.pos):
                        game_mode = None
                        board.fill(0)
                        game_over = False

    pygame.display.update()
