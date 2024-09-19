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


def has_two_pair(counts: list[int], sorted_counts: list[int]) -> bool:
    """
    Checks if the 5 dice match exactly the Two Pair pattern
    """
    return counts[sorted_counts[0]] == 2 and counts[sorted_counts[1]] == 2


def rerun_for_two_pair(counts: list[int], sorted_counts: list[int]) -> list[int]:
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


def has_trips(counts: list[int], sorted_counts: list[int]) -> bool:
    """
    Checks if the 5 dice match exactly the Trips pattern
    """
    return counts[sorted_counts[0]] == 3 and counts[sorted_counts[1]] == 1


def rerun_for_trips(counts: list[int], sorted_counts: list[int]) -> list[int]:
    if counts[sorted_counts[0]] >= 3:
        return [sorted_counts[0], sorted_counts[0], sorted_counts[0]] + roll_dice(2)

    if counts[sorted_counts[0]] == 2:
        return [sorted_counts[0], sorted_counts[0]] + roll_dice(3)

    return [sorted_counts[0], sorted_counts[1]] + roll_dice(3)


def has_little_straight(counts: list[int], _: list[int]) -> bool:
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


def rerun_for_straight(counts: list[int], sorted_counts: list[int]) -> list[int]:
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


def has_great_straight(counts: list[int], _: list[int]) -> bool:
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


def has_quads(counts: list[int], sorted_counts: list[int]) -> bool:
    """
    Checks if the 5 dice match exactly the Quads pattern
    """
    return counts[sorted_counts[0]] == 4


def rerun_for_quads(counts: list[int], sorted_counts: list[int]) -> list[int]:
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


# Ordered by rarity and because a "pair"
# is contained in "little straight" so it
# have to be check before
patterns = {
    "mega": has_mega,
    "great straight": has_great_straight,
    "little straight": has_little_straight,
    "quads": has_quads,
    "full": has_full,
    "trips": has_trips,
    "two pair": has_two_pair,
    "pair": has_pair,
}

patterns_rerun = {
    "mega": rerun_for_mega,
    "great straight": rerun_for_straight,
    "little straight": rerun_for_straight,
    "quads": rerun_for_quads,
    "full": rerun_for_full,
    "trips": rerun_for_trips,
    "two pair": rerun_for_two_pair,
    "pair": rerun_for_pair,
}
