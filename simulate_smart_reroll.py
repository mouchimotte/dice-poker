from tooling.patterns import patterns
from tooling.tools import get_max_subset, roll_dice, dice_digest


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

    # Rerun to get more point for following patterns:
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


tries = 1000000
print(f"Tries {tries} times of roll, with smart rerun with intent to reach the best pattern.")
probability_first, probability_rerun = simulate_smart(tries)
print(f"Without rerun any dice:")
for k, v in probability_first.items():
    print(f"    - {k}: {v / tries * 100:.4f}%")
print(f"With rerun from 1 to 3 dice:")
for k, v in probability_rerun.items():
    print(f"    - {k}: {v / tries * 100:.4f}%")
