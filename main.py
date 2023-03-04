import pygame
import chess
from stockfish import Stockfish

cent_detect = 75
max_moves = 20
stockfish = Stockfish(r"C:\Users\tanne\Documents\Chess\stockfish_14.1_win_x64_avx2\stockfish_14.1_win_x64_avx2\stockfish_14.1_win_x64_avx2.exe")
#board.set_fen('r3r1k1/pp1q1ppp/2n1pn2/1B1p4/3P4/B1P5/P1P2PPP/R2QR1K1 w - - 2 13') 
#Uncomment the line above and add your FEN to load the board from a certain state.
board = chess.Board()

previous_board_state = False
recalculate_eval = True
# initialize Pygame
pygame.init()

# set up the screen
screen = pygame.display.set_mode((360, 390))
stockfish.set_position(board.fen())

# load the piece images
piece_images = {
    chess.Piece(chess.PAWN, chess.WHITE): pygame.image.load("pgns/wp.png"),
    chess.Piece(chess.KNIGHT, chess.WHITE): pygame.image.load("pgns/wn.png"),
    chess.Piece(chess.BISHOP, chess.WHITE): pygame.image.load("pgns/wb.png"),
    chess.Piece(chess.ROOK, chess.WHITE): pygame.image.load("pgns/wr.png"),
    chess.Piece(chess.QUEEN, chess.WHITE): pygame.image.load("pgns/wq.png"),
    chess.Piece(chess.KING, chess.WHITE): pygame.image.load("pgns/wk.png"),
    chess.Piece(chess.PAWN, chess.BLACK): pygame.image.load("pgns/bp.png"),
    chess.Piece(chess.KNIGHT, chess.BLACK): pygame.image.load("pgns/bn.png"),
    chess.Piece(chess.BISHOP, chess.BLACK): pygame.image.load("pgns/bb.png"),
    chess.Piece(chess.ROOK, chess.BLACK): pygame.image.load("pgns/br.png"),
    chess.Piece(chess.QUEEN, chess.BLACK): pygame.image.load("pgns/bq.png"),
    chess.Piece(chess.KING, chess.BLACK): pygame.image.load("pgns/bk.png"),
}


# set up the Stockfish engine
evaluation = None

def calculate_new_eval(cent_detect, max_moves):
    all_moves = stockfish.get_top_moves(max_moves)
    equally_valid_moves = []
    if board.turn:
        const = 1
        top_centi_pawn = max(all_moves, key=lambda x: x["Centipawn"])["Centipawn"]
    else:
        const = -1
        top_centi_pawn = min(all_moves, key=lambda x: x["Centipawn"])["Centipawn"]
    for move in all_moves:
        if const ==1:
            if move["Centipawn"] > top_centi_pawn - cent_detect:
                equally_valid_moves.append(move)
            else: 
                break
        if const ==-1:
            if move["Centipawn"] < top_centi_pawn + cent_detect:
                equally_valid_moves.append(move)
            else: 
                break
    print(equally_valid_moves)
    new_eval = sum(d["Centipawn"] for d in equally_valid_moves) / len(equally_valid_moves)
    return new_eval

# render the board
def render_board():
    # Define the bar rectangle
    bar_rect = pygame.Rect(0, 0, 360, 30)
    pygame.draw.rect(screen, (0, 0, 0), bar_rect)

    # Render all squares and pieces except the one being dragged
    for square in chess.SQUARES:
        rank, file = chess.square_rank(square), chess.square_file(square)
        color = (255, 206, 158) if (rank + file) % 2 == 0 else (209, 139, 71)
        pygame.draw.rect(screen, color, pygame.Rect(file * 45, (7 - rank) * 45 + 30, 45, 45))
        piece = board.piece_at(square)
        if piece is not None and not (dragging and square == dragging_from):
            image = piece_images[piece]
            rect = pygame.Rect(file * 45, (7 - rank) * 45 + 30, 45, 45)
            screen.blit(image, rect)

    # Render the dragged piece on top of everything else
    if dragging:
        piece = board.piece_at(dragging_from)
        if piece is not None:
            image = piece_images[piece]
            rect = pygame.Rect(pygame.mouse.get_pos()[0] - 22, pygame.mouse.get_pos()[1] - 22, 45, 45)
            screen.blit(image, rect)

    # Render the evaluation text inside the bar
    if evaluation is not None:
        font = pygame.font.SysFont("Arial", 20)
        text = font.render("Evaluation: " + str(evaluation), True, (255, 255, 255))
        screen.blit(text, (10, 5))


# handle drag and drop
dragging = False
dragging_piece = None
dragging_from = None
def handle_drag_and_drop(event):
    global dragging, dragging_piece, dragging_from, previous_board_state,stockfish, board, recalculate_eval
    if event.type == pygame.MOUSEBUTTONDOWN:
        x, y = event.pos
        file, rank = x // 45, 7 - (y - 30) // 45
        square = chess.square(file, rank)
        piece = board.piece_at(square)
        if piece is not None:
            dragging = True
            dragging_piece = piece
            dragging_from = square
    elif event.type == pygame.MOUSEBUTTONUP:
        if dragging:
            x, y = event.pos
            file, rank = x // 45, 7 - (y - 30) // 45
            dragging_to = chess.square(file, rank)
            move = chess.Move(dragging_from, dragging_to)
            if move in board.legal_moves:
                board.push(move)
                stockfish.set_fen_position(board.fen())
                recalculate_eval = True
            dragging = False

                
# main loop
font = pygame.font.SysFont("Arial", 20)
text = font.render(" " , True, (255, 255, 255))
while True:
    # handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        elif event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEBUTTONUP:
            handle_drag_and_drop(event)
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            board.set_fen(chess.STARTING_FEN)
            recalculate_eval = True

    # render the board
    render_board()
    if recalculate_eval:
        evaluation = round(calculate_new_eval(cent_detect= cent_detect, max_moves=max_moves)/100,2)
        recalculate_eval = False
    if evaluation is not None:
        font = pygame.font.SysFont("Arial", 20)
    screen.blit(text, (10, 10))
    previous_board_state = board.copy()

    # update the screen
    pygame.display.update()