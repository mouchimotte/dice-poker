# Dice Poker
Dice game based on poker patterns.

## Rules

Roll 5 dice of 6 faces then find a pattern.
To increase the chance to match a pattern you can re-roll 1 to 3 dice.

Each pattern have corresponding points, the goal is to reach 1000 points or above.

Each player have the same amount of tries. Then each time a turn of game is started,
it should be finished. Then, if a player reach 1000 points or above, the turn have to
be finished to allow each player have same amount of tries.

## Patterns

| Pattern         | % of appearance with smart re-roll | Points | Linear distribution of Points | Definition                        |
|-----------------|------------------------------------|--------|-------------------------------|-----------------------------------|
| Méga            | 0.93%                              | 1000   | 1000                          | 5 of a kind                       |
| Great straight  | 1.45%                              | 740    | 738                           | 5 dice of sequential rank         |
| Little straight | 8.10%                              | 130    | 133                           | 4 dice of sequential rank         |
| Quads           | 8.70%                              | 120    | 123                           | 4 of a kind                       |
| Full            | 13.73%                             | 80     | 78                            | 3 of a kind and 2 of another kind |
| Trips           | 20.57%                             | 50     | 52                            | 3 of a kind                       |
| Two pair        | 28.02%                             | 40     | 38                            | 2 of a kind and 2 of another kind |
| Pair            | 12.19%                             | 10     | 11                            | 2 of a kind                       |
| nothing         | 0.85%                              | 0      | 0                             | no matching pattern               |

### Méga

> 5 of a kind

Ex: `3-3-3-3-3`

Most difficult pattern to match, in every different strategies of re-roll or not.
Base of the game it return the maximum number of points, 1000.

### Great straight

> 5 dice of sequential rank

Ex: `1-2-3-4-5`

Only 2 combinaisons possible.

### Little straight

> 4 dice of sequential rank

Ex: `1-2-3-4-6`

### Quads

> 4 of a kind

Ex: `2-2-2-2-6`

### Full

> 3 of a kind and 2 of another kind

Ex: `1-1-1-4-4`

### Trips

> 3 of a kind

Ex: `3-3-3-4-6`

### Two pair

> 2 of a kind and 2 of another kind

Ex: `6-6-5-5-1`

### Pair

> 2 of a kind

Ex: `5-5-1-2-3`

### Nothing

> no matching pattern

Ex: `1-2-3-5-6`

## Statistics

3 strategies of tests.
Here all stats regarding all strategies.
Those stats have been generated using the following scrips:

- [Without Re-roll](simulate_without_reroll.py)
- [Smart Re-roll](simulate_smart_reroll.py)
- [Re-roll to match pattern](simulate_reroll_to_match.py)
- [Sequential re-roll to match pattern](simulate_sequential_reroll.py)

Each have been run 1000000 times.

| Pattern\Strategy | Without Re-roll | Smart Re-roll | Re-roll to match pattern | Sequential re-roll to match pattern |
|------------------|-----------------|---------------|--------------------------|-------------------------------------|
| Méga             | 0.08%           | 0.93%         | 1.25%                    | 0.08%                               |
| Great Straight   | 1.52%           | 1.45%         | 5.51%                    | 1.54%                               |
| Little Straight  | 7.68%           | 8.10%         | 21.21%                   | 7.67%                               |
| Quads            | 1.95%           | 8.70%         | 12.23%                   | 1.96%                               |
| Full             | 3.85%           | 13.73%        | 14.75%                   | 3.88%                               |
| Trips            | 15.44%          | 20.57%        | 39.10%                   | 15.45%                              |
| Two Pair         | 23.16%          | 28.02%        | 45.55%                   | 23.15%                              |
| Pair             | 40.17%          | 12.19%        | 55.82%                   | 46.30%                              |
| Nothing          | 6.16%           | 0.85%         | not tested               | not tested                          |

### Without re-roll

Basically do not re-roll any dice,
Stats are coming from a single roll of 5 dice.

### Sequential re-roll to match pattern

After the first roll of the 5 dice,
The strategy re-roll the first dice of the set and check for the watching pattern,
If it not match it repeat the re-roll part, at most 3 times.

### Re-roll to match pattern

After the first roll of the 5 dice,
The strategy re-roll the good dice to match the watching pattern.

For instance, if we are looking for a Méga,

1. If the first roll match the pattern we stop here,
2. If we get a Quads, we will re-roll only the last die,
3. If we get a Trips (or Full), we will re-roll 2 last dice,
4. If we get a Pair (or Two Pair), we will re-roll 3 other dice,
5. If we get Straight or Nothing, we will keep 2 first dice and re-roll 3 last dice,

All patterns have its own strategy to try to match exactly the pattern,
So, if we get "more" than a Pair, and we are looking for a Pair, we will
re-roll as necessary dice as possible to get a Pair.

The Strategy could lead to get another pattern than the one expected,
So the simulation return also the list of other pattern who have match
after the re-roll and their probability of appearance.

Then we can obtain the estimated probability when looking for Méga:

- Méga: 1.2486%
- Great Straight: 0.2511%
- Little Straight: 3.9166%
- Quads: 11.8591%
- Full: 9.3591%
- Trips: 31.1485%
- Two pair: 21.3051%
- Pair: 20.3902%
- Nothing: 0.5217%

### Smart Re-roll

Like in the real life, when you re-roll its to match the most valuable pattern.

For instance, if we get a Quads at the first roll of dice,
We will re-roll the last die to try to match the Méga.
