import random

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from knapsack import fractional_greedy, greedy_01, knapsack_dp, knapsack_dp_1d

st.set_page_config(page_title="StockSmart", page_icon="📦", layout="wide")

# ---------- Sidebar: appearance ----------
try:
    BASE = st.context.theme.type or "dark"
except Exception:
    BASE = st.get_option("theme.base") or "dark"

ACCENTS = {
    "Purple": ("#6d4fd8", "#5b8dd6", "#7fb0d6"),
    "Emerald": ("#047857", "#10b981", "#6ee7b7"),
    "Sunset": ("#ea580c", "#f59e0b", "#f472b6"),
    "Ocean": ("#0369a1", "#0ea5e9", "#67e8f9"),
}
# name: (page bg, sidebar bg, mode)
BGS = {
    "Default": None,
    "Midnight Navy": ("#0b1220", "#111a2e", "dark"),
    "Pure Black": ("#000000", "#0d0d0d", "dark"),
    "Deep Purple": ("#140b2e", "#1e1245", "dark"),
    "Forest Green": ("#06140f", "#0d2a1f", "dark"),
    "Soft White": ("#f8fafc", "#eef2f7", "light"),
    "Warm Cream": ("#faf7f2", "#efe9df", "light"),
}

st.sidebar.title("📦 StockSmart")
accent = st.sidebar.selectbox("Accent color", list(ACCENTS), key="accent")
bg = st.sidebar.selectbox("Background", list(BGS), key="bg")
a1, a2, a3 = ACCENTS[accent]

MODE = BGS[bg][2] if BGS[bg] else BASE

PAL = {
    "dark": dict(card="#161b2b", txt="#ffffff", sub="#cbd5e1", lab="#9ca3af",
                 sel="#12301f", rej="#1a2233", rejb="#374151"),
    "light": dict(card="#ffffff", txt="#111827", sub="#4b5563", lab="#6b7280",
                  sel="#dcfce7", rej="#f1f5f9", rejb="#cbd5e1"),
}[MODE]

CSS = """
<style>
.hero{background:linear-gradient(135deg,__A1__,__A2__ 60%,__A3__);
 padding:28px 32px;border-radius:24px;margin-bottom:18px}
.hero h1{margin:0;font-size:2.3rem;color:#fff !important}
.hero p{color:#f8fafc !important;font-size:1.1rem;margin:8px 0 14px}
.hero .pill{display:inline-block;background:rgba(255,255,255,.25);color:#fff !important;
 padding:6px 16px;border-radius:20px;margin-right:8px;font-size:.9rem}
.kcard{background:__CARD__;border-radius:16px;padding:16px 20px;
 border-left:6px solid var(--c);box-shadow:0 1px 4px rgba(0,0,0,.15)}
.kcard .l{color:__LAB__;font-size:.75rem;letter-spacing:.1em;text-transform:uppercase}
.kcard .v{font-size:2rem;font-weight:700;color:__TXT__}
.kcard .s{color:__SUB__;font-size:.9rem}
.item{padding:8px 12px;margin-bottom:6px;border-radius:8px;color:__TXT2__}
</style>
"""
for k, v in {"__A1__": a1, "__A2__": a2, "__A3__": a3, "__CARD__": PAL["card"],
             "__LAB__": PAL["lab"], "__TXT__": PAL["txt"], "__SUB__": PAL["sub"],
             "__TXT2__": "#111827" if MODE == "light" else "#e5e7eb"}.items():
    CSS = CSS.replace(k, v)
st.markdown(CSS, unsafe_allow_html=True)

if BGS[bg]:
    page_bg, side_bg, mode = BGS[bg]
    text_fix = ""
    if mode == "light":
        text_fix = (".stApp p,.stApp label,.stApp li,.stApp h1,.stApp h2,.stApp h3,"
                    ".stApp h4,.stApp [data-testid='stMarkdownContainer'],"
                    ".stApp [data-testid='stWidgetLabel']{color:#111827;}")
    st.markdown(
        f"<style>.stApp{{background:{page_bg};}}"
        f"[data-testid='stSidebar']{{background:{side_bg};}}"
        f"[data-testid='stHeader']{{background:transparent;}}{text_fix}</style>",
        unsafe_allow_html=True,
    )


def kcard(label, value, sub, color):
    return (f'<div class="kcard" style="--c:{color}"><div class="l">{label}</div>'
            f'<div class="v">{value}</div><div class="s">{sub}</div></div>')


# ---------- State ----------
if "df" not in st.session_state:
    st.session_state.df = pd.read_csv("data/products.csv")[["product", "weight", "profit"]]
    st.session_state.ver = 0
st.session_state.setdefault("capacity", 30)


def _set(df, cap):
    st.session_state.df = df
    st.session_state.capacity = int(cap)
    st.session_state.ver += 1


def load_demo():
    _set(pd.read_csv("data/products.csv")[["product", "weight", "profit"]], 30)


def load_trap():
    _set(pd.DataFrame({"product": ["Laptop", "Phone", "Monitor"],
                       "weight": [10, 20, 30], "profit": [60, 100, 120]}), 50)


def load_random():
    rng = random.Random()
    n = st.session_state.nrand
    df = pd.DataFrame({"product": [f"Item {i+1}" for i in range(n)],
                       "weight": [rng.randint(1, 20) for _ in range(n)],
                       "profit": [rng.randint(20, 500) for _ in range(n)]})
    _set(df, int(df["weight"].sum() * 0.4))


# ---------- Hero ----------
st.markdown("""<div class="hero"><h1>📦 StockSmart: Warehouse Profit Optimizer</h1>
<p>Pick the most profitable products without exceeding your storage capacity.</p>
<span class="pill">Greedy: Fractional Knapsack</span>
<span class="pill">Dynamic Programming: 0/1 Knapsack</span></div>""",
            unsafe_allow_html=True)

# ---------- Sidebar: data ----------
st.sidebar.number_input("Storage capacity (kg)", 1, 10000, key="capacity")
st.sidebar.subheader("Load data")
st.sidebar.button("Load demo data", on_click=load_demo, width="stretch")
st.sidebar.button("🪤 Greedy Trap demo", on_click=load_trap, width="stretch")
st.sidebar.slider("Random products", 5, 40, 10, key="nrand")
st.sidebar.button("Generate random data", on_click=load_random, width="stretch")
up = st.sidebar.file_uploader("Or upload CSV (product, weight, profit)", type="csv")
if up and st.session_state.get("last_up") != up.name:
    u = pd.read_csv(up)
    u.columns = [c.strip().lower() for c in u.columns]
    if {"product", "weight", "profit"} <= set(u.columns):
        st.session_state.last_up = up.name
        _set(u[["product", "weight", "profit"]], st.session_state.capacity)
        st.rerun()
    else:
        st.sidebar.error("The CSV must have these columns: product, weight, profit")

# ---------- Tabs ----------
t1, t2, t3, t4, t5 = st.tabs(["1. Inventory", "2. Results", "3. DP Table",
                              "4. What-if", "5. Benchmark"])

with t1:
    st.write("Edit the table directly. Use the **+** row at the bottom to add a product, "
             "or select a row and press **Delete** to remove it.")
    edited = st.data_editor(st.session_state.df, num_rows="dynamic",
                            width="stretch",
                            key=f"editor{st.session_state.ver}")

df = edited.dropna()
df = df[(df["weight"] > 0) & (df["profit"] >= 0)].copy()
if df.empty:
    st.warning("Please add at least one valid product.")
    st.stop()
df["weight"] = df["weight"].astype(int)
df["profit"] = df["profit"].astype(int)
names, weights, profits = df["product"].tolist(), df["weight"].tolist(), df["profit"].tolist()
n, capacity = len(names), int(st.session_state.capacity)

fg, frac, t_fg = fractional_greedy(weights, profits, capacity)
g01, ch_g, t_g = greedy_01(weights, profits, capacity)
dp_p, ch_dp, table, t_dp = knapsack_dp(weights, profits, capacity)
gap = dp_p - g01
used_dp = sum(w for w, f in zip(weights, ch_dp) if f)
used_g = sum(w for w, f in zip(weights, ch_g) if f)

FONT = "#111827" if MODE == "light" else "#e5e7eb"


def style(fig, h):
    fig.update_layout(height=h, paper_bgcolor="rgba(0,0,0,0)",
                      plot_bgcolor="rgba(0,0,0,0)", font=dict(color=FONT),
                      margin=dict(t=30, b=10))
    return fig


with t1:
    a, b, c = st.columns(3)
    a.markdown(kcard("Products", n, "items in inventory", "#7c5cf0"), unsafe_allow_html=True)
    b.markdown(kcard("Total weight", sum(weights), "if everything is stored", "#5b9bd5"), unsafe_allow_html=True)
    c.markdown(kcard("Total profit", sum(profits), "if everything is sold", "#4caf50"), unsafe_allow_html=True)
    st.markdown("#### Profit per unit of weight (higher ratio = greedy picks it first)")
    order = sorted(range(n), key=lambda i: profits[i] / weights[i], reverse=True)
    fig = go.Figure(go.Bar(x=[names[i] for i in order],
                           y=[profits[i] / weights[i] for i in order],
                           marker_color=a2))
    st.plotly_chart(style(fig, 300), width="stretch")

with t2:
    k1, k2, k3, k4 = st.columns(4)
    k1.markdown(kcard("DP profit (optimal)", f"₹{dp_p:,}", f"{used_dp}/{capacity} kg used", "#22c55e"), unsafe_allow_html=True)
    k2.markdown(kcard("Greedy 0/1 profit", f"₹{g01:,}", f"{used_g}/{capacity} kg used", "#f59e0b"), unsafe_allow_html=True)
    k3.markdown(kcard("Fractional (upper bound)", f"₹{fg:,.0f}", "items can be split", "#5b9bd5"), unsafe_allow_html=True)
    k4.markdown(kcard("Greedy's loss", f"₹{gap:,}", f"{(gap / dp_p * 100 if dp_p else 0):.1f}% less profit", "#ef4444"), unsafe_allow_html=True)
    st.write("")

    if gap > 0:
        missed = [names[i] for i in range(n) if ch_dp[i] and not ch_g[i]]
        taken = [names[i] for i in range(n) if ch_g[i] and not ch_dp[i]]
        st.success(f"DP earned ₹{gap:,} more than Greedy. Greedy picked {', '.join(taken) or 'nothing extra'}, "
                   f"but missed {', '.join(missed) or 'nothing'}.")
    else:
        st.info("At this capacity, Greedy and DP give the same profit. Try the 'Greedy Trap demo' in the sidebar.")

    def gauge(used, title):
        f = go.Figure(go.Indicator(mode="gauge+number", value=used,
                                   number={"suffix": f" / {capacity} kg"}, title={"text": title},
                                   gauge={"axis": {"range": [0, capacity]}, "bar": {"color": "#22c55e"}}))
        return style(f, 250)

    g1, g2 = st.columns(2)
    g1.plotly_chart(gauge(used_dp, "DP: warehouse usage"), width="stretch")
    g2.plotly_chart(gauge(used_g, "Greedy 0/1: warehouse usage"), width="stretch")

    def cards(chosen, title, color):
        st.markdown(f"#### {title}")
        for i in range(n):
            bgc, bd, tag = (PAL["sel"], color, "✅") if chosen[i] else (PAL["rej"], PAL["rejb"], "▫️")
            st.markdown(f'<div class="item" style="background:{bgc};border-left:5px solid {bd}">'
                        f'{tag} <b>{names[i]}</b> &nbsp; {weights[i]} kg | ₹{profits[i]} | '
                        f'ratio {profits[i] / weights[i]:.1f}</div>', unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        cards(ch_dp, "🧠 DP (optimal)", "#22c55e")
    with c2:
        cards(ch_g, "⚡ Greedy 0/1", "#f59e0b")
    st.caption(f"Time: DP {t_dp:.6f}s | Greedy {t_g:.6f}s")

    out = df.assign(DP_selected=ch_dp, Greedy_selected=ch_g)
    st.download_button("⬇️ Download result CSV", out.to_csv(index=False), "stocksmart_result.csv")

with t3:
    st.write("Each cell shows the best profit at that capacity. "
             "White diamonds mark the path DP took (where an item was picked).")
    if capacity * n > 20000:
        st.warning("The table is too large. Reduce the capacity or number of items to see the heatmap.")
    else:
        path_x, path_y, c = [], [], capacity
        for i in range(n, 0, -1):
            if table[i][c] != table[i - 1][c]:
                path_x.append(c)
                path_y.append(i)
                c -= weights[i - 1]
        hm = go.Figure(go.Heatmap(z=table, x=list(range(capacity + 1)),
                                  y=["(no items)"] + names, colorscale="Viridis"))
        hm.add_trace(go.Scatter(x=path_x, y=[names[i - 1] for i in path_y], mode="markers",
                                marker=dict(color="white", size=11, symbol="diamond",
                                            line=dict(color="black", width=1)),
                                name="Item picked"))
        hm.update_layout(xaxis_title="Capacity (kg)")
        st.plotly_chart(style(hm, 520), width="stretch")

with t4:
    total_w = sum(weights)
    _, _, big, _ = knapsack_dp(weights, profits, total_w)
    curve = big[n]

    st.markdown("#### Profit curve: how profit grows with capacity")
    cf = go.Figure(go.Scatter(x=list(range(total_w + 1)), y=curve, mode="lines",
                              line=dict(color="#22c55e", width=3)))
    cf.add_vline(x=capacity, line_dash="dash", line_color="#f59e0b")
    cf.update_layout(xaxis_title="Capacity (kg)", yaxis_title="Max profit")
    st.plotly_chart(style(cf, 320), width="stretch")

    st.markdown("#### Capacity planner")
    target = st.number_input("Target profit (₹)", 1, int(sum(profits)),
                             min(int(sum(profits) * 0.5), int(sum(profits))))
    need = next((cp for cp in range(total_w + 1) if curve[cp] >= target), None)
    if need is None:
        st.error("This profit is not achievable with the available products.")
    else:
        st.success(f"To earn ₹{target:,}, you need a minimum capacity of **{need} kg**.")

    st.markdown("#### Sensitivity: which product hurts the most if removed?")
    rows = []
    for i in range(n):
        if ch_dp[i]:
            w2 = weights[:i] + weights[i + 1:]
            p2 = profits[:i] + profits[i + 1:]
            rows.append((names[i], dp_p - knapsack_dp_1d(w2, p2, capacity)[0]))
    if rows:
        rows.sort(key=lambda r: r[1], reverse=True)
        sf = go.Figure(go.Bar(x=[r[0] for r in rows], y=[r[1] for r in rows], marker_color="#ef4444"))
        sf.update_layout(yaxis_title="Profit loss (₹)")
        st.plotly_chart(style(sf, 300), width="stretch")
        st.info(f"⭐ Star product: **{rows[0][0]}** (removing it costs ₹{rows[0][1]:,})")

with t5:
    st.write("Greedy vs DP execution time on random items (capacity = 40% of total weight).")
    if st.button("▶ Run benchmark"):
        rng, res = random.Random(7), []
        bar = st.progress(0.0)
        sizes = [10, 50, 100, 200, 500]
        for k, m in enumerate(sizes):
            w = [rng.randint(1, 20) for _ in range(m)]
            p = [rng.randint(10, 500) for _ in range(m)]
            cp = int(sum(w) * 0.4)
            _, _, tg = greedy_01(w, p, cp)
            _, _, _, td = knapsack_dp(w, p, cp)
            _, t1d = knapsack_dp_1d(w, p, cp)
            res.append((m, tg, td, t1d))
            bar.progress((k + 1) / len(sizes))
        bf = go.Figure()
        for j, label in [(1, "Greedy 0/1"), (2, "DP 2D"), (3, "DP 1D")]:
            bf.add_trace(go.Scatter(x=[r[0] for r in res], y=[r[j] for r in res],
                                    mode="lines+markers", name=label))
        bf.update_layout(yaxis_type="log", xaxis_title="Items",
                         yaxis_title="Time (s, log scale)")
        st.plotly_chart(style(bf, 380), width="stretch")
        st.dataframe(pd.DataFrame(res, columns=["Items", "Greedy (s)", "DP 2D (s)", "DP 1D (s)"]),
                     width="stretch")