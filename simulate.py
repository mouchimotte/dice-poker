import random
from itertools import groupby
from typing import Callable


def roll_dice(n: int) -> list[int]:
    return [random.randint(1, 6) for _ in range(n)]


# a-a-a-a-a 5 mega
# a-a-a-a-b 4-1 carre
# a-a-a-b-b 3-2 full
# a-a-a-b-c 3-1-1 brelan
# a-a-b-b-c 2-2-1 double paire
# a-a-b-c-d 2-1-1-1 paire + petite suite
# a-b-c-d-e 1-1-1-1-1 grande suite + petite suite + rien
def dice_digest(dice: list[int]) -> tuple[list[int], list[int]]:
    counts = [0] * 7
    for die in dice:
        counts[die] += 1
    sorted_counts = sorted(range(7), key=lambda k: counts[k], reverse=True)
    sorted_counts.remove(0)
    return counts, sorted_counts


def has_pair(counts: list[int], sorted_counts: list[int]) -> bool:
    return counts[sorted_counts[0]] == 2 and counts[sorted_counts[1]] == 1


def rerun_for_pair(counts: list[int], sorted_counts: list[int]) -> list[int]:
    if counts[sorted_counts[0]] >= 2:
        return [sorted_counts[0], sorted_counts[0]] + roll_dice(3)
    return [sorted_counts[0], sorted_counts[1]] + roll_dice(3)


def has_double_pair(counts: list[int], sorted_counts: list[int]) -> bool:
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
    return counts[sorted_counts[0]] == 3 and counts[sorted_counts[1]] == 1


def rerun_for_brelan(counts: list[int], sorted_counts: list[int]) -> list[int]:
    if counts[sorted_counts[0]] >= 3:
        return [sorted_counts[0], sorted_counts[0], sorted_counts[0]] + roll_dice(2)

    if counts[sorted_counts[0]] == 2:
        return [sorted_counts[0], sorted_counts[0]] + roll_dice(3)

    return [sorted_counts[0], sorted_counts[1]] + roll_dice(3)


# 1-2-3-4
# 2-3-4-5
# 3-4-5-6
def has_little_suite(counts: list[int], _: list[int]) -> bool:
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


def get_max_subset(counts):
    subset_current = []
    subset_max = []
    for i, count in enumerate(counts):
        if count == 0:
            subset_max = subset_current if len(subset_current) > len(subset_max) else subset_max
            subset_current = []
        else:
            subset_current.append(i)
    return subset_max


def has_great_suite(counts: list[int], _: list[int]) -> bool:
    # 1-2-3-4-5
    # 2-3-4-5-6
    return len(get_max_subset(counts)) == 5


def has_full(counts: list[int], sorted_counts: list[int]) -> bool:
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
    return counts[sorted_counts[0]] == 5


def rerun_for_mega(counts: list[int], sorted_counts: list[int]) -> list[int]:
    if counts[sorted_counts[0]] == 4:
        return [sorted_counts[0], sorted_counts[0], sorted_counts[0], sorted_counts[0]] + roll_dice(1)

    if counts[sorted_counts[0]] >= 3:
        return [sorted_counts[0], sorted_counts[0], sorted_counts[0]] + roll_dice(2)

    if counts[sorted_counts[0]] == 2:
        return [sorted_counts[0], sorted_counts[0]] + roll_dice(3)

    return [sorted_counts[0], sorted_counts[1]] + roll_dice(3)


def simulate(trials: int, has_pattern: Callable) -> float:
    successes = 0
    for _ in range(trials):
        dice = roll_dice(5)
        counts, sorted_counts = dice_digest(dice)
        if has_pattern(counts, sorted_counts):
            successes += 1
        else:
            for i in range(3):
                dice = roll_dice(i+1) + dice[:5-i-1]
                if has_pattern(counts, sorted_counts):
                    successes += 1
                    break
    return successes / trials


def simulate_hard_try(trials: int, looking_for_pattern) -> dict[str, float]:
    successes = {_n: 0 for _n in patterns.keys()}
    successes.update({"": 0})
    for _ in range(trials):
        successes[simulate_hard_try_trial(looking_for_pattern)] += 1
    return successes


def simulate_hard_try_trial(looking_for_pattern: str) -> str:
    dice = roll_dice(5)
    counts, sorted_counts = dice_digest(dice)
    current_pattern = ""
    for pattern, has_pattern in patterns.items():
        if has_pattern(counts, sorted_counts):
            current_pattern = pattern
            break
    if current_pattern == looking_for_pattern:
        return current_pattern

    # Rerun
    dice = patterns_rerun[looking_for_pattern](counts, sorted_counts)
    counts, sorted_counts = dice_digest(dice)
    current_pattern = ""
    for pattern, has_pattern in patterns.items():
        if has_pattern(counts, sorted_counts):
            current_pattern = pattern
            break
    return current_pattern


def simulate_smart(trials: int) -> tuple[dict[str, float], dict[str, float]]:
    successes_first = {_n: 0 for _n in patterns.keys()}
    successes_first.update({"": 0})
    successes_rerun = {_n: 0 for _n in patterns.keys()}
    successes_rerun.update({"": 0})
    for _ in range(trials):
        first_pattern, current_pattern = simulate_smart_try()
        successes_first[first_pattern] += 1
        if current_pattern is not None:
            successes_rerun[current_pattern] += 1
    return successes_first, successes_rerun


def simulate_smart_try() -> tuple[str, str | None]:
    dice = roll_dice(5)
    # Check for pattern
    counts, sorted_counts = dice_digest(dice)
    first_pattern = ""
    for pattern, has_pattern in patterns.items():
        if has_pattern(counts, sorted_counts):
            first_pattern = pattern
            break

    # Stop at first roll for GOOD patterns
    if first_pattern in ["mega", "full", "grande suite"]:
        return first_pattern, None

    # Rerun to get more points for patterns:
    # - carre
    # - petite suite
    # - brelan
    # - double paire
    # - paire
    # - no pattern
    if first_pattern == "carre":
        # will rerun only the different die
        dice = [sorted_counts[0], sorted_counts[0], sorted_counts[0], sorted_counts[0]] + roll_dice(1)
    elif first_pattern == "petite suite":
        # will rerun only the extra die
        subset_max = get_max_subset(counts)
        dice = subset_max + roll_dice(1)
    elif first_pattern == "brelan":
        # will rerun only 2 different dice
        dice = [sorted_counts[0], sorted_counts[0], sorted_counts[0]] + roll_dice(2)
    elif first_pattern == "double paire":
        # will rerun only the different die
        dice = [sorted_counts[0], sorted_counts[0], sorted_counts[1], sorted_counts[1]] + roll_dice(1)
    elif first_pattern == "paire":
        # will rerun the 3 different dice, not the pair
        dice = [sorted_counts[0], sorted_counts[0]] + roll_dice(3)
    # no pattern
    else:
        # will keep first 2 dice and rerun the rest
        dice = [sorted_counts[0], sorted_counts[1]] + roll_dice(3)

    # Check for new pattern
    counts, sorted_counts = dice_digest(dice)
    current_pattern = ""
    for pattern, has_pattern in patterns.items():
        if has_pattern(counts, sorted_counts):
            current_pattern = pattern
            break

    return first_pattern, current_pattern


# Ordered by rarity
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

tries = 1000000
print(f"Tries {tries} times each pattern, with rerun 3 times a die.")
for name, has_pattern in patterns.items():
    probability = simulate(tries, has_pattern)
    print(f"Estimated probability of pattern {name}: {probability:.4f}")

print(f"\n")

print(f"Tries {tries} times each pattern, with smart rerun with intent to reach the pattern only.")
for name, _ in patterns.items():
    print(f"{tries} trials will be run for each pattern.")
    probability = simulate_hard_try(tries, name)

    print(f"Estimated probability when looking for {name}:")
    for k, v in probability.items():
        print(f"    - {k}: {v/tries*100:.4f}%")

print(f"\n")

print(f"Tries {tries} times of roll, with smart rerun with intent to reach the best pattern.")
probability_first, probability_rerun = simulate_smart(tries)
print(f"Without rerun any dice:")
for k, v in probability_first.items():
    print(f"    - {k}: {v / tries * 100:.4f}%")
print(f"With rerun from 1 to 3 dice:")
for k, v in probability_rerun.items():
    print(f"    - {k}: {v / tries * 100:.4f}%")
