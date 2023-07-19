import diamant
import players as playerclasses
import math
import csv


def game_loop(players: list) -> dict:
    game = diamant.Diamant(players=len(players))
    for round_index in range(1, 6):
        # print(f"\n=========\nRound {round_index}\n=========")
        round_players = list(players)  # All players start
        # make sure all players have no rubies
        for player in round_players:
            player.held_rubies = 0
        while True:
            # Select a new card, break if we have "died"
            round_over = game.select_card()  # Returns true if the round is over
            # print(f"\nCard is a {game.current_cavern}.")
            if round_over:
                # print("Ending round, we have been trapped!")
                # print(f"There were {len(round_players)} players remaining out of {len(players)}.")
                break
            else:
                game_state = game.get_game_state()

            # Give players rubies if required
            rubies_to_give = math.floor(game.current_tunnel[-1].rubies / len(round_players))
            # print(f"Each player gets {rubies_to_give} rubies.")
            for player in round_players:
                player.give_rubies(rubies_to_give)
            game.current_tunnel[-1].reduce_rubies(len(round_players) * rubies_to_give)  # Reduce ruby amount

            # Notify all players of state, are they continuing?
            players_going = []
            for index, player in enumerate(round_players):
                if not player.are_you_staying(game_state):
                    # We need to divide the rubies by all players leaving, so we need to know about them
                    players_going.append(player)
                    # Remove them from future parts of this round
                    round_players.pop(index)
                    # print(f"{player.name} is going home. {len(round_players)} players remaining.")

            # For players leaving, give them gems, remove gems from caverns that need to
            if len(players_going) > 0:
                for cavern in game.current_tunnel:
                    if cavern.rubies > 0:
                        rubies_to_give = math.floor(cavern.rubies / len(players_going))
                        for player in players_going:
                            player.give_rubies(rubies_to_give)
                        # Reduce ruby amount
                        cavern.reduce_rubies(len(players_going) * rubies_to_give)
                # Players that have just exited, should now bank
                for player in players_going:
                    # print(f"{player.name} banks {player.held_rubies} rubies")
                    player.bank()

            # End round if no one is left playing
            if len(round_players) <= 0:
                # print("There are no more players remaining, ending round.")
                game.start_new_round()
                break

    # print("\n")
    # print("Final scores")
    results = {}
    for player in players:
        # print(f"{player.name} had {player.banked_rubies}")
        results[player.name] = player.banked_rubies
        player.banked_rubies = 0  # Make sure the player doesnt have any rubies held over between games
    return results


if __name__ == "__main__":
    players = [
        playerclasses.RandomPlayer(),
        playerclasses.EstimatedRubiesPlayer(6),
        playerclasses.EstimatedRubiesPlayer(10),
        playerclasses.EstimatedRubiesPlayer(20),
    ]

    number_of_runs = 100

    player_scores = {}
    for player in players:
        player_scores[player.name] = {"mean": float(0.0), "median": float(0.0), "range": 0, "scores": []}

    for game_run in range(number_of_runs):
        results = game_loop(players=players)
        for player_name in player_scores:
            player_scores[player_name]["scores"].append(results[player_name])
        # print(player_scores)
    for player_name in player_scores:  # Average results out
        player_scores[player_name]["mean"] = sum(player_scores[player_name]["scores"]) / number_of_runs
    print(player_scores)
