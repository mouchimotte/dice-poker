from typing import Callable

from tooling.tools import roll_dice, get_max_subset


def has_pair(counts: list[int], sorted_counts: list[int]) -> bool:
    """
    Checks if the 5 dice match exactly the Pair pattern
    """
    return counts[sorted_counts[0]] == 2 and counts[sorted_counts[1]] == 1


def rerun_for_pair(counts: list[int], sorted_counts: list[int]) -> list[int]:
    if counts[sorted_counts[0]] >= 2:
        return [sorted_counts[0], sorted_counts[0]] + roll_dice(3)
    return [sorted_counts[0], sorted_counts[1]] + roll_dice(3)


def has_double_pair(counts: list[int], sorted_counts: list[int]) -> bool:
    """
    Checks if the 5 dice match exactly the Two Pair pattern
    """
    return counts[sorted_counts[0]] == 2 and counts[sorted_counts[1]] == 2


def rerun_for_double_pair(counts: list[int], sorted_counts: list[int]) -> list[int]:
    if counts[sorted_counts[0]] >= 4:
        return [sorted_counts[0], sorted_counts[0]] + roll_dice(3)

    if counts[sorted_counts[0]] == 3:
        if counts[sorted_counts[1]] == 2:
            return [
                sorted_counts[0],
                sorted_counts[0],
                sorted_counts[1],
                sorted_counts[1],
            ] + roll_dice(1)
        if counts[sorted_counts[1]] == 1:
            return [sorted_counts[0], sorted_counts[0]] + roll_dice(3)

    if counts[sorted_counts[0]] == 2:
        return [sorted_counts[0], sorted_counts[0]] + roll_dice(3)

    return [sorted_counts[0], sorted_counts[1]] + roll_dice(3)


def has_brelan(counts: list[int], sorted_counts: list[int]) -> bool:
    """
    Checks if the 5 dice match exactly the Trips pattern
    """
    return counts[sorted_counts[0]] == 3 and counts[sorted_counts[1]] == 1


def rerun_for_brelan(counts: list[int], sorted_counts: list[int]) -> list[int]:
    if counts[sorted_counts[0]] >= 3:
        return [sorted_counts[0], sorted_counts[0], sorted_counts[0]] + roll_dice(2)

    if counts[sorted_counts[0]] == 2:
        return [sorted_counts[0], sorted_counts[0]] + roll_dice(3)

    return [sorted_counts[0], sorted_counts[1]] + roll_dice(3)


def has_little_suite(counts: list[int], _: list[int]) -> bool:
    """
    Checks if the 5 dice match exactly the Little Straight pattern

    Can be:
    - 1-2-3-4-6
    - 2-3-4-5-2
    - 3-4-5-6-1

    This pattern should be tested before the Pair one,
    as the following example matches exactly the Little Straight
    and the Pair: 2-3-4-5-2
    """
    return len(get_max_subset(counts)) == 4


def rerun_for_suite(counts: list[int], sorted_counts: list[int]) -> list[int]:
    if counts[sorted_counts[0]] == 5:
        return [sorted_counts[0], sorted_counts[0]] + roll_dice(3)

    if counts[sorted_counts[0]] == 4:
        return [sorted_counts[0], sorted_counts[1]] + roll_dice(3)

    if counts[sorted_counts[0]] == 3 and counts[sorted_counts[1]] == 2:
        return [sorted_counts[0], sorted_counts[1]] + roll_dice(3)

    # Find the longest suite of number
    subset_max = get_max_subset(counts)

    # Rerun only necessary dice
    subset_max_len = len(subset_max)
    if subset_max_len > 1:
        return subset_max + roll_dice(5 - subset_max_len)

    return [sorted_counts[0], sorted_counts[1]] + roll_dice(3)


def has_great_suite(counts: list[int], _: list[int]) -> bool:
    """
    Checks if the 5 dice match exactly the Great Straight pattern

    Can be:
    - 1-2-3-4-5
    - 2-3-4-5-6
    """
    return len(get_max_subset(counts)) == 5


def has_full(counts: list[int], sorted_counts: list[int]) -> bool:
    """
    Checks if the 5 dice match exactly the Full pattern
    """
    return counts[sorted_counts[0]] == 3 and counts[sorted_counts[1]] == 2


def rerun_for_full(counts: list[int], sorted_counts: list[int]) -> list[int]:
    if counts[sorted_counts[0]] == 5:
        return [sorted_counts[0], sorted_counts[0], sorted_counts[0]] + roll_dice(2)

    if counts[sorted_counts[0]] >= 3:
        return [sorted_counts[0], sorted_counts[0], sorted_counts[0], sorted_counts[1]] + roll_dice(1)

    if counts[sorted_counts[0]] == 2:
        if counts[sorted_counts[1]] == 2:
            return [sorted_counts[0], sorted_counts[0], sorted_counts[1], sorted_counts[1]] + roll_dice(1)
        return [sorted_counts[0], sorted_counts[0], sorted_counts[1], sorted_counts[2]] + roll_dice(1)

    return [sorted_counts[0], sorted_counts[1]] + roll_dice(3)


def has_carre(counts: list[int], sorted_counts: list[int]) -> bool:
    """
    Checks if the 5 dice match exactly the Quads pattern
    """
    return counts[sorted_counts[0]] == 4


def rerun_for_carre(counts: list[int], sorted_counts: list[int]) -> list[int]:
    if counts[sorted_counts[0]] == 5:
        return [sorted_counts[0], sorted_counts[0], sorted_counts[0], sorted_counts[0]] + roll_dice(1)

    if counts[sorted_counts[0]] >= 3:
        return [sorted_counts[0], sorted_counts[0], sorted_counts[0]] + roll_dice(2)

    if counts[sorted_counts[0]] == 2:
        return [sorted_counts[0], sorted_counts[0]] + roll_dice(3)

    return [sorted_counts[0], sorted_counts[1]] + roll_dice(3)


def has_mega(counts: list[int], sorted_counts: list[int]) -> bool:
    """
    Checks if the 5 dice match exactly the Méga pattern
    """
    return counts[sorted_counts[0]] == 5


def rerun_for_mega(counts: list[int], sorted_counts: list[int]) -> list[int]:
    if counts[sorted_counts[0]] == 4:
        return [sorted_counts[0], sorted_counts[0], sorted_counts[0], sorted_counts[0]] + roll_dice(1)

    if counts[sorted_counts[0]] >= 3:
        return [sorted_counts[0], sorted_counts[0], sorted_counts[0]] + roll_dice(2)

    if counts[sorted_counts[0]] == 2:
        return [sorted_counts[0], sorted_counts[0]] + roll_dice(3)

    return [sorted_counts[0], sorted_counts[1]] + roll_dice(3)


# Ordered by rarity and
patterns = {
    "mega": has_mega,
    "grande suite": has_great_suite,
    "petite suite": has_little_suite,
    "carre": has_carre,
    "full": has_full,
    "brelan": has_brelan,
    "double paire": has_double_pair,
    "paire": has_pair,
}

patterns_rerun = {
    "mega": rerun_for_mega,
    "grande suite": rerun_for_suite,
    "petite suite": rerun_for_suite,
    "carre": rerun_for_carre,
    "full": rerun_for_full,
    "brelan": rerun_for_brelan,
    "double paire": rerun_for_double_pair,
    "paire": rerun_for_pair,
}
