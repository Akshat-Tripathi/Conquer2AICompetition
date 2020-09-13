class agent():

    def __init__(self, game, player):
        self.game = game
        self.player = player

    def step(self):
        raise NotImplementedError