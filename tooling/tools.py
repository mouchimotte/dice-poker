import random


def roll_dice(n: int) -> list[int]:
    """
    Returns a list of n dice rolls
    """
    return [random.randint(1, 6) for _ in range(n)]


def dice_digest(dice: list[int]) -> tuple[list[int], list[int]]:
    """
    Returns:
    - a list of number of times a number is present in the set of dice
    - and an ordered list of number that are the most present

    Those 2 lists will help to:
    - identify patterns
    - identify which dice are best to re-roll

    We can resume all possible combinaisons of 5 dice by:
    - a-a-a-a-a 5 mega
    - a-a-a-a-b 4-1 carre
    - a-a-a-b-b 3-2 full
    - a-a-a-b-c 3-1-1 brelan
    - a-a-b-b-c 2-2-1 double paire
    - a-a-b-c-d 2-1-1-1 paire + petite suite
    - a-b-c-d-e 1-1-1-1-1 grande suite + petite suite + rien
    """
    counts = [0] * 7
    for die in dice:
        counts[die] += 1
    sorted_counts = sorted(range(7), key=lambda k: counts[k], reverse=True)
    sorted_counts.remove(0)
    return counts, sorted_counts


def get_max_subset(counts: list[int]) -> list[int]:
    subset_current = []
    subset_max = []
    for i, count in enumerate(counts):
        if count == 0:
            subset_max = subset_current if len(subset_current) > len(subset_max) else subset_max
            subset_current = []
        else:
            subset_current.append(i)
    return subset_max
