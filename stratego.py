import colorama
from colorama import Fore, Back
import sys
colorama.init(autoreset=True)


class Piece:
    # PIECE CONSTRUCTOR
    def __init__(self, rank: str, colour: str = None):
        self._rank = rank
        self._colour = colour

    # METHODS USED TO OBTAIN PIECE ATTRIBUTES
    def get_rank(self) -> str:
        return self._rank

    def get_colour(self) -> str:
        return self._colour


# CLASS THAT HOLDS VARIABLES PERTAINING TO CURRENT GAME STATE
class GameState:
    def __init__(self, colour: str, is_playing: bool, on_coord2: bool):
        self._colour = colour
        self._isPlaying = is_playing
        self._onCoord2 = on_coord2

    def get_colour(self) -> str:
        return self._colour

    def is_playing(self):
        return self._isPlaying

    def on_coord2(self):
        return self._onCoord2

    def set_red(self):
        self._colour = RED

    def set_blue(self):
        self._colour = BLUE

    def set_is_playing(self, bool_value: bool):
        self._isPlaying = bool_value

    def set_on_coord2(self, bool_value: bool):
        self._onCoord2 = bool_value


# CONSTANTS
WATER: str = ' W'
BLUE: str = "blue"
RED: str = "red"

MAR: str = '10'
GEN: str = ' 9'
COL: str = ' 8'
MAJ: str = ' 7'
CAP: str = ' 6'
LIE: str = ' 5'   # Abbreviations of Piece Names
SER: str = ' 4'
MIN: str = ' 3'
SCO: str = ' 2'
SPY: str = ' 1'
BOM: str = ' B'
FLA: str = ' F'

# INITIAL GAME STATE
GameState = GameState(RED, False, False)


def init_board(cell: Piece, col_length: int, row_length: int) -> list:
    return [[cell for row in range(row_length)] for col in range(col_length)]


EMPTY_CELL: str = ' 0'
# INITIALIZES BOARD- ROWS: 8, COLUMNS: 10, CONTENT: '0'
board: list[list[Piece]] = init_board(Piece(EMPTY_CELL), 8, 10)
ROWS_LENGTH: int = len(board)
COLS_LENGTH: int = len(board[0])


def add_water(water: Piece):
    board[3][2] = water
    board[4][2] = water
    board[3][3] = water
    board[4][3] = water

    board[3][6] = water
    board[4][6] = water
    board[3][7] = water
    board[4][7] = water


add_water(Piece(WATER))


def print_board():
    print("  |  0  1  2  3  4  5  6  7  8  9")
    print("- - - - - - - - - - - - - - - - -")

    for row in range(ROWS_LENGTH):
        for col in range(-1, COLS_LENGTH):
            if col == -1:
                letters: list[str] = list(letterToNums)

                print(letters[row] + " | ", end='')
            else:
                cell = board[row][col]

                anon: str = ' S'

                if cell.get_colour() == RED:
                    if GameState.get_colour() == BLUE:
                        print(Fore.RED + anon, end=' ')
                    else:
                        print(Fore.RED + cell.get_rank(), end=' ')
                elif cell.get_colour() == BLUE:
                    if GameState.get_colour() == RED:
                        print(Fore.BLUE + anon, end=' ')
                    else:
                        print(Fore.BLUE + cell.get_rank(), end=' ')
                else:
                    if cell.get_rank() == WATER:
                        water = cell.get_rank()

                        print(Back.CYAN + water, end=' ')
                    else:
                        print(cell.get_rank(), end=' ')
        print()


redPieceNames: list[str] = [
    "Marshal : 10", "General : 9", "Colonel : 8", "2nd Colonel : 8", "Major : 7", "2nd Major : 7", "3rd Major : 7",
    "Captain : 6", "2nd Captain : 6", "3rd Captain : 6", "Lieutenant : 5", "2nd Lieutenant : 5", "Sergeant : 4",
    "2nd Sergeant : 4", "Miner : 3", "2nd Miner : 3", "3rd Miner : 3", "4th Miner : 3", "Scout : 2", "2nd Scout : 2",
    "3rd Scout : 2", "4th Scout : 2", "5th Scout : 2", "Bomb", "2nd Bomb", "3rd Bomb", "4th Bomb", "5th Bomb",
    "Spy : 1", "Flag"
]

bluePieceNames: list = redPieceNames

# PLAYING PIECES
redPieces: list[Piece] = [
    Piece(MAR, RED), Piece(GEN, RED), Piece(COL, RED), Piece(COL, RED), Piece(MAJ, RED), Piece(MAJ, RED),
    Piece(MAJ, RED), Piece(CAP, RED), Piece(CAP, RED), Piece(CAP, RED), Piece(LIE, RED), Piece(LIE, RED),
    Piece(SER, RED), Piece(SER, RED), Piece(MIN, RED), Piece(MIN, RED), Piece(MIN, RED), Piece(MIN, RED),
    Piece(SCO, RED), Piece(SCO, RED), Piece(SCO, RED), Piece(SCO, RED), Piece(SCO, RED), Piece(BOM, RED),
    Piece(BOM, RED), Piece(BOM, RED), Piece(BOM, RED), Piece(BOM, RED), Piece(SPY, RED), Piece(FLA, RED)
]

bluePieces: list[Piece] = [
    Piece(MAR, BLUE), Piece(GEN, BLUE), Piece(COL, BLUE), Piece(COL, BLUE), Piece(MAJ, BLUE), Piece(MAJ, BLUE),
    Piece(MAJ, BLUE), Piece(CAP, BLUE), Piece(CAP, BLUE), Piece(CAP, BLUE), Piece(LIE, BLUE), Piece(LIE, BLUE),
    Piece(SER, BLUE), Piece(SER, BLUE), Piece(MIN, BLUE), Piece(MIN, BLUE), Piece(MIN, BLUE), Piece(MIN, BLUE),
    Piece(SCO, BLUE), Piece(SCO, BLUE), Piece(SCO, BLUE), Piece(SCO, BLUE), Piece(SCO, BLUE), Piece(BOM, BLUE),
    Piece(BOM, BLUE), Piece(BOM, BLUE), Piece(BOM, BLUE), Piece(BOM, BLUE), Piece(SPY, BLUE), Piece(FLA, BLUE)
]


# CHECK IF A PIECE PLACE IS VALID
def valid_place(colour: str, y: int, x: int) -> bool:
    cell: Piece = board[y][x]

    if colour == RED:
        if y >= 5 and 0 <= x <= 9:
            return cell.get_rank() == EMPTY_CELL
    elif colour == BLUE:
        if y <= 2 and 0 <= x <= 9:
            return cell.get_rank() == EMPTY_CELL
    return False


def update_board(y: int, x: int, piece: Piece):
    board[y][x] = piece


# MAPS LETTERS TO THEIR CORRESPONDING INDEX ON THE BOARD
letterToNums: dict[str, int] = {
    'A': 0,
    'B': 1,
    'C': 2,
    'D': 3,
    'E': 4,
    'F': 5,
    'G': 6,
    'H': 7
}


# CHECKS IF COORDINATE INPUT IS VALID
def valid_coordinate(letter: str, num: str) -> bool:
    return letter in list(letterToNums) and num.isnumeric() and int(num) in range(0, 10)


# PIECE SET-UP PHASE
def set_up(piece_names: list[str], pieces: list[Piece]):
    i: int = 0
    while i < len(piece_names) and not GameState.is_playing():
        print(f"[{GameState.get_colour()}] Place your {piece_names[i]}: ")

        coordinate: str = input()

        if len(coordinate) < 2:
            print("You did not satisfy enough values for a coordinate. Provide a valid letter and number")
            continue
        letter: str = coordinate[0].upper()
        num: str = coordinate[1]

        if not valid_coordinate(letter, num):
            print("Invalid coordinate")
            continue
        num1: int = letterToNums.get(letter)
        num2: int = int(num)

        if not valid_place(GameState.get_colour(), num1, num2):
            print("Invalid coordinate")
            continue
        else:
            update_board(num1, num2, pieces[i])

            print_board()

        i += 1


# CHECKS IF ALL PIECES ON A COLOURED TEAM ARE UNABLE TO MOVE AND ATTACK
def all_invalid(colour: str) -> bool:
    movable: list[str] = [MAR, GEN, COL, MAJ, CAP, LIE, SER, MIN, SCO, SPY]
    for row in range(ROWS_LENGTH):
        for col in range(COLS_LENGTH):
            piece: Piece = board[row][col]
            if piece.get_colour() == colour and piece.get_rank() in movable:
                return False
    return True


# CHECKS IF THE FIRST PIECE SELECTED IS CONSIDERED VALID
def valid_source_piece(piece: Piece) -> bool:
    rejects: list[str] = [EMPTY_CELL, WATER, BOM, FLA]

    return piece.get_rank() not in rejects and piece.get_colour() == GameState.get_colour()


# CHECKS IF A PIECE TRAVERSE IS VALID
def valid_move(y1: int, x1: int, y2: int, x2: int) -> bool:
    source: Piece = board[y1][x1]
    destination: Piece = board[y2][x2]

    source_colour: str = source.get_colour()
    valid_destination: bool = destination.get_colour() != source_colour and destination.get_rank() != WATER

    if valid_destination:
        if source.get_rank() == SCO:
            pieces_crossed: list[Piece] = []
            if x1 == x2:
                if y1 != y2:
                    for p in range(y1+1, y2):
                        pieces_crossed.append(board[p][x1])
                    valid_path: bool = all(p.get_rank() == EMPTY_CELL for p in pieces_crossed)
                    # ^checks if pieces crossed in the traverse are empty
                    return valid_path
            elif y1 == y2:
                if x1 != x2:
                    for p in range(x1+1, x2+1):
                        pieces_crossed.append(board[y1][p])

                    valid_path: bool = all(p.get_rank() == EMPTY_CELL for p in pieces_crossed)
                    return valid_path
        else:
            if x1 == x2:
                if y1 != y2 and abs(y2 - y1) <= 1:
                    return True
            elif y1 == y2:
                if x1 != x2 and abs(x2 - x1) <= 1:
                    return True
    return False


# DETERMINES THE RESULTS OF EVERY ATTACK MATCH-UP OF PIECES AND UPDATES THE BOARD ACCORDINGLY
def att_matchups(y1: int, x1: int, y2: int, x2: int):
    source_piece: Piece = board[y1][x1]
    destination_piece: Piece = board[y2][x2]

    source: str = board[y1][x1].get_rank()
    destination: str = board[y2][x2].get_rank()

    if destination == BOM:
        if source == MIN:
            winner: Piece = source_piece
            loser: Piece = destination_piece

            update_board(y2, x2, winner)

            print(f"{Fore.YELLOW}{winner.get_colour()} piece #{winner.get_rank()} has disarmed {loser.get_colour()} piece #{loser.get_rank()}")

        else:
            winner: Piece = destination_piece
            loser: Piece = source_piece

            update_board(y1, x1, Piece(EMPTY_CELL))

            print(f"{Fore.YELLOW}{winner.get_colour()} piece #{winner.get_rank()} has defeated {loser.get_colour()} piece #{loser.get_rank()}")

    elif destination == FLA:
        winning_team: str = source_piece.get_colour()

        print(f"{Fore.YELLOW}Congratulations {winning_team}! You have successfully captured the opponent's flag and won the game!")
        GameState.set_is_playing(False)
        sys.exit()

    else:
        source_val: int = int(source)
        destination_val: int = int(destination)

        if destination_val > source_val:
            if source == SPY and destination_val % int(MAR) == 0:
                winner: Piece = source_piece
                loser: Piece = destination_piece

                update_board(y2, x2, winner)

                print(f"{Fore.YELLOW}{winner.get_colour()} piece #{winner.get_rank()} has defeated {loser.get_colour()} piece #{loser.get_rank()}")
            else:
                winner: Piece = destination_piece
                loser: Piece = source_piece

                print(f"{Fore.YELLOW}{winner.get_colour()} piece #{winner.get_rank()} has defeated {loser.get_colour()} piece #{loser.get_rank()}")

        elif source_val > destination_val:
            winner: Piece = source_piece
            loser: Piece = destination_piece

            update_board(y2, x2, source_piece)

            print(f"{Fore.YELLOW}{winner.get_colour()} piece #{winner.get_rank()} has defeated {loser.get_colour()} piece #{loser.get_rank()}")

        elif source_val == destination_val:
            update_board(y2, x2, Piece(EMPTY_CELL))

            print(f"{Fore.YELLOW}Tie! {source_piece.get_colour()} and {destination_piece.get_colour()} has both lost piece #{source}")


GameState.set_red()
print_board()
set_up(redPieceNames, redPieces)
GameState.set_blue()
set_up(bluePieceNames, bluePieces)
GameState.set_is_playing(True)
GameState.set_red()


# TAKES IN A STARTING PIECE THAT SERVES AS A PREREQUISITE PIECE FOR THE PIECE's DESTINATION
def move_piece_source():
    while GameState.is_playing() and not GameState.on_coord2():
        if all_invalid(BLUE):
            print(f"{Fore.YELLOW}Congratulations {RED}! Your opponent can not move or attack!")
            GameState.set_is_playing(False)
            sys.exit()
        elif all_invalid(RED):
            print(f"{Fore.YELLOW}Congratulations {BLUE}! Your opponent can not move or attack!")
            GameState.set_is_playing(False)
            sys.exit()
        print_board()
        print(f"\n[{GameState.get_colour()}] Input the first coordinate that represents the piece you will move: ")

        coordinate: str = input()

        if len(coordinate) < 2:
            print("You did not satisfy enough values for a coordinate. Provide a valid letter and number")
            continue
        letter: str = coordinate[0].upper()
        num: str = coordinate[1]

        if not valid_coordinate(letter, num):
            print("Invalid coordinate")
            continue
        y1: int = letterToNums.get(letter)
        x1: int = int(num)

        piece_source: Piece = board[y1][x1]

        if not valid_source_piece(piece_source):
            print("Invalid coordinate")
            continue
        else:
            GameState.set_on_coord2(True)

            move_piece_destination(y1, x1)


# TAKES IN THE SELECTED PIECE's DESTINATION OF IT's TRAVERSE
def move_piece_destination(y1: int, x1: int):
    while GameState.is_playing() and GameState.on_coord2():
        print("Input the second coordinate that represents the destination of your selected piece: ")

        coordinate: str = input()

        if len(coordinate) < 2:
            print("You did not satisfy enough values for a coordinate. Provide a valid letter and number")
            continue
        letter: str = coordinate[0].upper()
        num: str = coordinate[1]

        if not valid_coordinate(letter, num):
            print("Invalid coordinate")
            continue
        y2: int = letterToNums.get(letter)
        x2: int = int(num)

        piece_source: Piece = board[y1][x1]
        piece_destination: Piece = board[y2][x2]

        if not valid_move(y1, x1, y2, x2):
            print("Invalid coordinate")
            GameState.set_on_coord2(False)
        else:
            if piece_source.get_colour() != piece_destination.get_colour() and piece_destination.get_rank() != EMPTY_CELL:
                att_matchups(y1, x1, y2, x2)
            else:
                update_board(y2, x2, piece_source)
            update_board(y1, x1, Piece(EMPTY_CELL))

            if GameState.get_colour() == RED:
                GameState.set_blue()
            elif GameState.get_colour() == BLUE:
                GameState.set_red()

            GameState.set_on_coord2(False)


# MAIN LOOP IN PLAYING GAME PHASE
while GameState.is_playing():
    move_piece_source()
