import Piece
from Piece import *
from gameState import *
import colorama
from colorama import Fore, Back
import sys
import random
import time
colorama.init(autoreset=True)

water =' W'
blue = "blue"
red = "red"
mar = '10'
gen = ' 9'
cnl = ' 8'
maj = ' 7'
cap = ' 6'
lie = ' 5'
ser = ' 4'
mnr = ' 3'
sco = ' 2'
spy = ' 1'
bom = ' B'
fla = ' F'
empty_cell = ' 0'
wait_time = 1

piece_names = [
    "Marshal : 10", "General : 9", "Colonel : 8", "2nd Colonel : 8", "Major : 7", "2nd Major : 7", "3rd Major : 7",
    "Captain : 6", "2nd Captain : 6", "3rd Captain : 6", "Lieutenant : 5", "2nd Lieutenant : 5", "Sergeant : 4",
    "2nd Sergeant : 4", "Miner : 3", "2nd Miner : 3", "3rd Miner : 3", "4th Miner : 3", "Scout : 2", "2nd Scout : 2",
    "3rd Scout : 2", "4th Scout : 2", "5th Scout : 2", "Bomb", "2nd Bomb", "3rd Bomb", "4th Bomb", "5th Bomb",
    "Spy : 1", "Flag"
]

red_pieces = [
    Piece(mar, red), Piece(gen, red), Piece(cnl, red), Piece(cnl, red), Piece(maj, red), Piece(maj, red),
    Piece(maj, red), Piece(cap, red), Piece(cap, red), Piece(cap, red), Piece(lie, red), Piece(lie, red),
    Piece(ser, red), Piece(ser, red), Piece(mnr, red), Piece(mnr, red), Piece(mnr, red), Piece(mnr, red),
    Piece(sco, red), Piece(sco, red), Piece(sco, red), Piece(sco, red), Piece(sco, red), Piece(bom, red),
    Piece(bom, red), Piece(bom, red), Piece(bom, red), Piece(bom, red), Piece(spy, red), Piece(fla, red)
]

blue_pieces = [
    Piece(mar, blue), Piece(gen, blue), Piece(cnl, blue), Piece(cnl, blue), Piece(maj, blue), Piece(maj, blue),
    Piece(maj, blue), Piece(cap, blue), Piece(cap, blue), Piece(cap, blue), Piece(lie, blue), Piece(lie, blue),
    Piece(ser, blue), Piece(ser, blue), Piece(mnr, blue), Piece(mnr, blue), Piece(mnr, blue), Piece(mnr, blue),
    Piece(sco, blue), Piece(sco, blue), Piece(sco, blue), Piece(sco, blue), Piece(sco, blue), Piece(bom, blue),
    Piece(bom, blue), Piece(bom, blue), Piece(bom, blue), Piece(bom, blue), Piece(spy, blue), Piece(fla, blue)
]

letter_to_nums = {
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
    tmp_board = _board[:]
    tmp_board[3][2] = water
    tmp_board[4][2] = water
    tmp_board[3][3] = water
    tmp_board[4][3] = water
    tmp_board[3][6] = water
    tmp_board[4][6] = water
    tmp_board[3][7] = water
    tmp_board[4][7] = water

    return tmp_board

def print_board(colour: str, _board: list[list[Piece]] ):
    print("  |  0  1  2  3  4  5  6  7  8  9")
    print("- - - - - - - - - - - - - - - - -")

    for row in range(rows_length):
        for col in range(-1, cols_length):

            if col == -1:
                letters = list(letter_to_nums)
                print(letters[row] + " | ", end='')
            else:
                cell = _board[row][col]
                anon = ' S'

                if cell.get_colour() == red:
                    if colour == blue:
                        print(Fore.RED + anon, end=' ')
                    else:
                        print(Fore.RED + cell.get_rank(), end=' ')
                elif cell.get_colour() == blue:
                    if colour == red:
                        print(Fore.BLUE + anon, end=' ')
                    else:
                        print(Fore.BLUE + cell.get_rank(), end=' ')
                else:
                    if cell.get_rank() == water:
                        water_val = cell.get_rank()
                        print(Back.CYAN + water_val, end=' ')
                    else:
                        print(cell.get_rank(), end=' ')
        print()

def valid_place(colour: str, _board: list[list[Piece]], y: int, x: int) -> bool:
    cell = _board[y][x]

    if colour == red:
        if y >= 5 and 0 <= x <= 9:
            return cell.get_rank() == empty_cell
    elif colour == blue:
        if y <= 2 and 0 <= x <= 9:
            return cell.get_rank() == empty_cell
    return False

def update_board(_board: list[list[Piece]], y: int, x: int, piece: Piece) -> list[list[Piece]]:
    tmp_board = _board[:]
    tmp_board[y][x] = piece
    return tmp_board

def valid_coordinate(letter: str, num: str) -> bool:
    return letter in list(letter_to_nums) and num.isnumeric() and int(num) in range(0, 10)

def set_up(colour: str, _board: list[list[Piece]] ) -> list[list[Piece]]:
    tmp_board = _board[:]
    i: int = 0

    while i < len(piece_names) and not GameState.is_playing():
        print(f"[{colour}] Place your {piece_names[i]}: ")
        print(end='> ')
        coordinate: str = input()

        if len(coordinate) < 2:
            print(Fore.RED + "You did not satisfy enough values for a coordinate. Provide a valid letter and number")
            continue
        letter = coordinate[0].upper()
        num = coordinate[1]

        if not valid_coordinate(letter, num):
            print(Fore.RED + "Invalid coordinate. A valid coordinate must start with a letter from A-H and end with a number from 0-9")
            continue
        num1 = letter_to_nums.get(letter)
        num2 = int(num)

        if not valid_place(colour, tmp_board, num1, num2):
            if colour == red: print(Fore.RED + "Invalid place. Your coordinates should be placed within the bottom 3 rows")
            else: print(Fore.RED + "Invalid place. Your coordinates should be placed within the top 3 rows")
            continue
        else:
            tmp_board = update_board(tmp_board, num1, num2, red_pieces[i]) if colour == red else update_board(tmp_board, num1, num2, blue_pieces[i])
            print_board(colour, tmp_board)
        i += 1
    return tmp_board

def all_invalid(_board: list[list[Piece]], colour: str) -> bool:
    movable = [mar, gen, cnl, maj, cap, lie, ser, mnr, sco, spy]

    for row in range(rows_length):
        for col in range(cols_length):
            piece: Piece = _board[row][col]

            if piece.get_colour() == colour and piece.get_rank() in movable:
                return False
    return True

def valid_move(_board: list[list[Piece]], y1: int, x1: int, y2: int, x2: int) -> bool:
    tmp_board = _board[:]
    source = board[y1][x1]
    destination = board[y2][x2]
    source_colour = source.get_colour()
    valid_destination = destination.get_colour() != source_colour and destination.get_rank() != water

    if valid_destination:
        if source.get_rank() == sco:
            pieces_crossed = []

            if x1 == x2 and y1 != y2:
                for p in range(y1+1, y2):
                    pieces_crossed.append(tmp_board[p][x1])
                valid_path = all(p.get_rank() == empty_cell for p in pieces_crossed)

                return valid_path
            elif y1 == y2 and x1 != x2:
                for p in range(x1+1, x2+1):
                    pieces_crossed.append(tmp_board[y1][p])
                valid_path = all(p.get_rank() == empty_cell for p in pieces_crossed)

                return valid_path
        else:
            if x1 == x2 and y1 != y2 and abs(y2 - y1) <= 1:
                return True
            elif y1 == y2 and x1 != x2 and abs(x2 - x1) <= 1:
                return True
    return False

def attack(_board: list[list[Piece]], y1: int, x1: int, y2: int, x2: int) -> list[list[Piece]]:
    tmp_board = _board[:]
    source_piece = tmp_board[y1][x1]
    destination_piece = tmp_board[y2][x2]
    source = tmp_board[y1][x1].get_rank()
    destination = tmp_board[y2][x2].get_rank()

    if destination == bom:
        if source == mnr:
            tmp_board = update_board(tmp_board, y2, x2, source_piece)
            print(f"{Fore.YELLOW}{source_piece.get_colour()} piece #{source_piece.get_rank()} has disarmed {destination_piece.get_colour()} piece #{destination_piece.get_rank()}")
            time.sleep(wait_time)

            return tmp_board
        else:
            tmp_board = update_board(tmp_board, y1, x1, Piece(empty_cell))
            print(f"{Fore.YELLOW}{destination_piece.get_colour()} piece #{destination_piece.get_rank()} has defeated {source_piece.get_colour()} piece #{source_piece.get_rank()}")
            time.sleep(wait_time)

            return tmp_board
    elif destination == fla:
        print(f"{Fore.YELLOW}Congratulations {source_piece.get_colour}! You have successfully captured the opponent's flag and won the game!")
        GameState.set_is_playing(False)
        sys.exit()
    else:
        source_val = int(source)
        destination_val = int(destination)

        if destination_val > source_val:
            if source == spy and destination_val % int(mar) == 0:
                tmp_board = update_board(tmp_board, y2, x2, source_piece)
                print(f"{Fore.YELLOW}{source_piece.get_colour()} piece #{source_piece.get_rank()} has defeated {destination_piece.get_colour()} piece #{destination_piece.get_rank()}")
                time.sleep(wait_time)

                return tmp_board
            else:
                print(f"{Fore.YELLOW}{destination_piece.get_colour()} piece #{destination_piece.get_rank()} has defeated {source_piece.get_colour()} piece #{source_piece.get_rank()}")
                time.sleep(wait_time)

                return tmp_board
        elif source_val > destination_val:
            tmp_board = update_board(tmp_board, y2, x2, source_piece)
            print(f"{Fore.YELLOW}{source_piece.get_colour()} piece #{source_piece.get_rank()} has defeated {destination_piece.get_colour()} piece #{destination_piece.get_rank()}")
            time.sleep(wait_time)

            return tmp_board
        elif source_val == destination_val:
            tmp_board = update_board(tmp_board, y2, x2, Piece(empty_cell))
            print(f"{Fore.YELLOW}Tie! {source_piece.get_colour()} and {destination_piece.get_colour()} has both lost piece #{source}")
            time.sleep(wait_time)

            return tmp_board

def valid_source_piece(colour: str, piece: Piece) -> bool:
    rejects = [empty_cell, water, bom, fla]
    return piece.get_rank() not in rejects and piece.get_colour() == colour

def move_piece_source(colour: str, _board: list[list[Piece]]):
    tmp_board = _board

    while GameState.is_playing() and not GameState.on_coord2():
        if all_invalid(tmp_board, blue):
            print(f"{Fore.YELLOW}Congratulations {red}! Your opponent can not move or attack!")
            GameState.set_is_playing(False)
            sys.exit()
        elif all_invalid(tmp_board, red):
            print(f"{Fore.YELLOW}Congratulations {blue}! Your opponent can not move or attack!")
            GameState.set_is_playing(False)
            sys.exit()
        print(f"\n[{colour}] Input the first coordinate that represents the piece you will move\n")
        print_board(colour, tmp_board)
        print()
        print(end='> ')
        coordinate: str = input()

        if len(coordinate) < 2:
            print(Fore.RED + "You did not satisfy enough values for a coordinate. Provide a valid letter and number")
            time.sleep(wait_time)
            continue
        letter = coordinate[0].upper()
        num = coordinate[1]

        if not valid_coordinate(letter, num):
            print(Fore.RED + "Invalid coordinate. A valid coordinate must start with a letter from A-H and end with a number from 0-9")
            time.sleep(wait_time)
            continue
        y1 = letter_to_nums.get(letter)
        x1 = int(num)
        piece_source = tmp_board[y1][x1]

        if not valid_source_piece(colour, piece_source):
            print(f"{Fore.RED}Invalid piece. Select only a {colour} piece that is not a bomb or a flag. Bombs and flags can not be moved")
            time.sleep(wait_time)
            continue
        GameState.set_on_coord2(True)
        move_piece_destination(colour, tmp_board, y1, x1)

def move_piece_destination(colour: str, _board: list[list[Piece]], y1: int, x1: int):
    tmp_board = _board[:]

    while GameState.is_playing() and GameState.on_coord2():
        print("Input the second coordinate that represents the destination of your selected piece: ")
        print(end='> ')
        coordinate = input()

        if len(coordinate) < 2:
            print(Fore.RED + "You did not satisfy enough values for a coordinate. Provide a valid letter and number")
            time.sleep(wait_time)
            continue
        letter = coordinate[0].upper()
        num = coordinate[1]

        if not valid_coordinate(letter, num):
            print(Fore.RED + "Invalid coordinate. A valid coordinate must start with a letter from A-H and end with a number from 0-9")
            time.sleep(wait_time)
            continue
        y2 = letter_to_nums.get(letter)
        x2 = int(num)
        piece_source = tmp_board[y1][x1]
        piece_destination = tmp_board[y2][x2]

        if not valid_move(_board, y1, x1, y2, x2):
            print(Fore.RED + "Invalid move. NOTE: You can only move adjacent to your selected piece, not diagonally. "
                  "Pieces that are not Scouts (2) can only traverse 1 square. Pieces can not move to or through an occupied square (Piece or Water)")
            time.sleep(wait_time)
            GameState.set_on_coord2(False)
        else:
            if piece_source.get_colour() != piece_destination.get_colour() and piece_destination.get_rank() != empty_cell:
                tmp_board = attack(tmp_board, y1, x1, y2, x2)
            else:
                tmp_board = update_board(tmp_board, y2, x2, piece_source)
            tmp_board = update_board(tmp_board, y1, x1, Piece(empty_cell))

            colour = blue if colour == red else red
            GameState.set_on_coord2(False)
    move_piece_source(colour, tmp_board)

def auto_setup(colour: str, _board: list[list[Piece]]) -> list[list[Piece]]:
    tmp_board = _board

    for row in range(0, 3) if colour == blue else range(5, rows_length):
        for col in range(cols_length):
            rnd_piece = blue_pieces[random.randint(0, len(blue_pieces)-1)] if colour == blue else red_pieces[random.randint(0, len(red_pieces)-1)]
            tmp_board[row][col] = rnd_piece
            blue_pieces.remove(rnd_piece) if colour == blue else red_pieces.remove(rnd_piece)
    return tmp_board

def choose_setup_mode(colour: str, _board: list[list[Piece]]):
    tmp_board = _board[:]
    choosing = True

    while choosing:
        print_board(colour, tmp_board)
        print(f"\n[{colour}] Would you like us to randomly automate your piece set-up? (Y/N)")
        answer = input()

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

board = init_board(Piece(empty_cell), 8, 10)
board = add_water(board, Piece(water))
rows_length = len(board)
cols_length = len(board[0])
GameState = GameState(red, False, False)

def start(colour: str, _board: list[list[Piece]]):
    tmp_board = _board[:]
    choose_setup_mode(colour, tmp_board)
    colour = blue
    choose_setup_mode(colour, tmp_board)
    colour = red
    GameState.set_is_playing(True)
    move_piece_source(colour, tmp_board)

if __name__ == '__main__':
    start(GameState.get_colour(), board)
