import random
import json


def initialise_board(size=10):
    return [[None for _ in range(size)] for _ in range(size)]


def view_board(board, cell_size=16):
    # internal debug usage
    max_index = len(board)
    max_index_space = 1
    while max_index // 10:
        max_index = max_index // 10
        max_index_space += 1
    cell_size = max(cell_size, max_index_space)
    # cell_size parameter determines the width of each cell in characters.
    view_row = [str(item).center(cell_size) if item else ' ' * cell_size for item in range(1, len(board) + 1)]
    print((' ' * (max_index_space + 1)) + '|', end='')
    print(*view_row, sep='|', end='|\n')
    for i in range(len(board)):
        row = board[i]
        print('|' + str(i + 1).center(max_index_space), end='')
        view_row = [item.center(cell_size) if item else ' ' * cell_size for item in row]
        print('|', end='')
        print(*view_row, sep='|', end='|\n')


def create_battleships(filename="battleships.txt"):
    battleships = {}
    with open(filename, 'r') as file:
        for line in file:
            name, size = line.split(':')
            battleships[name] = int(size)
    return battleships


def next_empty_position(board, row, col):
    # returns the indices of the next empty cell.
    for i in range(row, len(board)):
        for j in range(len(board[row])):
            if i == row and col == j:
                continue
            if board[i][j] is None:
                return i, j
    for i in range(len(board)):
        for j in range(len(board[row])):
            if i == row and col == j:
                return None
            if board[i][j] is None:
                return i, j


def is_valid_placement(board, row, col, size, orientation):
    if orientation == 'h':
        for i in range(size):
            if col + i >= 0 and col + i < len(board[row]) and board[row][col + i] is None:
                continue
            else:
                return False
        return True
    else:
        for i in range(size):
            if row + i >= 0 and row + i < len(board) and board[row + i][col] is None:
                continue
            else:
                return False
        return True


def place_battleships(board, ships, algorithm='simple', placement_json=None):
    # utilizes the is_valid_placement function and the next_empty_position function to determine valid positions.
    if algorithm == 'simple':
        # simple in-order placement
        row, col = 0, 0
        for name, size in ships.items():
            while True:
                if is_valid_placement(board, row, col, size, 'h'):
                    for i in range(ships[name]):
                        board[row][col + i] = name
                    row, col = next_empty_position(board, row, col)
                    break
                elif is_valid_placement(board, row, col, size, 'v'):
                    for i in range(ships[name]):
                        board[row + i][col] = name
                    row, col = next_empty_position(board, row, col)
                    break
                else:
                    row, col = next_empty_position(board, row, col)
    elif algorithm == 'random':
        for name in ships:
            while True:
                row = random.randint(0, len(board) - 1)
                col = random.randint(0, len(board[row]) - 1)
                orientation = random.choice(['h', 'v'])
                if is_valid_placement(board, row, col, ships[name], orientation):
                    if orientation == 'h':
                        for i in range(ships[name]):
                            board[row][col + i] = name
                    else:
                        for i in range(ships[name]):
                            board[row + i][col] = name
                    break
    elif algorithm == 'custom':
        if placement_json is None:
            placement_file = "placement.json"
            with open(placement_file, 'r') as file:
                placements = json.load(file)
        else:
            placements = placement_json
        for name, placement in placements.items():
            row, col, orientation = int(placement[0]), int(placement[1]), placement[2]
            if is_valid_placement(board, row, col, ships[name], orientation):
                if orientation == 'h':
                    for i in range(ships[name]):
                        board[row][col + i] = name
                else:
                    for i in range(ships[name]):
                        board[row + i][col] = name
        return board


def is_all_ships_sunk(ships):
    # It returns True if all ships are sunk, otherwise False.
    for name in ships:
        if ships[name] > 0:
            return False
    return True
