import random

def player(prev_play, opponent_history=[[], [], [-1]], play_order=[{
              "RR": 0,
              "RP": 0,
              "RS": 0,
              "PR": 0,
              "PP": 0,
              "PS": 0,
              "SR": 0,
              "SP": 0,
              "SS": 0,
          }]):
    # maps for counters
    counter = {"R": "P", "P": "S", "S": "R", "": "P"}
    anticounter = {"R": "S", "P": "R", "S": "P", "": "S"}
    quincy_pattern = ["R", "R", "P", "P", "S"]

    # record opponent’s play
    if prev_play != "":
        opponent_history[1].append(prev_play)
    len_history = len(opponent_history[1])
    len_my_history = len(opponent_history[0])

    # first move = play "P"
    if len_history == 0:
        opponent_history[0].append("P")
        return "P"

    # get my last play
    my_prev_play = opponent_history[0][-1]

    # --- Strategy Detection ---
    next_play = None
    
    # print("player ", opponent_history[2][0])
    if len_my_history >= 5:
        abbey_trigger = "".join(opponent_history[0][-5:-3])
        last_two = "".join(opponent_history[0][-2:])
        # print("player ", opponent_history[0][-10:], " ", opponent_history[1][-5:], " ", last_two)
        if opponent_history[2][0] > 0:
            # print("player ", my_prev_play, " ", prev_play)
            if my_prev_play != counter[prev_play]:
                opponent_history[2][0] *= -1
                play_order=[{
                    "RR": 0,
                    "RP": 0,
                    "RS": 0,
                    "PR": 0,
                    "PP": 0,
                    "PS": 0,
                    "SR": 0,
                    "SP": 0,
                    "SS": 0,
                }]
            else:
                play_order[0][last_two] += 1
        elif abbey_trigger == "PP":
            if len_history >= 5:
                arr = opponent_history[1][-5:]
                is_quincy = False
                for i in range(5):
                    rotated = quincy_pattern[i:] + quincy_pattern[:i]
                    if arr == rotated:
                        is_quincy = True
                        break
                if is_quincy:
                    pass
                else:
                    play_order[0]["R" + opponent_history[0][-4]] += 1
                    play_order[0]["".join(opponent_history[0][-4:-2])] += 1
                    play_order[0]["".join(opponent_history[0][-3:-1])] += 1
                    play_order[0][last_two] += 1
                    opponent_history[2][0] *= -1
            else:
                play_order[0]["R" + opponent_history[0][-4]] += 1
                play_order[0]["".join(opponent_history[0][-4:-2])] += 1
                play_order[0]["".join(opponent_history[0][-3:-1])] += 1
                play_order[0][last_two] += 1
                opponent_history[2][0] *= -1

    # 1. Abbey
    # print("player abbey checker ", opponent_history[2][0])
    if opponent_history[2][0] > 0:
        potential_plays = [
            my_prev_play + "R",
            my_prev_play + "P",
            my_prev_play + "S",
        ]

        sub_order = {k: play_order[0][k] for k in potential_plays if k in play_order[0]}
        # print("player ", play_order, " ", sub_order, " ", last_two)
        if sub_order:
            predicted = max(sub_order, key=sub_order.get)[-1:]
            next_play = anticounter[predicted]
            opponent_history[0].append(next_play)
            return next_play

    # 2. Quincy
    if len_history >= 5:
        expected = ""
        arr = opponent_history[1][-5:]
        cycle_ok = False
        for i in range(5):
            rotated = quincy_pattern[i:] + quincy_pattern[:i]
            if arr == rotated:
                expected = rotated[0]
                cycle_ok = True
                break
        if cycle_ok:
            predicted = expected
            next_play = counter[predicted]
            opponent_history[0].append(next_play)
            return next_play

    # 3. Kris
    if len_history > 4 and opponent_history[1][-1] == counter[opponent_history[0][-2]]:
        if opponent_history[1][-2] == counter[opponent_history[0][-3]]:
            next_play = anticounter[my_prev_play]
            opponent_history[0].append(next_play)
            return next_play

    # 4. Mrugesh
    if len_history > 11:
        last_ten = opponent_history[0][-11:-1]
        most_freq = max(set(last_ten), key=last_ten.count)
        predicted = counter[most_freq]
        if opponent_history[1][-1] == predicted:
            next_play = counter[predicted]
            opponent_history[0].append(next_play)
            return next_play

    # 5. Random Player or Human → fall back to random safe play
    if not next_play:
        next_play = "P"

    opponent_history[0].append(next_play)
    return next_play