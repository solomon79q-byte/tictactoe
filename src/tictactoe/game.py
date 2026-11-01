from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt, IntPrompt


class Game:
    def __init__(self, player1, player2):
        self.board = [' ' for _ in range(9)]  # Represents the 3x3 board
        self.current_winner = None  # Keep track of the winner!
        self.player1 = player1
        self.player2 = player2
        self.current_player = player1  # Player 1 starts
        self.player1_wins = 0
        self.player2_wins = 0
        self.draws = 0
        self.wining_combinations = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Rows
            [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Columns
            [0, 4, 8], [2, 4, 6]   # Diagonals
        ]


        self.console = Console()

    def print_board(self):
        print()
        print(' ' + self.board[0] + ' | ' + self.board[1] + ' | ' + self.board[2])
        print('---+---+---')
        print(' ' + self.board[3] + ' | ' + self.board[4] + ' | ' + self.board[5])
        print('---+---+---')
        print(' ' + self.board[6] + ' | ' + self.board[7] + ' | ' + self.board[8])
        print()


    def print_board_instructions(self):
        # Tells us what number corresponds to what box  from 1 to 9; i.e. a guide for players
        print()
        print("GAME INSTRUCTIONS:")
        print('On each turn, choose a number from 1-9 to place your mark in the corresponding box:')
        number_board = [[str(i+1) for i in range(j * 3, (j + 1) * 3)] for j in range(3)]
        print()
        for row in number_board:
            print(' ' + ' | '.join(row))
            if row != number_board[-1]:
                print('---+---+---')
        print()
        self.console.input("[green]Press [blue]Enter[/blue] to continue...[/green]")

    def available_moves(self):
        # Returns a list of available moves (indices of empty spots)
        return [i for i, spot in enumerate(self.board) if spot == ' ']

    def make_move(self, square, letter):
        # If valid move, then make the move (assign square to letter)
        if self.board[square] == ' ':
            self.board[square] = letter
            if self.check_win(letter):
                self.current_winner = letter
            return True
        return False

    def check_win(self, letter):
        # Check if the last move resulted in a win
        for combination in self.wining_combinations:
            if all(self.board[i] == letter for i in combination):
                return True
        return False

    def check_full_board(self):
        # Check if the board is full (no empty spaces)
        return ' ' not in self.board


    def replay(self):
        console = Console()
        choice = console.input("[green]Press [blue]Enter[/blue] to play again or type [blue]q[/blue] to quit: [/green]")
        if choice != 'q':
            return True
        else:
            return False

    def print_scoreboard(self):
        table = Table()
        table.title = "Scoreboard"
        table.add_column("Player", justify="center", style="cyan", no_wrap=True)
        table.add_column("Wins", justify="center", style="green")
        table.add_column("Draws", justify="center", style="yellow")
        table.add_column("Losses", justify="center", style="red")

        table.add_row(self.player1, str(self.player1_wins), str(self.draws), str(self.player2_wins))
        table.add_row(self.player2, str(self.player2_wins), str(self.draws), str(self.player1_wins))

        self.console.print(table)

    def next_play(self):
        # Change X and O for the next play
        self.board = [' ' for _ in range(9)]
        self.current_winner = None
        