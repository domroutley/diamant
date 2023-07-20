import diamant
import players as playerclasses


def game_loop(players: list) -> list:
    game = diamant.Diamant(players)
    for round_index in range(1, 6):
        # print(f"\n=========\nRound {round_index}\n=========")
        while True: # Select cards until something breaks
            # Select a new card, break if we have "died"
            try_to_extend = game.extend_tunnel()  # Returns false if the round is over, the tunnel could not be extended
            if not try_to_extend: # we have been trapped
                game.start_new_round()
                break

            # End round if no one is left playing
            if game.how_many_players_playing() <= 0:
                game.start_new_round()
                break
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
