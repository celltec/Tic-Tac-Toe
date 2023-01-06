from collections import Counter
from itertools import count, cycle
import PySimpleGUI as sg

# Repeat endlessly until closed
for round in count(1):
    layout = [[sg.Button('',
                         key=(row, col),  # "key" is the identifier of the button
                         size=(4, 1),
                         pad=(2, 2),
                         border_width=0,
                         button_color=('black', 'white'),
                         mouseover_colors=('black', 'white'),
                         font=('Segoe Print', 40)
                         ) for col in range(3)] for row in range(3)]  # Generate 9 buttons in a 3x3 list

    window = sg.Window('Tic Tac Toe',
                       layout,
                       margins=(0, 0),
                       background_color='black')

    # Create a generator that alternatingly returns a symbol as well as an increasing move count
    symbols = enumerate(cycle(('X', 'O')), 1)

    # Prepare an empty data structure that represents the board
    board = [['' for _ in range(3)] for _ in range(3)]

    # Main loop
    running = True
    while running:
        # Get window event
        button = window.read()[0]

        # Handle close event
        if button == sg.WIN_CLOSED:
            window.close()
            exit(0)

        # Check if button has already been clicked
        if window[button].get_text():
            continue

        # Update the window and set the data
        move, symbol = next(symbols)
        window[button].update(symbol)
        row, col = button  # The "key" of a button is its position
        board[row][col] = symbol

        # Get all combinations of board entries that need to be checked
        combinations = board[:]  # Horizontal
        combinations.extend([col for col in zip(*board)])  # Vertical
        combinations.append([board[i][i] for i in range(len(board))])  # Top left to bottom right
        combinations.append([[row[::-1] for row in board][i][i] for i in range(len(board))])  # Top right to bottom left

        # Check all combinations
        for combination in combinations:
            player, amount = Counter(combination).most_common(1)[0]
            if player and amount == 3:
                sg.popup_no_titlebar(f'\nRound {round}:\n{player} wins!\n', font=('Calibi', 20))
                running = False
                break

        # Check if all fields were filled with no winner
        if running and move == 9:
            sg.popup_no_titlebar(f'\nRound {round}:\nDraw!\n', font=('Calibi', 20))
            running = False

    window.close()
