import Piece
from Piece import *
from gameState import *
import colorama
from colorama import Fore, Back
import sys
import random
import time
colorama.init(autoreset=True)

# CONSTANTS
WATER: str = ' W'
BLUE: str = "blue"
RED: str = "red"

MAR: str = '10'
GEN: str = ' 9'
COL: str = ' 8'
MAJ: str = ' 7'
CAP: str = ' 6'
LIE: str = ' 5'
SER: str = ' 4'
MIN: str = ' 3'
SCO: str = ' 2'
SPY: str = ' 1'
BOM: str = ' B'
FLA: str = ' F'
EMPTY_CELL: str = ' 0'
WAIT_TIME: int = 1

pieceNames: list[str] = [
    "Marshal : 10", "General : 9", "Colonel : 8", "2nd Colonel : 8", "Major : 7", "2nd Major : 7", "3rd Major : 7",
    "Captain : 6", "2nd Captain : 6", "3rd Captain : 6", "Lieutenant : 5", "2nd Lieutenant : 5", "Sergeant : 4",
    "2nd Sergeant : 4", "Miner : 3", "2nd Miner : 3", "3rd Miner : 3", "4th Miner : 3", "Scout : 2", "2nd Scout : 2",
    "3rd Scout : 2", "4th Scout : 2", "5th Scout : 2", "Bomb", "2nd Bomb", "3rd Bomb", "4th Bomb", "5th Bomb",
    "Spy : 1", "Flag"
]

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


def init_board(cell: Piece, col_length: int, row_length: int) -> list[list[Piece]]:
    return [[cell for row in range(row_length)] for col in range(col_length)]


def add_water(_board: list[list[Piece]], water: Piece) -> list[list[Piece]]:
    tmp_board: list[list[Piece]] = _board[:]
    tmp_board[3][2] = water
    tmp_board[4][2] = water
    tmp_board[3][3] = water
    tmp_board[4][3] = water

    tmp_board[3][6] = water
    tmp_board[4][6] = water
    tmp_board[3][7] = water
    tmp_board[4][7] = water

    return tmp_board


def print_board(colour: str, _board):
    print("  |  0  1  2  3  4  5  6  7  8  9")
    print("- - - - - - - - - - - - - - - - -")

    for row in range(ROWS_LENGTH):
        for col in range(-1, COLS_LENGTH):
            if col == -1:
                letters: list[str] = list(letterToNums)

                print(letters[row] + " | ", end='')
            else:
                cell = _board[row][col]

                anon: str = ' S'

                if cell.get_colour() == RED:
                    if colour == BLUE:
                        print(Fore.RED + anon, end=' ')
                    else:
                        print(Fore.RED + cell.get_rank(), end=' ')
                elif cell.get_colour() == BLUE:
                    if colour == RED:
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


# CHECK IF A PIECE PLACE IS VALID
def valid_place(colour: str, _board: list[list[Piece]], y: int, x: int) -> bool:
    cell: Piece = _board[y][x]

    if colour == RED:
        if y >= 5 and 0 <= x <= 9:
            return cell.get_rank() == EMPTY_CELL
    elif colour == BLUE:
        if y <= 2 and 0 <= x <= 9:
            return cell.get_rank() == EMPTY_CELL
    return False


def update_board(_board: list[list[Piece]], y: int, x: int, piece: Piece) -> list[list[Piece]]:
    tmp_board = _board[:]
    tmp_board[y][x] = piece
    return tmp_board


# CHECKS IF COORDINATE INPUT IS VALID
def valid_coordinate(letter: str, num: str) -> bool:
    return letter in list(letterToNums) and num.isnumeric() and int(num) in range(0, 10)


# PIECE SET-UP PHASE
def set_up(colour: str, _board: list[list[Piece]]) -> list[list[Piece]]:
    tmp_board = _board[:]
    i: int = 0
    while i < len(pieceNames) and not GameState.is_playing():
        print(f"[{colour}] Place your {pieceNames[i]}: ")
        print(end='> ')

        coordinate: str = input()

        if len(coordinate) < 2:
            print(Fore.RED + "You did not satisfy enough values for a coordinate. Provide a valid letter and number")
            continue
        letter: str = coordinate[0].upper()
        num: str = coordinate[1]

        if not valid_coordinate(letter, num):
            print(Fore.RED + "Invalid coordinate. A valid coordinate must start with a letter from A-H and end with a number from 0-9")
            continue
        num1: int = letterToNums.get(letter)
        num2: int = int(num)

        if not valid_place(colour, tmp_board, num1, num2):
            if colour == RED: print(Fore.RED + "Invalid place. Your coordinates should be placed within the bottom 3 rows")
            else: print(Fore.RED + "Invalid place. Your coordinates should be placed within the top 3 rows")
            continue
        else:
            tmp_board = update_board(tmp_board, num1, num2, redPieces[i]) if colour == RED else update_board(tmp_board, num1, num2, bluePieces[i])
            print_board(colour, tmp_board)

        i += 1
    return tmp_board


# CHECKS IF ALL PIECES ON A COLOURED TEAM ARE UNABLE TO MOVE AND ATTACK
def all_invalid(_board: list[list[Piece]], colour: str) -> bool:
    movable: list[str] = [MAR, GEN, COL, MAJ, CAP, LIE, SER, MIN, SCO, SPY]
    for row in range(ROWS_LENGTH):
        for col in range(COLS_LENGTH):
            piece: Piece = _board[row][col]
            if piece.get_colour() == colour and piece.get_rank() in movable:
                return False
    return True


# CHECKS IF A PIECE TRAVERSE IS VALID
def valid_move(_board: list[list[Piece]], y1: int, x1: int, y2: int, x2: int) -> bool:
    tmp_board = _board[:]
    source: Piece = board[y1][x1]
    destination: Piece = board[y2][x2]

    source_colour: str = source.get_colour()
    valid_destination: bool = destination.get_colour() != source_colour and destination.get_rank() != WATER

    if valid_destination:
        if source.get_rank() == SCO:
            pieces_crossed: list[Piece] = []
            if x1 == x2 and y1 != y2:
                for p in range(y1+1, y2):
                    pieces_crossed.append(tmp_board[p][x1])
                valid_path: bool = all(p.get_rank() == EMPTY_CELL for p in pieces_crossed)
                # ^checks if pieces crossed in the traverse are empty
                return valid_path
            elif y1 == y2 and x1 != x2:
                for p in range(x1+1, x2+1):
                    pieces_crossed.append(tmp_board[y1][p])
                valid_path: bool = all(p.get_rank() == EMPTY_CELL for p in pieces_crossed)
                return valid_path
        else:
            if x1 == x2 and y1 != y2 and abs(y2 - y1) <= 1:
                return True
            elif y1 == y2 and x1 != x2 and abs(x2 - x1) <= 1:
                return True

    return False


# DETERMINES THE RESULTS OF EVERY ATTACK MATCH-UP OF PIECES AND UPDATES THE BOARD ACCORDINGLY
def attack(_board: list[list[Piece]], y1: int, x1: int, y2: int, x2: int) -> list[list[Piece]]:
    tmp_board: list[list[Piece]] = _board[:]

    source_piece: Piece = tmp_board[y1][x1]
    destination_piece: Piece = tmp_board[y2][x2]

    source: str = tmp_board[y1][x1].get_rank()
    destination: str = tmp_board[y2][x2].get_rank()

    if destination == BOM:
        if source == MIN:
            winner: Piece = source_piece
            loser: Piece = destination_piece

            tmp_board = update_board(tmp_board, y2, x2, winner)

            print(f"{Fore.YELLOW}{winner.get_colour()} piece #{winner.get_rank()} has disarmed {loser.get_colour()} piece #{loser.get_rank()}")
            time.sleep(WAIT_TIME)
            return tmp_board

        else:
            winner: Piece = destination_piece
            loser: Piece = source_piece

            tmp_board = update_board(tmp_board, y1, x1, Piece(EMPTY_CELL))

            print(f"{Fore.YELLOW}{winner.get_colour()} piece #{winner.get_rank()} has defeated {loser.get_colour()} piece #{loser.get_rank()}")
            time.sleep(WAIT_TIME)
            return tmp_board
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

                tmp_board = update_board(tmp_board, y2, x2, winner)

                print(f"{Fore.YELLOW}{winner.get_colour()} piece #{winner.get_rank()} has defeated {loser.get_colour()} piece #{loser.get_rank()}")
                time.sleep(WAIT_TIME)
                return tmp_board
            else:
                winner: Piece = destination_piece
                loser: Piece = source_piece

                print(f"{Fore.YELLOW}{winner.get_colour()} piece #{winner.get_rank()} has defeated {loser.get_colour()} piece #{loser.get_rank()}")
                time.sleep(WAIT_TIME)
                return tmp_board
        elif source_val > destination_val:
            winner: Piece = source_piece
            loser: Piece = destination_piece

            tmp_board = update_board(tmp_board, y2, x2, source_piece)

            print(f"{Fore.YELLOW}{winner.get_colour()} piece #{winner.get_rank()} has defeated {loser.get_colour()} piece #{loser.get_rank()}")
            time.sleep(WAIT_TIME)
            return tmp_board
        elif source_val == destination_val:
            tmp_board = update_board(tmp_board, y2, x2, Piece(EMPTY_CELL))

            print(f"{Fore.YELLOW}Tie! {source_piece.get_colour()} and {destination_piece.get_colour()} has both lost piece #{source}")
            time.sleep(WAIT_TIME)
            return tmp_board


# CHECKS IF THE FIRST PIECE SELECTED IS CONSIDERED VALID
def valid_source_piece(colour: str, piece: Piece) -> bool:
    rejects: list[str] = [EMPTY_CELL, WATER, BOM, FLA]

    return piece.get_rank() not in rejects and piece.get_colour() == colour


# TAKES IN A STARTING PIECE THAT SERVES AS A PREREQUISITE PIECE FOR THE PIECE's DESTINATION
def move_piece_source(colour: str, _board: list[list[Piece]]):
    tmp_board: list[list[Piece]] = _board

    while GameState.is_playing() and not GameState.on_coord2():
        if all_invalid(tmp_board, BLUE):
            print(f"{Fore.YELLOW}Congratulations {RED}! Your opponent can not move or attack!")
            GameState.set_is_playing(False)
            sys.exit()
        elif all_invalid(tmp_board, RED):
            print(f"{Fore.YELLOW}Congratulations {BLUE}! Your opponent can not move or attack!")
            GameState.set_is_playing(False)
            sys.exit()
        print(f"\n[{colour}] Input the first coordinate that represents the piece you will move\n")
        print_board(colour, tmp_board)
        print()
        print(end='> ')

        coordinate: str = input()

        if len(coordinate) < 2:
            print(Fore.RED + "You did not satisfy enough values for a coordinate. Provide a valid letter and number")
            time.sleep(WAIT_TIME)
            continue
        letter: str = coordinate[0].upper()
        num: str = coordinate[1]

        if not valid_coordinate(letter, num):
            print(Fore.RED + "Invalid coordinate. A valid coordinate must start with a letter from A-H and end with a number from 0-9")
            time.sleep(WAIT_TIME)
            continue
        y1: int = letterToNums.get(letter)
        x1: int = int(num)

        piece_source: Piece = tmp_board[y1][x1]

        if not valid_source_piece(colour, piece_source):
            print(f"{Fore.RED}Invalid piece. Select only a {colour} piece that is not a bomb or a flag. Bombs and flags can not be moved")
            time.sleep(WAIT_TIME)
            continue
        GameState.set_on_coord2(True)

        move_piece_destination(colour, tmp_board, y1, x1)


# TAKES IN THE SELECTED PIECE's DESTINATION OF IT's TRAVERSE
def move_piece_destination(colour: str, _board: list[list[Piece]], y1: int, x1: int):
    tmp_board: list[list[Piece]] = _board[:]

    while GameState.is_playing() and GameState.on_coord2():
        print("Input the second coordinate that represents the destination of your selected piece: ")
        print(end='> ')
        coordinate: str = input()

        if len(coordinate) < 2:
            print(Fore.RED + "You did not satisfy enough values for a coordinate. Provide a valid letter and number")
            time.sleep(WAIT_TIME)
            continue
        letter: str = coordinate[0].upper()
        num: str = coordinate[1]

        if not valid_coordinate(letter, num):
            print(Fore.RED + "Invalid coordinate. A valid coordinate must start with a letter from A-H and end with a number from 0-9")
            time.sleep(WAIT_TIME)
            continue
        y2: int = letterToNums.get(letter)
        x2: int = int(num)

        piece_source: Piece = tmp_board[y1][x1]
        piece_destination: Piece = tmp_board[y2][x2]

        if not valid_move(_board, y1, x1, y2, x2):
            print(Fore.RED + "Invalid move. NOTE: You can only move adjacent to your selected piece, not diagonally. "
                  "Pieces that are not Scouts (2) can only traverse 1 square. Pieces can not move to or through an occupied square (Piece or Water)")
            time.sleep(WAIT_TIME)
            GameState.set_on_coord2(False)
        else:
            if piece_source.get_colour() != piece_destination.get_colour() and piece_destination.get_rank() != EMPTY_CELL:
                tmp_board = attack(tmp_board, y1, x1, y2, x2)
            else:
                tmp_board = update_board(tmp_board, y2, x2, piece_source)
            tmp_board = update_board(tmp_board, y1, x1, Piece(EMPTY_CELL))

            colour = BLUE if colour == RED else RED
            GameState.set_on_coord2(False)

    move_piece_source(colour, tmp_board)


def auto_setup(colour: str, _board: list[list[Piece]]) -> list[list[Piece]]:
    tmp_board: list[list[Piece]] = _board

    for row in range(0, 3) if colour == BLUE else range(5, ROWS_LENGTH):
        for col in range(COLS_LENGTH):
            rnd_piece = bluePieces[random.randint(0, len(bluePieces)-1)] if colour == BLUE else redPieces[random.randint(0, len(redPieces)-1)]
            tmp_board[row][col] = rnd_piece
            bluePieces.remove(rnd_piece) if colour == BLUE else redPieces.remove(rnd_piece)
    return tmp_board


def choose_setup_mode(colour: str, _board: list[list[Piece]]):
    tmp_board: list[list[Piece]] = _board[:]
    choosing: bool = True

    while choosing:
        print_board(colour, tmp_board)
        print(f"\n[{colour}] Would you like us to randomly automate your piece set-up? (Y/N)")
        answer: str = input()

        if answer.upper() == 'Y':
            auto_setup(colour, tmp_board)
        elif answer.upper() == 'N':
            set_up(colour, tmp_board)
        else:
            print(Fore.RED + "Invalid answer. Please answer with 'Y' or 'N'")
            continue
        print_board(colour, tmp_board)
        print()
        choosing = False


# INITIAL BOARD STATE- ROWS: 8, COLUMNS: 10, CONTENT: '0'
board: list[list[Piece]] = init_board(Piece(EMPTY_CELL), 8, 10)
board = add_water(board, Piece(WATER))
ROWS_LENGTH: int = len(board)
COLS_LENGTH: int = len(board[0])

# INITIAL GAME STATE
GameState = GameState(RED, False, False)


def start(colour: str, _board: list[list[Piece]]):
    tmp_board: list[list[Piece]] = _board[:]

    choose_setup_mode(colour, tmp_board)
    colour = BLUE
    choose_setup_mode(colour, tmp_board)

    colour = RED
    GameState.set_is_playing(True)

    move_piece_source(colour, tmp_board)


if __name__ == '__main__':
    start(GameState.get_colour(), board)
