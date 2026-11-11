"""
===============================================================================
Project Title : Tic-Tac-Toe (Problem Statement No. 57)
Course        : Programming Fundamentals and Logic Building Using Python
                (RU-100-01-00021) | Session: 2026-27
Submitted By  : Mihir Nayak (RU-26-01151)
                B.Tech in Computer Science & Engineering (AI & ML with IBM)
Under Guidance: Mr. Priyanshu (IBM SME and EXPERT)
University    : School of Computer Science and Engineering,
                Rungta International Skills University, Bhilai, CG
===============================================================================
Description:
A standalone two-player console Tic-Tac-Toe game on a 3x3 grid stored as a
1D Python list of 9 elements. Players X and O take turns entering positions
1 to 9 (1-2-3 top row, 4-5-6 middle row, 7-8-9 bottom row). Player X always
plays first. After every valid move, the updated board is displayed and
evaluated across all 8 winning lines or for a full-board draw.
===============================================================================
"""

import sys

# Predefined tuple of all 8 winning index combinations (0-based indices)
# 3 horizontal rows, 3 vertical columns, and 2 diagonals
WINNING_COMBINATIONS = (
    (0, 1, 2),  # Top row (1-2-3)
    (3, 4, 5),  # Middle row (4-5-6)
    (6, 7, 8),  # Bottom row (7-8-9)
    (0, 3, 6),  # Left column (1-4-7)
    (1, 4, 7),  # Middle column (2-5-8)
    (2, 5, 8),  # Right column (3-6-9)
    (0, 4, 8),  # Main diagonal (1-5-9)
    (2, 4, 6),  # Anti-diagonal (3-5-7)
)


# =============================================================================
# 1. Board Management Module
# =============================================================================
def create_board():
    """Initializes and returns an empty 9-cell board as a 1D Python list."""
    return [" "] * 9


def display_board(board):
    """
    Formats and prints the 9-element board list as a clean 3x3 ASCII grid.
    Empty cells display their position number (1-9) as a subtle guide, or
    the player's mark ('X' or 'O') once occupied.
    """
    print()
    for row in range(3):
        start = row * 3
        cells = [
            board[start + col] if board[start + col] != " " else str(start + col + 1)
            for col in range(3)
        ]
        print(f"  {cells[0]} | {cells[1]} | {cells[2]} ")
        if row < 2:
            print(" ---+---+---")
    print()


# =============================================================================
# 2. Input Validation Module
# =============================================================================
def take_move(board, current_player):
    """
    Prompts the active player for a position (1-9), validates the input using
    a while loop and try-except block, ensures the cell is unoccupied, and
    commits the move to the board list.
    """
    while True:
        raw_input_val = input(
            f"Player {current_player}, enter your move (1-9): "
        ).strip()

        try:
            position = int(raw_input_val)
        except ValueError:
            print("Invalid position. Enter a number from 1 to 9.")
            continue

        if position < 1 or position > 9:
            print("Invalid position. Enter a number from 1 to 9.")
            continue

        index = position - 1
        if board[index] != " ":
            print(f"Position {position} is already taken. Choose another position.")
            continue

        board[index] = current_player
        return position


# =============================================================================
# 3. Win/Draw Detection Module
# =============================================================================
def check_win(board, player):
    """
    Checks all 8 possible winning combinations (3 rows, 3 columns, 2 diagonals).
    Returns the formatted winning line string (e.g., '1-2-3') if the player
    has won, or None otherwise.
    """
    for a, b, c in WINNING_COMBINATIONS:
        if board[a] == board[b] == board[c] == player:
            return f"{a + 1}-{b + 1}-{c + 1}"
    return None


def check_draw(board):
    """
    Returns True if all 9 cells on the board are filled (no empty spaces left),
    indicating a draw when no winning line has been detected.
    """
    return " " not in board


# =============================================================================
# 4. Game Loop Control
# =============================================================================
def ask_play_again():
    """
    Prompts the players whether they want to play another round via a (y/n)
    prompt and validates the response.
    """
    while True:
        choice = input("Play again? (y/n): ").strip().lower()
        if choice in ("y", "yes"):
            return True
        if choice in ("n", "no"):
            return False
        print("Invalid choice. Please enter 'y' or 'n'.")


def play_round():
    """Executes a single full round of Tic-Tac-Toe starting with Player X."""
    board = create_board()
    current_player = "X"

    print("\n=========================================")
    print("       TIC-TAC-TOE (Positions 1-9)       ")
    print("=========================================")
    display_board(board)

    while True:
        take_move(board, current_player)
        display_board(board)

        winning_line = check_win(board, current_player)
        if winning_line is not None:
            print(f"Player {current_player} wins!")
            print(f"Winning line: {winning_line}")
            break

        if check_draw(board):
            print("Board is full after 9 moves.")
            print("It's a draw! No moves left.")
            break

        # Switch turns between X and O
        current_player = "O" if current_player == "X" else "X"


def main():
    """Main entry point orchestrating multiple rounds of the game."""
    while True:
        play_round()
        if not ask_play_again():
            print("Thanks for playing!")
            break


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\nGame exited. Thanks for playing!")
        sys.exit(0)