class Game:
    def __init__(self, player1, player2):
        self.board = [' ' for _ in range(9)]  # Represents the 3x3 board
        self.current_winner = None  # Keep track of the winner!
        self.player1 = player1
        self.player2 = player2
        self.current_player = player1  # Player 1 starts
        self.wining_combinations = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Rows
            [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Columns
            [0, 4, 8], [2, 4, 6]   # Diagonals
        ]

    def print_board(self):
        print()
        print(' ' + self.board[0] + ' | ' + self.board[1] + ' | ' + self.board[2])
        print('---+---+---')
        print(' ' + self.board[3] + ' | ' + self.board[4] + ' | ' + self.board[5])
        print('---+---+---')
        print(' ' + self.board[6] + ' | ' + self.board[7] + ' | ' + self.board[8])
        print()


    def print_board_nums(self):
        # Tells us what number corresponds to what box  from 1 to 9; i.e. a guide for players
        number_board = [[str(i+1) for i in range(j * 3, (j + 1) * 3)] for j in range(3)]
        print()
        for row in number_board:
            print(' ' + ' | '.join(row))
            if row != number_board[-1]:
                print('---+---+---')
        print()

    def available_moves(self):
        # Returns a list of available moves (indices of empty spots)
        return [i for i, spot in enumerate(self.board) if spot == ' ']

    def make_move(self, square, letter):
        # If valid move, then make the move (assign square to letter)
        if self.board[square] == ' ':
            self.board[square] = letter
            if self.winner(square, letter):
                self.current_winner = letter
            return True
        return False

    def winner(self, square, letter):
        # Check if the last move resulted in a win
        for combination in self.wining_combinations:
            if all(self.board[i] == letter for i in combination):
                return True
        return False
