def rockpaperscissors(opponent, outcome):
    '''
    Returns the score of this match.

    Win = 6 pts.
    Draw = 3 pts.

    Rock (A/0) = 1 pt.
    Paper (B/1) = 2 pts.
    Scissors (C/2) = 3 pts.
    '''
    replies = [[2, 0, 1], [0, 1, 2], [1, 2, 0]]
    scores = [[4, 1, 7], [8, 5, 2], [3, 9, 6]]

    opponent_number = ord(opponent) - ord('A')
    reply = replies[ord(outcome) - ord('X')][opponent_number]
    return scores[reply][opponent_number]


with open("day2/day2in.txt") as strats:
    score = 0
    for match in strats:
        score += rockpaperscissors(match[0], match[2])
    print(score)