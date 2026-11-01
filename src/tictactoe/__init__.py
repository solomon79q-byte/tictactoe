from .game import Game


def main() -> None:
    print("Hello from tictactoe!")
    game = Game("Player 1", "Player 2")
    game.print_board()
    game.print_board_nums()