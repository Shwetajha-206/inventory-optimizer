import random

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from knapsack import fractional_greedy, greedy_01, knapsack_dp, knapsack_dp_1d

SIZES = [10, 50, 100, 200, 500, 1000]
CAPACITY_RATIO = 0.4   # capacity = total weight ka 40%
TRIALS = 3


def make_items(n, rng):
    weights = [rng.randint(1, 20) for _ in range(n)]
    profits = [rng.randint(10, 500) for _ in range(n)]
    return weights, profits


def main():
    rng = random.Random(42)
    rows = []

    for n in SIZES:
        t_fg = t_g01 = t_dp = t_dp1 = 0.0
        gap = 0.0
        for _ in range(TRIALS):
            w, p = make_items(n, rng)
            cap = int(sum(w) * CAPACITY_RATIO)

            _, _, a = fractional_greedy(w, p, cap)
            g, _, b = greedy_01(w, p, cap)
            d, _, _, c = knapsack_dp(w, p, cap)
            _, e = knapsack_dp_1d(w, p, cap)

            t_fg += a; t_g01 += b; t_dp += c; t_dp1 += e
            gap += (d - g) / d * 100

        rows.append({
            "n": n,
            "fg": t_fg / TRIALS, "g01": t_g01 / TRIALS,
            "dp": t_dp / TRIALS, "dp1": t_dp1 / TRIALS,
            "gap": gap / TRIALS,
        })

    print(f"{'Items':<8}{'Frac(s)':<12}{'Greedy01(s)':<14}"
          f"{'DP 2D(s)':<12}{'DP 1D(s)':<12}{'Profit gap %':<12}")
    print("-" * 70)
    for r in rows:
        print(f"{r['n']:<8}{r['fg']:<12.6f}{r['g01']:<14.6f}"
              f"{r['dp']:<12.6f}{r['dp1']:<12.6f}{r['gap']:<12.3f}")

    ns = [r["n"] for r in rows]
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4.5))

    ax1.plot(ns, [r["g01"] for r in rows], "s-", label="Greedy 0/1")
    ax1.plot(ns, [r["dp"] for r in rows], "o-", label="DP 2D")
    ax1.plot(ns, [r["dp1"] for r in rows], "^-", label="DP 1D")
    ax1.set_yscale("log")
    ax1.set_xlabel("Number of items")
    ax1.set_ylabel("Time (seconds, log scale)")
    ax1.set_title("Execution Time")
    ax1.legend()
    ax1.grid(True, alpha=0.3)

    ax2.bar([str(n) for n in ns], [r["gap"] for r in rows], color="#e67e22")
    ax2.set_xlabel("Number of items")
    ax2.set_ylabel("Profit lost by Greedy 0/1 (%)")
    ax2.set_title("Greedy vs DP: Profit Gap")
    ax2.grid(True, axis="y", alpha=0.3)
    plt.tight_layout()
    plt.savefig("benchmark_results.png", dpi=150)
    print("\nGraph saved: benchmark_results.png")


if __name__ == "__main__":
    main()
