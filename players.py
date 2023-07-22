import random
import math


class BasePlayer:
    """Base class"""

    def __init__(self, name: str):
        self.name: str = name
        self.held_rubies: int = 0
        self.banked_rubies: int = 0
        self.returning: bool = False
        self.passive: bool = False

    def are_you_staying(self, game_state):
        # base class
        return False

    def give_rubies(self, rubies):
        self.held_rubies += rubies

    def gone_home(self):
        self.banked_rubies += self.held_rubies
        self.held_rubies = 0
        self.returning = False
        self.passive = True

    def new_round(self):
        self.held_rubies = 0
        self.returning = False
        self.passive = False

    def new_game(self):
        self.new_round()
        self.banked_rubies = 0

    def _estimated_rubies_remaining(
        self, game_tunnel: list, guessed_num_players: int = 2
    ) -> int:
        rubies_remaining = 0
        for cavern in game_tunnel:
            rubies_remaining += math.floor(cavern.rubies / guessed_num_players)
        return rubies_remaining


class RandomPlayer(BasePlayer):
    """Returns randomly 1 out of every 10 times."""

    def __init__(self, name: str):
        super().__init__(f"RandomPlayer{name}")

    def are_you_staying(self, game_state):
        return False if random.randint(0, 9) == 0 else True


class EstimatedRubiesPlayer(BasePlayer):
    """Returns if it thinks it can get the target amount of rubies."""

    def __init__(self, target_rubies: int):
        super().__init__(f"EstimatedRubies{str(target_rubies)}")
        self.target_rubies = target_rubies

    def are_you_staying(self, game_state):
        if self.held_rubies >= self.target_rubies:  # We just have the amount in hand
            return False

        # When adding half (floored on each cavern) the remaining rubies to the amount in hand
        if (
            self._estimated_rubies_remaining(game_state["tunnel"], 2)
            >= self.target_rubies
        ):
            return False
        return True


class CarefulPlayer(BasePlayer):
    """Returns if it thinks it is likely to lose"""

    def __init__(self, danger_threshold):
        super().__init__(f"CarefulPlayer{danger_threshold}")
        self.danger_threshold = danger_threshold

    def are_you_staying(self, game_state):
        # if we have no rubies and cannot get any going home, stay
        if (
            self.held_rubies == 0
            and self._estimated_rubies_remaining(
                game_state["tunnel"], max([game_state["players_playing"] - 1, 1])
            )
            <= 0
        ):
            return True

        # if there is a "high" likelyhood of getting trapped, go home
        # we define high as > x% chance that the next card pulled causes us to get trapped
        # to do this:
        # get how many cards are left
        # get traps encountered and discarded
        # for type of trap, add chance that it could appear next (and kill) to total
        # if total chance is higher than x, return false, else return true
        chance_of_death = 0
        caverns_left_to_draw = game_state["total_caverns"] - len(game_state["tunnel"])
        for trap_type in game_state["trap_types"]:
            # if there is a chance that this type of trap could kill, this is 'cus there are 3 of each trap, and two are needed to kill, so if 2 are discarded it cannot kill again
            if (
                game_state["traps_discarded"].count(trap_type) < 2
                and trap_type in game_state["traps_encountered"]
            ):
                chance_of_death += (
                    3 - game_state["traps_discarded"].count(trap_type)
                ) / caverns_left_to_draw
