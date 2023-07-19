import diamant
import players as playerclasses
import math
import csv


def game_loop(players: list) -> list:
    game = diamant.Diamant(players=len(players))
    for round_index in range(1, 6):
        # print(f"\n=========\nRound {round_index}\n=========")
        # Reset all player status
        for player in players:
            player.new_round()
        while True: # Select cards until something breaks
            # Select a new card, break if we have "died"
            round_over = game.select_card()  # Returns true if the round is over
            # print(f"\nCard is a {game.current_cavern}.")
            if round_over:
                # print("Ending round, we have been trapped!")
                break
            else:
                game_state = game.get_game_state()

            # Get how many players are still playing
            players_playing = len(players)
            for player in players:
                if player.passive:
                    players_playing -= 1

            # Give players rubies if required
            rubies_to_give = math.floor(game.current_tunnel[-1].rubies / players_playing)
            # print(f"Each player gets {rubies_to_give} rubies.")
            for player in players:
                if not player.passive:
                    player.give_rubies(rubies_to_give)
            game.current_tunnel[-1].reduce_rubies(players_playing * rubies_to_give)  # Reduce ruby amount

            # Notify all players of state, are they continuing?
            players_returning = 0
            for player in players:
                if not player.are_you_staying(game_state):
                    player.returning = True # TODO, could the player just set this themselves?
                    players_returning += 1

            # For players leaving, give them gems, remove gems from caverns that need to
            if players_returning > 0:
                for cavern in game.current_tunnel:
                    if cavern.rubies > 0:
                        rubies_to_give = math.floor(cavern.rubies / players_returning)
                        for player in players:
                            if player.returning:
                                player.give_rubies(rubies_to_give) # Give rubies to player
                                cavern.reduce_rubies(rubies_to_give) # Reduce ruby amount in cavern
                                player.bank() # Tell player to bank rubies

            # Tell players returning that they are now passive
            players_playing = len(players)
            for player in players:
                if player.returning:
                    player.passive = True
                    player.returning = False
                    players_playing -= 1
                elif player.passive:
                    players_playing -= 1
                else: # They are still playing
                    pass

            # End round if no one is left playing
            if players_playing <= 0:
                # print("There are no more players remaining, ending round.")
                game.start_new_round()
                break

    # print("\n")
    # print("Final scores")
    # for player in players:
    #     # print(f"{player.name} had {player.banked_rubies}")
    #     results[player.name] = player.banked_rubies
    #     player.banked_rubies = 0  # Make sure the player doesnt have any rubies held over between games
    return players


if __name__ == "__main__":
    players = [
        playerclasses.RandomPlayer(),
        playerclasses.EstimatedRubiesPlayer(6),
        playerclasses.EstimatedRubiesPlayer(10),
        playerclasses.EstimatedRubiesPlayer(20),
    ]

    number_of_runs = 1000

    player_scores = {}
    for player in players:
        player_scores[player.name] = {"mean": 0, "median": 0, "range": 0, "scores": []}

    for game_run in range(number_of_runs):
        players = game_loop(players=players)
        for player in players:
            player_scores[player.name]["scores"].append(player.banked_rubies)
            player.new_game()

    for player in players:  # Average results out
        player_scores[player.name]["mean"] = sum(player_scores[player.name]["scores"]) / number_of_runs
        print(f"{player.name} has a mean of {player_scores[player.name]['mean']}")
