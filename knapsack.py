import time
from itertools import combinations


# ---------- 1. Fractional Knapsack (Greedy) ----------
def fractional_greedy(weights, profits, capacity):
    """Items tod sakte hain. Return: (total_profit, fractions list, time)."""
    start = time.perf_counter()
    n = len(weights)
    order = sorted(range(n), key=lambda i: profits[i] / weights[i], reverse=True)

    fractions = [0.0] * n
    remaining = capacity
    total = 0.0

    for i in order:
        if remaining <= 0:
            break
        if weights[i] <= remaining:
            fractions[i] = 1.0
            remaining -= weights[i]
            total += profits[i]
        else:
            fractions[i] = remaining / weights[i]
            total += profits[i] * fractions[i]
            remaining = 0

    return total, fractions, time.perf_counter() - start


# ---------- 2. Greedy for 0/1 (sirf poore items) ----------
def greedy_01(weights, profits, capacity):
    """Ratio se sort, par sirf poore items. Optimal NAHI hota."""
    start = time.perf_counter()
    n = len(weights)
    order = sorted(range(n), key=lambda i: profits[i] / weights[i], reverse=True)

    chosen = [0] * n
    remaining = capacity
    total = 0

    for i in order:
        if weights[i] <= remaining:
            chosen[i] = 1
            remaining -= weights[i]
            total += profits[i]

    return total, chosen, time.perf_counter() - start


# ---------- 3. 0/1 Knapsack DP (2D table) ----------
def knapsack_dp(weights, profits, capacity):
    """Optimal. Return: (profit, chosen list, dp table, time)."""
    start = time.perf_counter()
    n = len(weights)
    dp = [[0] * (capacity + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        w, p = weights[i - 1], profits[i - 1]
        for c in range(capacity + 1):
            dp[i][c] = dp[i - 1][c]                      # item skip
            if w <= c:
                dp[i][c] = max(dp[i][c], dp[i - 1][c - w] + p)  # item lo

    # Backtrack: kaunse items chune gaye
    chosen = [0] * n
    c = capacity
    for i in range(n, 0, -1):
        if dp[i][c] != dp[i - 1][c]:
            chosen[i - 1] = 1
            c -= weights[i - 1]

    return dp[n][capacity], chosen, dp, time.perf_counter() - start


# ---------- 4. Space-optimized DP (1D array) ----------
def knapsack_dp_1d(weights, profits, capacity):
    """Sirf profit deta hai, par memory O(W) (2D mein O(n*W))."""
    start = time.perf_counter()
    dp = [0] * (capacity + 1)
    for w, p in zip(weights, profits):
        for c in range(capacity, w - 1, -1):   # peeche se, taaki item 2 baar na ho
            dp[c] = max(dp[c], dp[c - w] + p)
    return dp[capacity], time.perf_counter() - start


# ---------- 5. Brute Force (proof ke liye, sirf chhote n) ----------
def brute_force(weights, profits, capacity):
    """Saare 2^n combinations try karta hai."""
    n = len(weights)
    best, best_set = 0, ()
    for r in range(n + 1):
        for combo in combinations(range(n), r):
            w = sum(weights[i] for i in combo)
            if w <= capacity:
                p = sum(profits[i] for i in combo)
                if p > best:
                    best, best_set = p, combo
    return best, best_set


if __name__ == "__main__":
    import pandas as pd

    df = pd.read_csv("data/products.csv")
    names = df["product"].tolist()
    weights = df["weight"].tolist()
    profits = df["profit"].tolist()
    capacity = 30

    fg, frac, t1 = fractional_greedy(weights, profits, capacity)
    g01, ch_g, t2 = greedy_01(weights, profits, capacity)
    dp_p, ch_dp, table, t3 = knapsack_dp(weights, profits, capacity)
    dp1, t4 = knapsack_dp_1d(weights, profits, capacity)

    print(f"Capacity: {capacity} kg\n")
    print(f"Fractional Greedy (upper bound): {fg:.1f}   [{t1:.6f}s]")
    print(f"Greedy 0/1:                      {g01}   [{t2:.6f}s]")
    print(f"DP 0/1 (optimal):                {dp_p}   [{t3:.6f}s]")
    print(f"DP 1D check:                     {dp1}   [{t4:.6f}s]")
    print(f"\nDP ne Greedy 0/1 se {dp_p - g01} zyada profit diya\n")

    print("DP ke chune hue products:")
    for i, flag in enumerate(ch_dp):
        if flag:
            print(f"  {names[i]:<18} {weights[i]:>3} kg   {profits[i]:>5}")
    print(f"  Total weight: {sum(w for w, f in zip(weights, ch_dp) if f)} kg")