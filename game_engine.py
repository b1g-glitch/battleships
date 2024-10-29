from components import initialise_board, create_battleships, place_battleships, is_all_ships_sunk, view_board
import random


def attack(coordinates, board, battleships):
    # Takes coordinates and checks if there's a battleship at those coordinates.
    x, y = coordinates
    if board[x][y] in battleships:
        ship = board[x][y]
        battleships[ship] -= 1
        board[x][y] = None
        return True
    else:
        return False


def cli_coordinates_input():
    # Takes user input for coordinates in the form of space-separated numbers.
    while True:
        numbers = input("Enter coordinates (space to separate, e.g., 1 4): ")
        numbers = numbers.split()
        if len(numbers) != 2:
            print("Invalid input, please enter again.")
            continue
        try:
            x = int(numbers[0])
            y = int(numbers[1])
        except:
            print("Invalid input, please enter again.")
            continue
        if x <= 0 or y <= 0 or x > BOARD_SIZE or y > BOARD_SIZE:
            print("Invalid input, please enter again.")
            continue
        return x - 1, y - 1


def simple_game_loop():
    # main game loop
    # initializes the board, creates battleships, and places them on the board
    print("Welcome to Battleship!")
    board = initialise_board()
    ships = create_battleships()
    place_battleships(board, ships)

    while not is_all_ships_sunk(ships):
        x, y = cli_coordinates_input()
        if attack((x, y), board, ships):
            # repeatedly takes user input for coordinates and attacks the specified position
            # print whether it's a hit or a miss until all ships are sunk.
            print("Hit!")
        else:
            print("Miss!")

    print("Game Over!")


if __name__ == "__main__":
    simple_game_loop()
