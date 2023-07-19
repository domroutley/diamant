import random


class Cavern:
    trap: str = ""
    __original_rubies = 0
    rubies: int = 0
    relic: bool = False

    def __init__(self, rubies: int = 0, relic: bool = False, trap: str = ""):
        self.trap = trap
        self.rubies = rubies
        self.__original_rubies = rubies
        self.relic = relic

    def reset_rubies(self):
        self.rubies = self.__original_rubies

    def reduce_rubies(self, take: int):
        self.rubies -= take

    def __str__(self) -> str:
        if self.trap == "":
            return f"{self.__original_rubies} rubies cavern"
        else:
            return f"{self.trap} cavern"


class Diamant:
    __original_players: int = -1
    players: int = -1
    caverns: list = []
    current_tunnel: list = []
    traps_encountered: list = []
    traps_discarded: list = []
    current_cavern: Cavern

    def __init__(self, players: int):
        self.players = players
        self.__original_players = players
        # Start by shuffling the deck
        self.caverns = [
            Cavern(trap="snek"),
            Cavern(trap="snek"),
            Cavern(trap="snek"),
            Cavern(trap="chomper"),
            Cavern(trap="chomper"),
            Cavern(trap="chomper"),
            Cavern(trap="spleider"),
            Cavern(trap="spleider"),
            Cavern(trap="spleider"),
            Cavern(trap="squish"),
            Cavern(trap="squish"),
            Cavern(trap="squish"),
            Cavern(trap="lava"),
            Cavern(trap="lava"),
            Cavern(trap="lava"),
            Cavern(1),
            Cavern(2),
            Cavern(3),
            Cavern(4),
            Cavern(5),
            Cavern(5),
            Cavern(7),
            Cavern(7),
            Cavern(9),
            Cavern(11),
            Cavern(11),
            Cavern(13),
            Cavern(14),
            Cavern(15),
            Cavern(17),
            # Relic caverns
            # Cavern(5, True),
            # Cavern(7, True),
            # Cavern(8, True),
            # Cavern(10, True),
            # Cavern(12, True),
        ]
        random.shuffle(self.caverns)

    def select_card(self):
        cavern = self.caverns.pop()
        self.current_cavern = cavern
        if cavern.trap != "":
            self.traps_encountered.append(cavern.trap)
            # If we would die
            if len(self.traps_encountered) != len(set(self.traps_encountered)):
                self.traps_discarded.append(cavern.trap)  # Store this "death" card
                self.start_new_round()  # Reset values
                return True  # State that we have died
        # We only add the cavern to the tunnel if it would not have killed us
        # This means it gets "purged" from the game
        self.current_tunnel.append(cavern)  # If we have not died, we want to add that cavern to the tunnel
        return False

    def start_new_round(self):
        # Reset values
        for cavern in self.current_tunnel:
            cavern.reset_rubies()  # Reset rubies
            self.caverns.append(cavern)  # Add back to deck
        self.current_tunnel = []  # Reset current tunnel
        self.traps_encountered = []  # Reset what traps would kill us
        random.shuffle(self.caverns)  # Shuffle
        self.players = int(self.__original_players)

    def get_game_state(self):
        return {
            "current_tunnel": self.current_tunnel,
            "players_remaining": self.players,
            "traps_encountered": self.traps_encountered,
            "traps_discarded": self.traps_discarded,
        }
