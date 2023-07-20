import random
import math


class BasePlayer:
    """Base class"""
    def __init__(self, name: str):
        self.name:str = name
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


class RandomPlayer(BasePlayer):
    """Returns randomly 1 out of every 10 times."""

    def __init__(self):
        super().__init__("RandomPlayer")

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
        rubies_remaining = 0
        for cavern in game_state["tunnel"]:
            rubies_remaining += cavern.rubies
        # When adding half the remaining rubies to the amount in hand
        if (self.held_rubies + (math.floor(rubies_remaining / 2))) >= self.target_rubies:
            return False
        return True
