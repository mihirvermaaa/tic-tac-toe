#!/usr/bin/env python3
"""
Tic-Tac-Toe — Interactive Terminal & Desktop Game Engine
========================================================
A lightweight, zero-dependency Tic-Tac-Toe application written in Python 3.

Features:
- Rich Unicode box-drawing terminal UI with automatic ANSI color detection
- Live multi-round session scoreboard (X Wins, O Wins, Draws)
- Strict try-except input sanitization and occupied-cell protection
- Complete 8-line win evaluation with winning-line highlighting
- Optional dark-themed Tkinter desktop GUI mode (`python tic_tac_toe.py --gui`)
"""

import os
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

# Enable ANSI colors automatically in interactive terminals (disabled in pipes/tests)
USE_COLOR = sys.stdout.isatty() and os.environ.get("NO_COLOR") is None

RESET = "\033[0m" if USE_COLOR else ""
BOLD = "\033[1m" if USE_COLOR else ""
DIM = "\033[2m" if USE_COLOR else ""
CYAN = "\033[96m" if USE_COLOR else ""
CORAL = "\033[91m" if USE_COLOR else ""
GREEN = "\033[92m" if USE_COLOR else ""
YELLOW = "\033[93m" if USE_COLOR else ""


# =============================================================================
# 1. Board Management & Terminal UI Module
# =============================================================================
def create_board():
    """Initializes and returns an empty 9-cell board as a 1D Python list."""
    return [" "] * 9


def format_cell(board, index, winning_indices=None):
    """Formats a single board cell with optional ANSI color and win highlight."""
    mark = board[index]
    if mark == " ":
        return f"{DIM}{index + 1}{RESET}"
    if winning_indices and index in winning_indices:
        return f"{BOLD}{GREEN}{mark}{RESET}"
    if mark == "X":
        return f"{BOLD}{CYAN}X{RESET}"
    return f"{BOLD}{CORAL}O{RESET}"


def display_board(board, winning_indices=None):
    """
    Renders the 9-element board list into a clean Unicode box-drawing 3x3 grid.
    Empty cells show their position number (1-9); occupied cells show X or O.
    """
    print()
    print("    ┌───┬───┬───┐")
    for row in range(3):
        start = row * 3
        c0 = format_cell(board, start, winning_indices)
        c1 = format_cell(board, start + 1, winning_indices)
        c2 = format_cell(board, start + 2, winning_indices)
        print(f"    │ {c0} │ {c1} │ {c2} │")
        if row < 2:
            print("    ├───┼───┼───┤")
    print("    └───┴───┴───┘")
    print()


def display_header(scores, round_num):
    """Prints the game title banner and live session scoreboard."""
    print("\n  ╔═══════════════════════════════════════════╗")
    print(f"  ║        {BOLD}TIC-TAC-TOE  •  ROUND #{round_num:<2}{RESET}          ║")
    print("  ╠═══════════════════════════════════════════╣")
    print(
        f"  ║   {CYAN}Player X: {scores['X']:<2}{RESET}  │  "
        f"{CORAL}Player O: {scores['O']:<2}{RESET}  │  "
        f"{YELLOW}Draws: {scores['Draws']:<2}{RESET} ║"
    )
    print("  ╚═══════════════════════════════════════════╝")


# =============================================================================
# 2. Input Validation Module
# =============================================================================
def take_move(board, current_player):
    """
    Prompts the active player for a position (1-9), validates input via a
    while loop and try-except block, checks cell availability, and updates the
    board list.
    """
    player_tag = (
        f"{BOLD}{CYAN}X{RESET}"
        if current_player == "X"
        else f"{BOLD}{CORAL}O{RESET}"
    )
    while True:
        raw_input_val = input(
            f"  Player {player_tag}, enter your move (1-9): "
        ).strip()

        try:
            position = int(raw_input_val)
        except ValueError:
            print("  Invalid position. Enter a number from 1 to 9.")
            continue

        if position < 1 or position > 9:
            print("  Invalid position. Enter a number from 1 to 9.")
            continue

        index = position - 1
        if board[index] != " ":
            print(f"  Position {position} is already taken. Choose another position.")
            continue

        board[index] = current_player
        return position


# =============================================================================
# 3. Win/Draw Detection Module
# =============================================================================
def check_win(board, player):
    """
    Checks all 8 winning combinations (3 rows, 3 columns, 2 diagonals).
    Returns a tuple of (winning_line_str, winning_indices_tuple) if the player
    has won, or (None, None) otherwise.
    """
    for a, b, c in WINNING_COMBINATIONS:
        if board[a] == board[b] == board[c] == player:
            return f"{a + 1}-{b + 1}-{c + 1}", (a, b, c)
    return None, None


def check_draw(board):
    """Returns True if all 9 cells on the board are occupied."""
    return " " not in board


# =============================================================================
# 4. Game Loop Control Module
# =============================================================================
def ask_play_again():
    """Prompts players whether to start another round via a (y/n) prompt."""
    while True:
        choice = input("\n  Play again? (y/n): ").strip().lower()
        if choice in ("y", "yes"):
            return True
        if choice in ("n", "no"):
            return False
        print("  Invalid choice. Please enter 'y' or 'n'.")


def play_round(scores, round_num):
    """Executes a single round of Tic-Tac-Toe starting with Player X."""
    board = create_board()
    current_player = "X"

    display_header(scores, round_num)
    display_board(board)

    while True:
        take_move(board, current_player)
        winning_line, win_indices = check_win(board, current_player)

        display_board(board, winning_indices=win_indices)

        if winning_line is not None:
            scores[current_player] += 1
            print(f"  {BOLD}{GREEN}Player {current_player} wins!{RESET}")
            print(f"  Winning line: {winning_line}")
            break

        if check_draw(board):
            scores["Draws"] += 1
            print("  Board is full after 9 moves.")
            print(f"  {BOLD}{YELLOW}It's a draw! No moves left.{RESET}")
            break

        current_player = "O" if current_player == "X" else "X"


# =============================================================================
# 5. Optional Desktop GUI Mode (--gui)
# =============================================================================
def launch_gui():
    """Launches a modern dark-slate Tkinter desktop interface."""
    import tkinter as tk

    root = tk.Tk()
    root.title("Tic-Tac-Toe")
    root.configure(bg="#0f172a")
    root.resizable(False, False)

    board = create_board()
    state = {"player": "X", "game_over": False, "X": 0, "O": 0, "Draws": 0}
    buttons = []

    header = tk.Label(
        root,
        text="TIC-TAC-TOE",
        font=("Helvetica", 18, "bold"),
        fg="#f8fafc",
        bg="#0f172a",
        pady=10,
    )
    header.pack()

    score_label = tk.Label(
        root,
        text="Player X: 0   |   Player O: 0   |   Draws: 0",
        font=("Helvetica", 11, "bold"),
        fg="#94a3b8",
        bg="#1e293b",
        padx=18,
        pady=6,
    )
    score_label.pack(padx=20, pady=(0, 10), fill="x")

    status_label = tk.Label(
        root,
        text="Player X's turn",
        font=("Helvetica", 12, "bold"),
        fg="#38bdf8",
        bg="#0f172a",
        pady=4,
    )
    status_label.pack()

    grid_frame = tk.Frame(root, bg="#0f172a", padx=20, pady=10)
    grid_frame.pack()

    def update_scoreboard():
        score_label.config(
            text=f"Player X: {state['X']}   |   Player O: {state['O']}   |   Draws: {state['Draws']}"
        )

    def on_cell_click(idx):
        if state["game_over"] or board[idx] != " ":
            return

        p = state["player"]
        board[idx] = p
        color = "#38bdf8" if p == "X" else "#f43f5e"
        buttons[idx].config(text=p, fg=color, bg="#1e293b")

        winning_line, win_indices = check_win(board, p)
        if winning_line is not None:
            state["game_over"] = True
            state[p] += 1
            for w_idx in win_indices:
                buttons[w_idx].config(bg="#14532d", fg="#4ade80")
            status_label.config(
                text=f"Player {p} wins! (Line: {winning_line})", fg="#4ade80"
            )
            update_scoreboard()
            return

        if check_draw(board):
            state["game_over"] = True
            state["Draws"] += 1
            status_label.config(
                text="It's a draw! No moves left.", fg="#facc15"
            )
            update_scoreboard()
            return

        state["player"] = "O" if p == "X" else "X"
        next_color = "#38bdf8" if state["player"] == "X" else "#f43f5e"
        status_label.config(text=f"Player {state['player']}'s turn", fg=next_color)

    for i in range(9):
        btn = tk.Button(
            grid_frame,
            text=str(i + 1),
            font=("Helvetica", 20, "bold"),
            width=4,
            height=2,
            bg="#1e293b",
            fg="#475569",
            activebackground="#334155",
            relief="flat",
            bd=0,
            command=lambda idx=i: on_cell_click(idx),
        )
        btn.grid(row=i // 3, column=i % 3, padx=5, pady=5)
        buttons.append(btn)

    def reset_round():
        for i in range(9):
            board[i] = " "
            buttons[i].config(text=str(i + 1), bg="#1e293b", fg="#475569")
        state["player"] = "X"
        state["game_over"] = False
        status_label.config(text="Player X's turn", fg="#38bdf8")

    reset_btn = tk.Button(
        root,
        text="Play Again / New Round",
        font=("Helvetica", 11, "bold"),
        bg="#2563eb",
        fg="#ffffff",
        activebackground="#1d4ed8",
        activeforeground="#ffffff",
        relief="flat",
        padx=16,
        pady=8,
        command=reset_round,
    )
    reset_btn.pack(pady=(6, 18))

    root.mainloop()


def main():
    """Main entry point supporting CLI mode (default) and GUI mode (--gui)."""
    if "--gui" in sys.argv:
        launch_gui()
        return

    scores = {"X": 0, "O": 0, "Draws": 0}
    round_num = 1
    while True:
        play_round(scores, round_num)
        if not ask_play_again():
            print("  Thanks for playing!")
            break
        round_num += 1


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\n  Game exited. Thanks for playing!")
        sys.exit(0)