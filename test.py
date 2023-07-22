game_state = {
    "total_caverns": 30,
    "trap_types": ["test1", "test2", "test3", "test4", "test5"],
    "traps_discarded": [],
    "traps_encountered": ["test1", "test2", "test3", "test4"],
}

chance_of_death = 0
caverns_left_to_draw = game_state["total_caverns"] - 18  # len(game_state["tunnel"])
for trap_type in game_state["trap_types"]:
    # if there is a chance that this type of trap could kill, this is 'cus there are 3 of each trap, and two are needed to kill, so if 2 are discarded it cannot kill again
    if (
        game_state["traps_discarded"].count(trap_type) < 2
        and trap_type in game_state["traps_encountered"]
    ):
        chance_of_death += (
            3 - game_state["traps_discarded"].count(trap_type)
        ) / caverns_left_to_draw

print(f"There are {caverns_left_to_draw} caverns left to be played")
print(f"{len(game_state['traps_encountered'])} traps have been encountered")
print(f"{len(game_state['traps_discarded'])} traps have been discarded")
print(f"There is a {chance_of_death}/1 chance of death")
