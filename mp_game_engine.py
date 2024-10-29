from components import initialise_board, create_battleships, place_battleships, is_all_ships_sunk, view_board
import random


def generate_attack(board_size, level=0, hit=None, miss=None):
    # generates an attack position based on the specified level of difficulty.
    if level == 0:
        x = random.randint(0, board_size - 1)
        y = random.randint(0, board_size - 1)
        return (x, y)
    elif level == 1:
        unattacked_cells = []
        for x in range(board_size):
            for y in range(board_size):
                if (x, y) not in hit and (x, y) not in miss:
                    unattacked_cells.append((x, y))
        return random.choice(unattacked_cells)
    elif level == 2:
        unattacked_cells = []
        priority = []
        direction = ((-1, 0), (1, 0), (0, 1), (0, -1))
        for x in range(board_size):
            for y in range(board_size):
                if (x, y) not in hit and (x, y) not in miss:
                    unattacked_cells.append((x, y))
        if hit is None or len(hit) == 0:
            return random.choice(unattacked_cells)
        for cell in unattacked_cells:
            x, y = cell
            for dir in direction:
                dx, dy = dir
                nx, ny = x + dx, y + dy
                if (nx, ny) in hit:
                    priority.append((x, y))
        if priority:
            result = random.choice(priority)
            print('priority', priority, result)
            return result
        return random.choice(unattacked_cells)


def generate_ascii_report(board):
    ascii_report = [['*' for _ in range(len(board[i]))] for i in range(len(board))]
    for i in range(len(board)):
        for j in range(len(board)):
            if board[i][j]:
                ascii_report[i][j] = board[i][j]
    return ascii_report


def update_ascii_report(report, row, col, symbol):
    # updates the ASCII report with the result of an attack (hit or miss) at the specified row and column.
    report[row][col] = symbol


def ai_opponent_game_loop():
    # Sets up and runs the game loop for the Battleship game against an AI opponent.
    print("Welcome to Battleship!")
    players['user'] = {'board': initialise_board(), 'ships': create_battleships()}
    players['ai'] = {'board': initialise_board(), 'ships': create_battleships()}

    opponent_ascii_report = generate_ascii_report(players['user']['board'])

    # Place ships
    place_battleships(players['user']['board'], players['user']['ships'], algorithm='custom')
    place_battleships(players['ai']['board'], players['ai']['ships'], algorithm='random')

    # initialize the report
    ascii_report = generate_ascii_report(players['user']['board'])

    # initialize attack history to avoid duplicate attack
    hits, miss = [], []
    ai_hits, ai_miss = [], []

    while True:
        # User's turn
        x, y = cli_coordinates_input()

        if (x, y) not in hits or (x, y) not in miss:
            print(f'You attack at ({x + 1},{y + 1})')

            if attack((x, y), players['ai']['board'], players['ai']['ships']):
                update_ascii_report(opponent_ascii_report, x, y, 'H')
                print("Hit!")
                hits.append((x, y))
            else:
                update_ascii_report(opponent_ascii_report, x, y, 'M')
                print("Miss!")
                miss.append((x, y))
        else:
            print(f'You attacked at ({x + 1},{y + 1}) before. You wasted one turn.')
        x, y = generate_attack(len(players['user']['board']), 2, ai_hits, ai_miss)
        if (x, y) not in ai_hits or (x, y) not in ai_miss:
            print(f"AI's attack at ({x + 1}, {y + 1})")
            if attack((x, y), players['user']['board'], players['user']['ships']):
                update_ascii_report(ascii_report, x, y, 'H')
                print("Hit!")
                ai_hits.append((x, y))
            else:
                update_ascii_report(ascii_report, x, y, 'M')
                print("Miss!")
                ai_miss.append((x, y))
        else:
            print(f'AI attacked at ({x + 1},{y + 1}) before. AI wasted one turn.')

        # ascii representation of user's board
        print('Your current board:')
        view_board(ascii_report)
        print('AI\'s board:')
        view_board(opponent_ascii_report, 1)

        # Check for game over or not
        if is_all_ships_sunk(players['ai']['ships']):
            print("Congratulations! You won!")
            break
        elif is_all_ships_sunk(players['user']['ships']):
            print("Game Over! AI won.")
            break


# global variable
BOARD_SIZE = 10
players = {}

if __name__ == "__main__":
    # simple_game_loop()
    ai_opponent_game_loop()
