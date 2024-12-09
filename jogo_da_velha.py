import random

def print_board(board):
    for row in board:
        print(" | ".join(row))
    print("\n")

def is_winner(board, mark):
    # Checa linhas, colunas e diagonais para uma vitória
    for i in range(3):
        if all(cell == mark for cell in board[i]):  # Linhas
            return True
        if all(board[j][i] == mark for j in range(3)):  # Colunas
            return True
    # Diagonais
    if all(board[i][i] == mark for i in range(3)) or all(board[i][2 - i] == mark for i in range(3)):
        return True
    return False

def empty_cells(board):
    return [(i, j) for i in range(3) for j in range(3) if board[i][j] == " "]

def make_move(board, mark, move):
    board[move[0]][move[1]] = mark

def find_winning_move(board, mark):
    for i, j in empty_cells(board):
        board[i][j] = mark
        if is_winner(board, mark):
            board[i][j] = " "  # Reverte a mudança
            return (i, j)
        board[i][j] = " "
    return None

def find_fork_move(board, mark):
    for i, j in empty_cells(board):
        board[i][j] = mark
        winning_moves = 0
        for x, y in empty_cells(board):
            board[x][y] = mark
            if is_winner(board, mark):
                winning_moves += 1
            board[x][y] = " "
        board[i][j] = " "
        if winning_moves >= 2:
            return (i, j)
    return None

def find_opposite_corner(board, opponent_mark):
    corners = [(0, 0), (0, 2), (2, 0), (2, 2)]
    for i, j in corners:
        if board[i][j] == opponent_mark:
            opposite = (2 - i, 2 - j)
            if board[opposite[0]][opposite[1]] == " ":
                return opposite
    return None

def find_empty_corner(board):
    corners = [(0, 0), (0, 2), (2, 0), (2, 2)]
    for i, j in corners:
        if board[i][j] == " ":
            return (i, j)
    return None

def intelligent_move(board, player_mark, opponent_mark):
    # R1: Vitória ou bloqueio
    move = find_winning_move(board, player_mark) or find_winning_move(board, opponent_mark)
    if move:
        return move

    # R2: Criar um garfo
    move = find_fork_move(board, player_mark)
    if move:
        return move

    # R3: Centro livre
    if board[1][1] == " ":
        return (1, 1)

    # R4: Oposto ao canto do oponente
    move = find_opposite_corner(board, opponent_mark)
    if move:
        return move

    # R5: Canto vazio
    move = find_empty_corner(board)
    if move:
        return move

    # R6: Qualquer espaço vazio
    return random.choice(empty_cells(board))

def main():
    board = [[" " for _ in range(3)] for _ in range(3)]
    player_mark = "X"
    opponent_mark = "O"

    print("Bem-vindo ao Jogo da Velha!")
    print_board(board)

    for turn in range(9):
        if turn % 2 == 0:  # Jogador inteligente
            print("Jogada do sistema especialista:")
            move = intelligent_move(board, player_mark, opponent_mark)
            make_move(board, player_mark, move)
        else:  # Oponente
            print("Sua vez (digite linha e coluna):")
            move = None
            while move not in empty_cells(board):
                try:
                    move = tuple(map(int, input("Linha e coluna (0-2 separados por espaço): ").split()))
                except ValueError:
                    continue
            make_move(board, opponent_mark, move)

        print_board(board)

        if is_winner(board, player_mark):
            print("O sistema especialista venceu!")
            return
        elif is_winner(board, opponent_mark):
            print("Você venceu! Parabéns!")
            return

    print("Empate!")

if __name__ == "__main__":
    main()
