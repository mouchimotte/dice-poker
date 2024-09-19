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
        else:
            for i in range(3):
                dice = roll_dice(i+1) + dice[:5-i-1]
                if has_pattern(counts, sorted_counts):
                    successes += 1
                    break
    return successes / trials

tries = 1000000
print(f"Tries {tries} times each pattern, with re-roll 3 times a die.")
for name, has_pattern in patterns.items():
    probability = simulate(tries, has_pattern)
    print(f"Estimated probability of pattern {name}: {probability:.4f}")
