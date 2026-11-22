#  Intelligent Inventory Management Using Knapsack Optimization

## Problem Statement

A warehouse manager must select products to **maximize total profit** without exceeding a given **storage capacity**. Each product has a **weight** and a **profit** value. This project implements and compares:

- **Greedy (Fractional Knapsack)**: sort by profit/weight ratio, items can be split
- **Dynamic Programming (0/1 Knapsack)**: each item is taken whole or not at all

and compares their results and performance.

##  Features

- Select products under a capacity limit to maximize profit
- Greedy Fractional Knapsack and DP 0/1 Knapsack (2D and space-optimized 1D)
- Side-by-side comparison of total profit, selected items and profit loss
- Interactive Plotly charts
- Benchmark of execution time on random inputs (10 to 500 items)
- Products loaded from `data/products.csv`
- Unit tests

##  Project Structure

```
inventory-optimizer/
├── app.py               # Streamlit UI
├── knapsack.py          # Greedy and DP implementations
├── benchmark.py         # Runtime benchmarking
├── test_knapsack.py     # Unit tests
├── data/products.csv    # Product weight and profit data
├── benchmark_results.png
├── requirements.txt
└── README.md
```

## Getting Started

```
git clone https://github.com/Shwetajha-206/inventory-optimizer.git
cd inventory-optimizer
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m streamlit run app.py
```
App opens at `http://localhost:8501`.

Run tests: `python -m pytest test_knapsack.py`
Run benchmark: `python benchmark.py`

## Algorithms

| Approach | Time | Space | Result |
|----------|------|-------|--------|
| Greedy (Fractional) | O(n log n) | O(n) | Optimal for the fractional problem |
| DP 0/1 (2D) | O(n × W) | O(n × W) | Optimal for 0/1 |
| DP 0/1 (1D) | O(n × W) | O(W) | Optimal for 0/1 |

`n` = number of items, `W` = capacity.

**Greedy (Fractional):** sorts items by profit/weight ratio and fills the knapsack, taking a fraction of the last item if needed. It is very fast, and its profit is an **upper bound** for the 0/1 answer.

**DP (0/1):** builds a table of best profit for every item count and capacity. It is exact for whole items, but slower on large capacities.

## Comparison

Fractional greedy usually reports equal or higher profit than 0/1 DP because it may split items, which is not possible in a real warehouse. DP gives the true best selection of whole products, while greedy is much faster as the input grows. See `benchmark_results.png` for the runtime comparison.

## Tech Stack

Python, Streamlit, Plotly, Pandas

##  Author

[Shwetajha-206](https://github.com/Shwetajha-206)
