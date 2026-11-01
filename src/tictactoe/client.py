import argparse
import json
import socket
from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt, IntPrompt

console = Console()

class TCPGameClient:
    """TCP client for the guest player in a hosted Tic-Tac-Toe game."""

    def __init__(self, host: str, port: int = 54321) -> None:
        self.host = host
        self.port = port
        self._socket: socket.socket | None = None
        self._reader = None

    def connect(self) -> dict:
        if self._socket is not None:
            raise RuntimeError("Client is already connected.")
        self._socket = socket.create_connection((self.host, self.port))
        self._reader = self._socket.makefile("r", encoding="utf-8")
        return self.receive_state()

    def receive_state(self) -> dict:
        if self._reader is None:
            raise RuntimeError("Connect to a game server before receiving state.")
        line = self._reader.readline()
        if not line:
            raise ConnectionError("The game server disconnected.")
        try:
            message = json.loads(line)
        except json.JSONDecodeError as error:
            raise ValueError("The server sent invalid JSON.") from error
        if not isinstance(message, dict) or message.get("type") != "state":
            raise ValueError("The server sent an invalid game-state message.")
        return message

    def make_move(self, square: int) -> dict:
        if self._socket is None:
            raise RuntimeError("Connect to a game server before making a move.")
        request = json.dumps({"type": "move", "square": square}) + "\n"
        self._socket.sendall(request.encode("utf-8"))
        return self.receive_state()

    def close(self) -> None:
        if self._reader is not None:
            self._reader.close()
            self._reader = None
        if self._socket is not None:
            self._socket.close()
            self._socket = None

    def __enter__(self) -> "TCPGameClient":
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        self.close()


def _print_state(state: dict) -> None:
    board = state["board"]
    console.print()
    console.print(f" {board[0]} | {board[1]} | {board[2]}")
    console.print("---+---+---")
    console.print(f" {board[3]} | {board[4]} | {board[5]}")
    console.print("---+---+---")
    console.print(f" {board[6]} | {board[7]} | {board[8]}")
    console.print()
    if "error" in state:
        console.print(state["error"], style="red")
    if state["status"] == "won":
        if state["winner"] == "O":
            console.print("You win!", style="green")
            print_scoreboard(state)
        else:
            console.print(f"You lose!", style="red")
            print_scoreboard(state)
    elif state["status"] == "draw":
        console.print("It's a draw!", style="yellow")
        print_scoreboard(state)
    elif state["current_player"] == "O":
        console.print("Your turn (O).", style="blue")
    else:
        console.print(f"Waiting for {state['players']['X']} (X) to move...", style="magenta")


def play(host: str, port: int) -> None:
    with TCPGameClient(host, port) as client:
        state = client.connect()
        while True:
            _print_state(state)
            if state["status"] != "in_progress":
                if replay():
                    state = client.receive_state()
                    _print_state(state)
                    continue
                else:
                    return
            if state["current_player"] == "O":
                try:
                    square = IntPrompt.ask("Choose a position from 1-9", choices=[str(i) for i in range(1, 10)])
                except ValueError:
                    console.print("Enter a number from 1 to 9.", style="red")
                    continue
                state = client.make_move(square)
            else:
                state = client.receive_state()

        

def replay() -> None:
    exit_choice = Prompt.ask("[green]Press [blue]Enter[/blue] to play again or type [blue]q[/blue] to quit: [/green]", default="")
    if exit_choice.lower() != "q":
        return True
    return False

def main() -> None:
    host = "127.0.0.1"
    play(host, 54321)


def print_scoreboard(state: dict) -> None:
    table = Table(title="Scoreboard")
    table.add_column("Player", style="cyan", no_wrap=True)
    table.add_column("Wins", style="green")
    table.add_column("Draws", style="yellow")
    table.add_column("Losses", style="red")

    table.add_row(state["players"]["X"], str(state["stats"]["player1_wins"]), str(state["stats"]["draws"]), str(state["stats"]["player2_wins"]))
    table.add_row(state["players"]["O"], str(state["stats"]["player2_wins"]), str(state["stats"]["draws"]), str(state["stats"]["player1_wins"]))


    console.print(table)


if __name__ == "__main__":
    main()
