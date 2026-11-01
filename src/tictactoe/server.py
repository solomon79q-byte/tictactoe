import argparse
import json
import socket
from collections.abc import Callable
from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt, IntPrompt

from .game import Game


DEFAULT_HOST = "0.0.0.0"
DEFAULT_PORT = 54321


console = Console()

class TCPGameServer:
    """Authoritative TCP server for a single Tic-Tac-Toe game."""

    def __init__(
        self,
        game: Game,
        host: str = DEFAULT_HOST,
        port: int = DEFAULT_PORT,
        host_move_provider: Callable[[dict], int] | None = None,
    ) -> None:
        self.game = game
        self.host = host
        self.port = port
        self.host_move_provider = host_move_provider
        self._current_mark = "X"
        self._status = "in_progress"
        self._last_move: dict | None = None

    def _state(self, error: str | None = None) -> dict:
        state = {
            "type": "state",
            "board": self.game.board.copy(),
            "current_player": self._current_mark,
            "current_player_name": self.game.current_player,
            "status": self._status,
            "winner": self.game.current_winner,
            "available_moves": [index + 1 for index in self.game.available_moves()],
            "players": {"X": self.game.player1, "O": self.game.player2},
            "last_move": self._last_move,
            "stats": {
                "player1_wins": self.game.player1_wins,
                "player2_wins": self.game.player2_wins,
                "draws": self.game.draws,
            },
        }
        if error is not None:
            state["error"] = error
        return state

    @staticmethod
    def _send_json(connection: socket.socket, message: dict) -> None:
        payload = json.dumps(message, separators=(",", ":")) + "\n"
        connection.sendall(payload.encode("utf-8"))

    def _apply_move(self, square: object, mark: str) -> str | None:
        if self._status != "in_progress":
            return "The game is already over."
        if mark != self._current_mark:
            return "It is not your turn."
        if isinstance(square, bool) or not isinstance(square, int) or not 1 <= square <= 9:
            return "Move must be a board position from 1 to 9."

        board_index = square - 1
        if not self.game.make_move(board_index, mark):
            return "That position is already occupied."

        self._last_move = {"square": square, "player": mark}
        if self.game.current_winner:
            self._status = "won"
            if mark == "X":
                self.game.player1_wins += 1
            else:
                self.game.player2_wins += 1
        elif self.game.check_full_board():
            self._status = "draw"
            self.game.draws += 1
        else:
            self._current_mark = "O" if mark == "X" else "X"
            self.game.current_player = (
                self.game.player1 if self._current_mark == "X" else self.game.player2
            )
        return None

    def _host_turn(self) -> None:
        while True:
            if self.host_move_provider is not None:
                square = self.host_move_provider(self._state())
            else:
                self.game.print_board()
                try:
                    square = IntPrompt.ask(f"{self.game.current_player}, choose your move (1-9): ", choices=[str(i) for i in range(1, 10)])
                except ValueError:
                    console.print("Enter a number from 1 to 9.", style="red")
                    continue

            error = self._apply_move(square, "X")
            if error is None:
                return
            console.print(error, style="red")

    def serve_forever(self) -> None:
        """Accept one guest and host the game until it ends or disconnects."""
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as listener:
            listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            listener.bind((self.host, self.port))
            listener.listen(1)
            address, port = listener.getsockname()
            console.print(f"Waiting for a guest on {address}:{port}...")
            connection, guest_address = listener.accept()
            with connection:
                console.print(f"Guest connected from {guest_address}.")
                with connection.makefile("r", encoding="utf-8") as reader:
                    self._send_json(connection, self._state())
                    while True:

                        if self._status == "won":
                            if self._current_mark == "X":
                                console.print(f"You win!", style="green")
                                self.game.print_scoreboard()
                            else:
                                 console.print(f"You lose!", style="red")
                                 self.game.print_scoreboard()
                        elif self._status == "draw":
                            console.print("It's a draw!", style="yellow")
                            self.game.print_scoreboard()
                        

                        if self._status in ["won", "draw"]:
                            if self.game.replay():
                                self.game.next_play()
                                self._current_mark = "X"
                                self._status = "in_progress"
                                self._last_move = None
                                continue
                            else:
                                console.print("Exiting...", style="red")
                                return
                    

                        if self._current_mark == "X":
                            self._host_turn()
                            self.game.print_board()
                            console.print(f"Waiting for {self.game.player2} (O) to move...")
                            self._send_json(connection, self._state())
                            continue

                        line = reader.readline()
                        if not line:
                            print("Guest disconnected.")
                            return
                        try:
                            request = json.loads(line)
                        except json.JSONDecodeError:
                            self._send_json(
                                connection,
                                self._state("Request must be a valid JSON object."),
                            )
                            continue

                        if not isinstance(request, dict) or request.get("type") != "move":
                            self._send_json(
                                connection,
                                self._state('Request type must be "move".'),
                            )
                            continue

                        error = self._apply_move(request.get("square"), "O")
                        self._send_json(connection, self._state(error))


                        
                
                    


def main() -> None:
    parser = argparse.ArgumentParser(description="Host a Tic-Tac-Toe game over TCP.")
    parser.add_argument("--host", default=DEFAULT_HOST, help="Address to bind (default: all interfaces)")
    parser.add_argument("--port", type=int, default=DEFAULT_PORT)
    parser.add_argument("--player", default="Host", help="Host player's name")
    parser.add_argument("--guest", default="Guest", help="Guest player's name")
    args = parser.parse_args()
    TCPGameServer(Game(args.player, args.guest), args.host, args.port).serve_forever()


if __name__ == "__main__":
    main()
