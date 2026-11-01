# Tic-Tac-Toe CLI

A small Python project for playing Tic-Tac-Toe in several modes:

- against a CPU opponent
- with a second human player on the same machine
- over a local network with a host and guest connection

The app uses the `rich` library to render a polished terminal interface and keeps score across rounds.

## Features

- Single-player mode against an AI opponent
- Two-player local pass-and-play mode
- LAN multiplayer support using UDP discovery + TCP gameplay
- Scoreboard tracking for wins, losses, and draws
- Replay flow after each round
- Simple board-numbered input using positions 1 through 9

## Project overview

This project is organized around a reusable game engine and multiple play flows:

- `src/tictactoe/main.py` launches the interactive menu
- `src/tictactoe/game.py` contains the core board logic and score tracking
- `src/tictactoe/play_with_cpu.py` handles human-vs-computer mode
- `src/tictactoe/minimax.py` implements the CPU decision logic
- `src/tictactoe/two_players.py` handles local two-player mode
- `src/tictactoe/server.py` runs the authoritative TCP game server for LAN play
- `src/tictactoe/client.py` connects a guest player to the server
- `src/tictactoe/udp.py` provides room discovery for LAN matchmaking

## Getting started

### Prerequisites

- Python 3.15 or newer
- `uv` is recommended for dependency management, but `pip` also works

### Install dependencies

```bash
uv sync
```

Or with pip:

```bash
python -m pip install -e .
```

## Running the game

Start the interactive menu:

```bash
python -m tictactoe.main
```

If you are using `uv`, this is also valid:

```bash
uv run python -m tictactoe.main
```

## Menu options

When the program starts, you will see a menu with these choices:

1. Play against CPU
2. Play against another player
3. Play over LAN (host)
4. Play over LAN (guest)
5. Exit

## How to play

The board is numbered from 1 to 9:

```text
 1 | 2 | 3
---+---+---
 4 | 5 | 6
---+---+---
 7 | 8 | 9
```

Choose the number corresponding to the square you want to claim.

## LAN multiplayer

LAN mode uses a room code to match players on the same network.

### Host

1. Run the app and choose `3. Play over LAN (host)`
2. Enter a room code
3. The host waits for a guest to connect

### Guest

1. Run the app and choose `4. Play over LAN (guest)`
2. Enter the same room code
3. The guest discovers the host on the local network and connects

The host plays as `X` and the guest plays as `O`. The server validates each move and sends updated game state back to the client after each turn.

## Notes

- The CPU difficulty is selected from 1 (easy), 2 (medium), or 3 (hard)
- The scoreboard persists for the current round session until you exit the game
- The project is intentionally lightweight and designed for terminal-based play

## License

This project is provided as a local learning/demo project and does not currently include a formal license file.