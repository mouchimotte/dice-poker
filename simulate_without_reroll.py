from typing import Callable

from tooling.patterns import patterns
from tooling.tools import roll_dice, dice_digest


def simulate(trials: int, has_pattern: Callable) -> float:
    successes = 0
    for _ in range(trials):
        dice = roll_dice(5)
        counts, sorted_counts = dice_digest(dice)
        if has_pattern(counts, sorted_counts):
            successes += 1
    return successes / trials

tries = 1000000
print(f"Tries {tries} times each pattern, without re-roll.")
for name, has_pattern in patterns.items():
    probability = simulate(tries, has_pattern)
    print(f"Estimated probability of pattern {name}: {probability:.4f}")
