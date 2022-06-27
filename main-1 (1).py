from collections import namedtuple

#  to hold the information of each tile in the grid
Grid = namedtuple('battle_grid', 'is_ship_tile is_destroyed')
Ship = namedtuple('ship', 'x_cord y_cord alignment size')

#  holds the information of ships held by each player
PLAYERS_SHIPS = {1: [], 2: []}

# number of ships per player
NUMBER_OF_SHIPS = 1

#  holds the scores of the players
PLAYERS_SCORE = {1: 0, 2: 0}

#  holds the current player information
CURRENT_PLAYER = 1

#  holds the current player information
CURRENT_BOARD = []

#  Grid x-axis co-ordinates
X_COORDINATES = {}

#  Grid y-axis co-ordinates
Y_COORDINATES = {}


# builds grid according to given co-ordinates
def build_coordinate():
    start_letter = 'A'
    for i in range(SIZE):
        if start_letter not in Y_COORDINATES.keys():
            Y_COORDINATES[start_letter] = i
        if str(i + 1) not in X_COORDINATES.keys():
            X_COORDINATES[str(i + 1)] = i
        start_letter = chr(ord(start_letter) + 1)


# gets numeric validated input from user
def get_validated_input(message):
    while True:
        try:
            print(message)
            value = int(input())
            if value > 0:
                return value
            else:
                print("Please enter a valid numeric value")
        except:
            print("Please enter a valid numeric value")


# gets numeric validated input from user
def get_validated_input_in_range(message, min, max):
    while True:
        try:
            print(message)
            value = int(input())
            if max >= value >= min:
                return value
            else:
                print("Please enter a valid numeric value")
        except:
            print("Please enter a valid numeric value")


#  displays each tile based on its current status destroyed, missed, un-hit
def display_battle_grid():
    print('INSTRUCTIONS: AN X = SUCCESSFULLY DESTROYED SHIP, AN M = MISSED HIT , AN EMPTY SPACE MEANS UN-HIT TILE')
    print('   ', end='')
    print('| ' + ' | '.join(X_COORDINATES.keys()) + ' |')
    if SIZE < 10:
        print('----' * (len(X_COORDINATES.keys()) + 1))
    else:
        print('-----' * (len(X_COORDINATES.keys()) - 1))
    keys = list(Y_COORDINATES.keys())
    for i in range(len(CURRENT_BOARD)):
        print(keys[i] + '  | ', end='')
        for j in range(len(CURRENT_BOARD[i])):
            if not CURRENT_BOARD[i][j].is_destroyed and CURRENT_BOARD[i][j].is_ship_tile:
                print('S | ', end='')
            elif CURRENT_BOARD[i][j].is_destroyed and not CURRENT_BOARD[i][j].is_ship_tile:
                print('M | ', end='')
            elif CURRENT_BOARD[i][j].is_destroyed and CURRENT_BOARD[i][j].is_ship_tile:
                print('X | ', end='')
            else:
                if j < len(CURRENT_BOARD[i]) - 1 and CURRENT_BOARD[i][j + 1].is_destroyed:
                    print(' | ', end='')
                elif j < len(CURRENT_BOARD[i]) - 1 and CURRENT_BOARD[i][j + 1].is_destroyed \
                        and not CURRENT_BOARD[i][j].is_ship_tile:
                    print(' |  ', end='')
                else:
                    print(' |  ', end='')
        print()
        if SIZE < 10:
            print('----' * (len(X_COORDINATES.keys()) + 1))
        else:
            print('-----' * (len(X_COORDINATES.keys()) - 1))


# checks how many ships of opponent have been completely destroyed
def destroyed_ships_count(ships):
    count = 0
    for ship in ships:
        if ship.alignment == 2:
            c = 0
            for i in range(ship.size):
                if i < SIZE and CURRENT_BOARD[ship.x_cord][ship.y_cord + i].is_destroyed:
                    c += 1
            if c == ship.size:
                count += 1
        else:
            c = 0
            for i in range(ship.size):
                if i < SIZE and CURRENT_BOARD[ship.x_cord + i][ship.y_cord].is_destroyed:
                    c += 1
            if c == ship.size:
                count += 1
    return count


#  change the turn of the players
def change_turn():
    global CURRENT_PLAYER
    global CURRENT_BOARD

    if CURRENT_PLAYER == 1:
        CURRENT_PLAYER = 2
        CURRENT_BOARD = PLAYER_TWO_BOARD
    else:
        CURRENT_PLAYER = 1
        CURRENT_BOARD = PLAYER_ONE_BOARD


#  gets the attack co-ordinate for the human player/players
def get_valid_coordinates(message):
    while True:
        co_ordinates = input(message)
        y_ordinate = co_ordinates[0]
        x_ordinate = co_ordinates[1:]
        if x_ordinate in X_COORDINATES.keys() and y_ordinate in Y_COORDINATES.keys():
            return [Y_COORDINATES[y_ordinate], X_COORDINATES[x_ordinate], co_ordinates]
        else:
            print('please enter valid coordinates')


# simulate the player vs player functionality
def player_vs_player():
    while True:
        display_battle_grid()
        count = destroyed_ships_count(PLAYERS_SHIPS[CURRENT_PLAYER])

        # change_turn()
        # count_other = destroyed_ships_count(PLAYERS_SHIPS[CURRENT_PLAYER])
        # change_turn()

        print("\t\t\t\t Player " + str(CURRENT_PLAYER) + " Score: " + str(PLAYERS_SCORE[CURRENT_PLAYER]))
        print("\t\t\t\t Player " + str(CURRENT_PLAYER) + " Remaining Ships: " + str(NUMBER_OF_SHIPS - count))
        # print("\t\t\t\t Player 2 Remaining Ships: " + str(NUMBER_OF_SHIPS - count_other))

        # change_turn()
        coordinates = get_valid_coordinates('Enter Coordinates you want to attack i.e (A10) or (B5) :- ')
        # change_turn()

        print("\t\t\t\t Player " + str(CURRENT_PLAYER) + " attacked " + str(coordinates[2]))

        # change_turn()
        if CURRENT_BOARD[coordinates[0]][coordinates[1]].is_ship_tile:
            print("\t\t\t\t Part of Player " + str(CURRENT_PLAYER) + "'s ship got destroyed.")
            PLAYERS_SCORE[CURRENT_PLAYER] = PLAYERS_SCORE[CURRENT_PLAYER] + 1

        CURRENT_BOARD[coordinates[0]][coordinates[1]] = Grid(CURRENT_BOARD[coordinates[0]][coordinates[1]].is_ship_tile, True)
        count = destroyed_ships_count(PLAYERS_SHIPS[CURRENT_PLAYER])
        # change_turn()

        if count == NUMBER_OF_SHIPS:
            if CURRENT_PLAYER == 1:
                print("Player 1 Won!. Destroyed all Player 2 ships")
                break
            else:
                print("Player 2 Won!. Destroyed all Player 1 ships")
                break
        change_turn()


# create ships for each player
def create_ships(board):
    for i in range(NUMBER_OF_SHIPS):
        co_ordinates = get_valid_coordinates('Enter Starting Coordinates of Ship i.e (A10) or (B5) :- ')
        size = get_validated_input("Enter ship size")
        alignment = get_validated_input_in_range("Enter alignment of ship (1 = vertical, 2 = horizontal)", 1, 2)
        PLAYERS_SHIPS[CURRENT_PLAYER].append(Ship(co_ordinates[0], co_ordinates[1], alignment, size))
        if alignment == 2:
            for j in range(size):
                if co_ordinates[1] + j < SIZE:
                    board[co_ordinates[0]][co_ordinates[1]+j] = Grid(True, False)
        else:
            for j in range(size):
                if co_ordinates[1] + j < SIZE:
                    board[co_ordinates[0]+j][co_ordinates[1]] = Grid(True, False)


SIZE = get_validated_input("Enter the grid size")
PLAYER_ONE_BOARD = [[Grid(False, False) for y in range(SIZE)] for x in range(SIZE)]
PLAYER_TWO_BOARD = [[Grid(False, False) for y in range(SIZE)] for x in range(SIZE)]

CURRENT_BOARD = PLAYER_ONE_BOARD
build_coordinate()
print('Enter Ship Details for Player 1', end='\n\n')
create_ships(PLAYER_ONE_BOARD)
print('Enter Ship Details for Player 2', end='\n\n')
CURRENT_PLAYER = 2
CURRENT_BOARD = PLAYER_TWO_BOARD
create_ships(PLAYER_TWO_BOARD)
CURRENT_PLAYER = 1
CURRENT_BOARD = PLAYER_ONE_BOARD
player_vs_player()
