import random

from knapsack import (fractional_greedy, greedy_01, knapsack_dp,
                      knapsack_dp_1d, brute_force)


def test_greedy_trap():
    weights = [10, 20, 30]
    profits = [60, 100, 120]
    capacity = 50
    g, _, _ = greedy_01(weights, profits, capacity)
    dp, _, _, _ = knapsack_dp(weights, profits, capacity)
    print(f"Greedy 0/1 = {g}, DP = {dp}")
    assert g == 160
    assert dp == 220


def test_dp_matches_brute_force():
    rng = random.Random(1)
    for _ in range(200):
        n = rng.randint(1, 10)
        weights = [rng.randint(1, 15) for _ in range(n)]
        profits = [rng.randint(10, 200) for _ in range(n)]
        capacity = rng.randint(5, 40)
        dp, _, _, _ = knapsack_dp(weights, profits, capacity)
        dp1, _ = knapsack_dp_1d(weights, profits, capacity)
        bf, _ = brute_force(weights, profits, capacity)
        assert dp == bf, f"DP mismatch: {weights} {profits} {capacity}"
        assert dp1 == bf, f"1D mismatch: {weights} {profits} {capacity}"


def test_fractional_is_upper_bound():
    rng = random.Random(2)
    for _ in range(200):
        n = rng.randint(1, 12)
        weights = [rng.randint(1, 15) for _ in range(n)]
        profits = [rng.randint(10, 200) for _ in range(n)]
        capacity = rng.randint(5, 50)
        frac, _, _ = fractional_greedy(weights, profits, capacity)
        dp, _, _, _ = knapsack_dp(weights, profits, capacity)
        assert frac >= dp - 1e-9


if __name__ == "__main__":
    test_greedy_trap()
    test_dp_matches_brute_force()
    test_fractional_is_upper_bound()
    print("All tests passed")
