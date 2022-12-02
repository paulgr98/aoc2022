with open('input.txt', 'r') as f:
    data = f.read().splitlines()

data = [tuple(item.split()) for item in data]


def determine_result(choices: tuple):
    """
        Determine result of a round.

        A, X - rock
        B, Y - paper
        C, Z - scissors

        win - 6 pts.
        draw  - 3 pts.
        lose - 0 pts.
    """
    opponent_choice = choices[0]
    my_choice = choices[1]

    victories = {
        'X': 'C',  # rock beats scissors
        'Y': 'A',  # paper beats rock
        'Z': 'B'  # scissors beats paper
    }
    draws = {
        'X': 'A',
        'Y': 'B',
        'Z': 'C'
    }
    defeat = victories[my_choice]

    if opponent_choice == draws[my_choice]:
        return 3  # win
    elif opponent_choice == defeat:
        return 6  # draw
    else:
        return 0  # lose


def calc_score(choices: tuple):
    """
        Calculate score for a tuple of choices.

        A, X - rock
        B, Y - paper
        C, Z - scissors

        rock - 1 pts.
        paper - 2 pts.
        scissors - 3 pts.
    """
    my_choice = choices[1]
    pts = {
        'X': 1,
        'Y': 2,
        'Z': 3
    }
    return determine_result(choices) + pts[my_choice]


def determine_choice(choices: tuple):
    """
        A, X - rock
        B, Y - paper
        C, Z - scissors

        X - lose
        Y - draw
        Z - lose

    """
    opponent_choice = choices[0]
    result = choices[1]

    if result == 'Y':  # draw
        my_choices = {
            'A': 'X',
            'B': 'Y',
            'C': 'Z'
        }
        return my_choices[opponent_choice]
    elif result == 'X':  # lose
        my_choices = {
            'A': 'Z',
            'B': 'X',
            'C': 'Y'
        }
        return my_choices[opponent_choice]
    else:  # win
        my_choices = {
            'A': 'Y',
            'B': 'Z',
            'C': 'X'
        }
        return my_choices[opponent_choice]


def calc_score_strategy_2(choices: tuple):
    opponent_choice = choices[0]
    my_choice = determine_choice(choices)
    return calc_score((opponent_choice, my_choice))


# part one
total_pts = sum([calc_score(ch) for ch in data])
print(total_pts)

# part two
total_pts = sum([calc_score_strategy_2(ch) for ch in data])
print(total_pts)
