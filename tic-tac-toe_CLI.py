import os
from collections import Counter
from itertools import count, cycle

X = '\033[35m' 'X' '\033[0m'
O = '\033[36m' 'O' '\033[0m'

def print_board(board):
    os.system('cls')
    print('┌───┬───┬───┐')

    counter = 1
    for i, row in enumerate(board, 1):
        print('│', end='')

        for item in row:
            char = item or f'\033[90;3m{counter}\033[0m'
            print(f' {char} │', end='')
            counter += 1
        print()

        if i < len(board):
            print('├───┼───┼───┤')

    print('└───┴───┴───┘')

# Repeat endlessly
for round in count(1):
    # Create a generator that alternatingly returns a symbol as well as an increasing move count
    symbols = enumerate(cycle((X, O)), 1)

    # Prepare an empty data structure that represents the board
    board = [['' for _ in range(3)] for _ in range(3)]
    print_board(board)

    # Main loop
    running = True
    while running:
        while True:  # Get choice of cell from player
            try:
                choice = int(input(f'Choose cell: '))
                if not choice in range(1, 10):
                    raise ValueError
            except ValueError:
                print('Please choose a number between 1 and 9.')
                continue
            break

        # Extract cell coordinates from chosen number
        row, col = divmod(choice - 1, 3)

        # Check if cell was already used
        if board[row][col]:
            continue

        # Update the board
        move, symbol = next(symbols)
        board[row][col] = symbol
        print_board(board)

        # Get all combinations of board entries that need to be checked
        combinations = board[:]  # Horizontal
        combinations.extend([col for col in zip(*board)])  # Vertical
        combinations.append([board[i][i] for i in range(len(board))])  # Top left to bottom right
        combinations.append([[row[::-1] for row in board][i][i] for i in range(len(board))])  # Top right to bottom left

        # Check all combinations
        for combination in combinations:
            player, amount = Counter(combination).most_common(1)[0]
            if player and amount == 3:
                input(f'Round {round}: {player} wins!\n')
                running = False
                break

        # Check if all fields were filled with no winner
        if running and move == 9:
            input(f'Round {round}: Draw!\n')
            running = False
