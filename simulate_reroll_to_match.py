from tooling.patterns import patterns, patterns_rerun
from tooling.tools import roll_dice, dice_digest


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


tries = 1000000
print(f"Tries {tries} times each pattern, with smart rerun with intent to reach the pattern only.")
for name, _ in patterns.items():
    print(f"{tries} trials will be run for each pattern.")
    probability = simulate_hard_try(tries, name)

    print(f"Estimated probability when looking for {name}:")
    for k, v in probability.items():
        print(f"    - {k}: {v/tries*100:.4f}%")
