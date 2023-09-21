def rockpaperscissors(opponent, reply):
    '''
    Returns the score of this match.

    Win = 6 pts.
    Draw = 3 pts.

    Rock (A/X) = 1 pt.
    Paper (B/Y) = 2 pts.
    Scissors (C/Z) = 3 pts.
    '''
    outcomes = [[4, 1, 7], [8, 5, 2], [3, 9, 6]]
    return outcomes[ord(reply) - ord('X')][ord(opponent) - ord('A')]


with open("day2/day2in.txt") as strats:
    score = 0
    for match in strats:
        score += rockpaperscissors(match[0], match[2])
    print(score)