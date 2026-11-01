class User:
    def __init__(self, name, exp=0, wins=0, losses=0, draws=0):
        self.name = name
        self.wins = wins
        self.losses = losses
        self.draws = draws