import random
import math
import players as playerclasses


class Cavern:
    def __init__(self, rubies: int, relic: bool = False):
        self.rubies = rubies
        self.__original_rubies = rubies
        self.relic = relic
        self.in_tunnel = False
        self.is_trap = False

    def reset(self):
        self.rubies = self.__original_rubies
        self.in_tunnel = False

    def reduce_rubies(self, take: int):
        self.rubies -= take


class Trap(Cavern):
    def __init__(self, name: str):
        super().__init__(0) # Sets up standard values
        self.name = name
        self.is_trap = True


class Diamant:
    def __init__(self, players:list):
        # Start by shuffling the deck
        self.caverns = [
            Trap("snek"),
            Trap("snek"),
            Trap("snek"),
            Trap("chomper"),
            Trap("chomper"),
            Trap("chomper"),
            Trap("spleider"),
            Trap("spleider"),
            Trap("spleider"),
            Trap("squish"),
            Trap("squish"),
            Trap("squish"),
            Trap("lava"),
            Trap("lava"),
            Trap("lava"),
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
        self.traps_encountered = []
        self.traps_discarded = []
        self.players = players
        for player in self.players: # Initilise players
            player.new_game()
        self._trap_types = set([])
        for cavern in self.caverns:
            if cavern.is_trap:
                self._trap_types.add(cavern.name)

    def get_game_state(self):
        return {
            "tunnel": list(self.caverns[0:self.current_cavern_index]),
            "traps_encountered": self.traps_encountered,
            "traps_discarded": self.traps_discarded,
            "players_playing": self.how_many_players_playing(),
            "total_caverns": len(self.caverns),
            "trap_types": self._trap_types
        }

    def extend_tunnel(self) -> bool:
        # pick a cavern
        # this just sets the _next_ cavern as in the tunnel
        for index, cavern in enumerate(self.caverns):
            if not cavern.in_tunnel: # The next card
                cavern.in_tunnel = True
                self.current_cavern_index = index
                # is this a trap card, if so do we die?
                if cavern.is_trap:
                    if cavern.name in self.traps_encountered:
                        self.traps_discarded.append(cavern.name) # Can be used by players to calculate risk
                        self.caverns.pop(index) # Remove cavern from circulation
                        return False
                    else:
                        self.traps_encountered.append(cavern.name)
                else: # Give players rubies
                    rubies_to_give = math.floor(cavern.rubies / self.how_many_players_playing())
                    for player in self.players:
                        if not player.passive:
                            player.give_rubies(rubies_to_give)
                            cavern.reduce_rubies(rubies_to_give)
                    # Notify players of state, and share out rubies if they leave
                    self.__escort_players_home()
                break # Stop selecting cavern "cards"
        return True

    def start_new_round(self):
        # Reset values
        for cavern in self.caverns:
            cavern.reset()  # Reset cavern status
        self.traps_encountered = []  # Reset what traps would kill us
        self.current_cavern_index = 0 # reset current cavern index
        random.shuffle(self.caverns)  # Shuffle cavern "cards"
        # Reset all player status
        for player in self.players:
            player.new_round()

    def how_many_players_playing(self) -> int:
        players_playing = len(self.players)
        for player in self.players:
            if player.passive:
                players_playing -= 1
        return players_playing

    def __query_players(self):
        are_any_returning = False
        for player in self.players:
            if not player.are_you_staying(self.get_game_state()):
                player.returning = True
                are_any_returning = True
        return are_any_returning

    def __escort_players_home(self):
        if self.__query_players():
            for cavern in self.caverns:
                if cavern.in_tunnel and cavern.rubies > 0:
                    rubies_to_give = math.floor(cavern.rubies / self.how_many_players_playing())
                    for player in self.players:
                        if not player.passive and player.returning: # NOTE, not set as passive until after they have returned
                            player.give_rubies(rubies_to_give)
                            cavern.reduce_rubies(rubies_to_give)

            # tell all players trying to return that they have done so
            for player in self.players:
                if player.returning:
                    player.gone_home()
