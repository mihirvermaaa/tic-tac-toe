# Tic-Tac-Toe — Interactive CLI & Desktop Game Engine

A lightweight, zero-dependency Tic-Tac-Toe game built in pure Python 3. Designed with a clean modular architecture featuring a box-drawing terminal interface, automatic ANSI color styling, live multi-round score tracking, and an optional dark-themed Tkinter desktop GUI.

## Features

- **Polished Terminal UI:** Renders the 3×3 board using crisp Unicode box-drawing frames (`┌───┬───┬───┐`), color-coded player marks (`X` in cyan, `O` in coral), and green highlights on winning lines.
- **Live Session Scoreboard:** Tracks Player X wins, Player O wins, and Draws across consecutive rounds.
- **Desktop GUI Mode (`--gui`):** Includes a built-in dark-slate Tkinter desktop interface with interactive tiles and score tracking.
- **Strict Input Sanitization:** Validates every move via `try-except` parsing, enforcing the `1–9` range and preventing overwrites on occupied cells without losing the active player's turn.
- **Zero External Dependencies:** Runs out of the box on Python 3.8+ using only the Python standard library.

## Quickstart

### 1. Run in Terminal (Default CLI Mode)

```bash
python tic_tac_toe.py
```

### 2. Run Desktop Window (GUI Mode)

```bash
python tic_tac_toe.py --gui
```

## Terminal Preview

```text
  ╔═══════════════════════════════════════════╗
  ║        TIC-TAC-TOE  •  ROUND #1           ║
  ╠═══════════════════════════════════════════╣
  ║   Player X: 1   │  Player O: 0   │  Draws: 0  ║
  ╚═══════════════════════════════════════════╝

    ┌───┬───┬───┐
    │ X │ X │ X │
    ├───┼───┼───┤
    │ O │ O │ 6 │
    ├───┼───┼───┤
    │ 7 │ 8 │ 9 │
    └───┴───┴───┘

  Player X wins!
  Winning line: 1-2-3
```

## Architecture Overview

| Module / Function | Responsibility |
| :--- | :--- |
| `create_board()` | Initializes the 9-cell 1D state list (`[" "] * 9`). |
| `display_board()` | Renders the 3×3 Unicode grid with position guides and winning-line highlights. |
| `take_move()` | Prompts the active player, validates `1–9` integer bounds, and prevents duplicate moves. |
| `check_win()` | Evaluates all 8 winning index tuples (3 rows, 3 columns, 2 diagonals) in O(1) time. |
| `check_draw()` | Detects full-board stalemates when all 9 cells are occupied with no winner. |
| `launch_gui()` | Launches the optional dark-mode Tkinter desktop interface (`--gui`). |

## Verified Scenarios

| Scenario | Move Sequence | Expected Outcome |
| :--- | :--- | :--- |
| **Horizontal Win** | `X:1, O:4, X:2, O:5, X:3` | `Player X wins!` (`Winning line: 1-2-3`) |
| **Full-Board Draw** | `X:1, O:2, X:3, O:5, X:4, O:6, X:8, O:7, X:9` | `Board is full after 9 moves.` / `It's a draw! No moves left.` |
| **Input Validation** | `10`, `abc`, or already occupied cell `1` | Rejects invalid input with clear error prompt and retains turn |
| **Middle-Row Win & Exit** | `X:1, O:4, X:2, O:5, X:9, O:6`, Replay: `n` | `Player O wins!` (`Winning line: 4-5-6`) / `Thanks for playing!` |
