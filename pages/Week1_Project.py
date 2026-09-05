import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st
import yfinance as yf

from core import progress, theme
from core.day01_vectors import Vectors
from core.device import is_mobile

st.set_page_config(
    page_title="Week 1 Project — ThefacelessQuant",
    page_icon="assets/fq.ico",
    layout="wide",
)
theme.inject_base_css()
theme.render_sidebar_brand()

mobile = is_mobile()

# --- Assets & Benchmark Definition ---
TICKERS = ["AAPL", "JPM", "JNJ"]
SECTORS = ["Technology", "Financials", "Healthcare"]
TICKER_LABELS = [f"{t} ({s})" for t, s in zip(TICKERS, SECTORS)]
BENCHMARK = np.array([1 / 3, 1 / 3, 1 / 3])
TICKER_COLORS = [theme.LINEAR_ALGEBRA, theme.CALCULUS, theme.QUANT_FINANCE]


@st.cache_data(ttl=3600, show_spinner="Fetching live prices...")
def fetch_live_returns(tickers):
  try:
    data = yf.download(
        tickers,
        period="15d",
        interval="1d",
        progress=False,
        auto_adjust=True,
    )["Close"]
    data = data[tickers]
    rets = data.pct_change().dropna().tail(5)
    if len(rets) < 2:
      raise ValueError("Not enough live data returned")
    dates = [d.strftime("%b %d") for d in rets.index]
    return rets.values, dates, True
  except Exception:
    fallback = np.array([
        [0.010, -0.004, 0.006],
        [-0.006, 0.008, 0.003],
        [0.012, -0.002, 0.005],
        [0.003, 0.006, -0.004],
        [0.008, 0.001, 0.007],
    ])
    return fallback, ["Day 1", "Day 2", "Day 3", "Day 4", "Day 5"], False


RETURNS, RETURN_DATES, LIVE_DATA = fetch_live_returns(TICKERS)


def math_code_card(latex_lines, code):
  with st.expander("Show Math & Code"):
    for line in latex_lines:
      st.latex(line)
    st.code(code, language="python")


# ---------------------------------------------------------------- Top Navigation
nav_left, nav_right = st.columns(2)
with nav_left:
  st.page_link("pages/5_Linear_Systems.py", label="Back: Day 5, Linear Systems")
with nav_right:
  st.page_link("Home.py", label="Next: Day 6, Matrix Inverse", disabled=True)

# ---------------------------------------------------------------- Header
completed_projects = progress.get_completed_projects()
badge = " ✓" if 1 in completed_projects else ""
st.markdown(
    f"<p style='color:{theme.CALCULUS}; font-weight:600; letter-spacing:0.08em; "
    "text-transform:uppercase; font-size:0.8rem; margin-bottom:2px;'>"
    "Week 1 Project · Linear Algebra</p>"
    f"<h1 style='margin-top:0;'>Build Your First Quant Portfolio{badge}</h1>"
    "<p class='hero-subtitle'>Five days of theory. One production-grade"
    " portfolio. Apply linear algebra concepts sequentially to build,"
    " stress-test, and optimize a single portfolio from scratch.</p>",
    unsafe_allow_html=True,
)

with st.container(border=True):
  st.markdown(
      "<p><strong>The scenario:</strong> As an incoming quantitative analyst,"
      f" your task is to construct a three-asset cross-sector portfolio: "
      f"{', '.join(TICKER_LABELS)}. You will evaluate alignment against an"
      " equal-weight benchmark, simulate historical returns, execute a tactical"
      " tilt, and solve a constrained system to hit exact factor targets.</p>",
      unsafe_allow_html=True,
  )
  if LIVE_DATA:
    st.caption(
        "Live daily closes via Yahoo Finance,"
        f" {RETURN_DATES[0]} \u2013 {RETURN_DATES[-1]}."
    )
  else:
    st.caption(
        "Using fixed illustrative returns — live market data unavailable right"
        " now."
    )

st.write("")

# ---------------------------------------------------------------- Mobile-Ready Navigation
STEPS = [
    "1. Allocate Weights",
    "2. Benchmark Alignment",
    "3. Historical Backtest",
    "4. Apply Strategy",
    "5. Hit Your Target",
    "Summary",
]

st.session_state.setdefault("w1_weights", np.array([0.40, 0.35, 0.25]))
st.session_state.setdefault("step_idx", 0)


def next_step():
  if st.session_state.step_idx < len(STEPS) - 1:
    st.session_state.step_idx += 1


def prev_step():
  if st.session_state.step_idx > 0:
    st.session_state.step_idx -= 1


try:
  selected_step = st.segmented_control(
      "Workflow Navigation",
      options=STEPS,
      default=STEPS[st.session_state.step_idx],
      label_visibility="collapsed",
  )
  if selected_step:
    st.session_state.step_idx = STEPS.index(selected_step)
except AttributeError:
  selected_step = st.radio(
      "Workflow Navigation",
      options=STEPS,
      index=st.session_state.step_idx,
      horizontal=True,
      label_visibility="collapsed",
  )
  if selected_step:
    st.session_state.step_idx = STEPS.index(selected_step)

current_step = st.session_state.step_idx
st.markdown(f"### {STEPS[current_step]}")

# ================================================================ STEP 1 — VECTORS
if current_step == 0:
  st.markdown(
      f"<p style='color:{theme.TEXT_MUTED};'>Step 1: Define your capital"
      f" allocation vector w across {', '.join(TICKER_LABELS)}. Portfolio"
      " weights are fundamentally vectors whose components sum to 1.0 (fully"
      " invested).</p>",
      unsafe_allow_html=True,
  )

  slider_cols = st.columns(1 if mobile else 3)
  w1 = slider_cols[0].slider(
      f"{TICKERS[0]} WEIGHT",
      0.0,
      1.0,
      float(st.session_state["w1_weights"][0]),
      0.05,
      key="w1_s1",
  )
  w2 = slider_cols[1 if not mobile else 0].slider(
      f"{TICKERS[1]} WEIGHT",
      0.0,
      1.0,
      float(st.session_state["w1_weights"][1]),
      0.05,
      key="w1_s2",
  )
  w3 = slider_cols[2 if not mobile else 0].slider(
      f"{TICKERS[2]} WEIGHT",
      0.0,
      1.0,
      float(st.session_state["w1_weights"][2]),
      0.05,
      key="w1_s3",
  )

  weights = np.array([w1, w2, w3])
  total = float(weights.sum())
  st.session_state["w1_weights"] = weights

  if abs(total - 1.0) > 1e-6:
    st.warning(
        f"Weights sum to {total:.2f}, not 1.00. Adjust sliders to satisfy the"
        " budget constraint."
    )

  exposure = Vectors().compute(v=weights)["norm_v"]

  m_cols = st.columns(2)
  m_cols[0].metric("Portfolio Weights (w)", f"[{w1:.2f}, {w2:.2f}, {w3:.2f}]")
  m_cols[1].metric("Weight Concentration (‖w‖₂)", f"{exposure:.3f}")

  fig_alloc = go.Figure()
  for i, ticker in enumerate(TICKERS):
    fig_alloc.add_trace(
        go.Bar(
            y=["Allocation"],
            x=[weights[i]],
            name=f"{ticker} ({SECTORS[i]})",
            orientation="h",
            marker_color=TICKER_COLORS[i],
            text=[f"{ticker} {weights[i]:.0%}"],
            textposition="inside",
        )
    )
  fig_alloc.update_layout(
      template="quant_dark",
      barmode="stack",
      height=120 if mobile else 140,
      margin=dict(l=5, r=5, t=10, b=10),
      showlegend=False,
      xaxis=dict(range=[0, max(1.0, total)]),
  )
  st.plotly_chart(
      fig_alloc, use_container_width=True, config={"displayModeBar": False}
  )

  math_code_card(
      [
          r"\mathbf{w} = [w_1, w_2, w_3], \qquad \lVert \mathbf{w} \rVert_2 ="
          r" \sqrt{\textstyle\sum_i w_i^2}"
      ],
      f"weights = np.array([{w1:.2f}, {w2:.2f}, {w3:.2f}])\n"
      "exposure = np.linalg.norm(weights)",
  )

# ================================================================ STEP 2 — DOT PRODUCT
elif current_step == 1:
  weights = st.session_state["w1_weights"]
  st.markdown(
      f"<p style='color:{theme.TEXT_MUTED};'>Step 2: How "
      "close is your portfolio to the market benchmark — an equal-weight (for"
      " this project it is assummed marke benchmark is an equal weight"
      " portfolio). The dot product and cosine similarity quantify portfolio"
      " tilt. </p>",
      unsafe_allow_html=True,
  )

  dot = float(np.dot(weights, BENCHMARK))
  norm_w = float(np.linalg.norm(weights))
  norm_b = float(np.linalg.norm(BENCHMARK))
  denom = norm_w * norm_b
  cos_theta = max(-1.0, min(1.0, dot / denom)) if denom > 1e-9 else 0.0
  angle_deg = float(np.degrees(np.arccos(cos_theta)))

  m_cols = st.columns(1 if mobile else 3)
  m_cols[0].metric("Inner Product (w · b)", f"{dot:.3f}")
  m_cols[1 if not mobile else 0].metric(
      "Cosine Similarity (cos θ)", f"{cos_theta:.3f}"
  )
  m_cols[2 if not mobile else 0].metric(
      "Angular Deviation (θ)", f"{angle_deg:.1f}°"
  )

  if angle_deg < 10:
    st.info("Closet indexer: Book closely tracks equal-weight allocation.")
  elif angle_deg < 25:
    st.info("Modest tilt: Active positioning with disciplined tracking.")
  else:
    st.info("High conviction: Substantial tilt away from benchmark neutrality.")

  math_code_card(
      [
          r"\cos\theta = \frac{\mathbf{w} \cdot \mathbf{b}}{\lVert"
          r" \mathbf{w} \rVert\, \lVert \mathbf{b} \rVert}"
      ],
      "benchmark = np.array([1/3, 1/3, 1/3])\n"
      "cos_theta = np.dot(weights, benchmark) / (np.linalg.norm(weights) *"
      " np.linalg.norm(benchmark))\n"
      "angle_deg = np.degrees(np.arccos(cos_theta))",
  )

# ================================================================ STEP 3 — MATRICES
elif current_step == 2:
  weights = st.session_state["w1_weights"]
  st.markdown(
      f"<p style='color:{theme.TEXT_MUTED};'> Step 3: Evaluate out-of-sample"
      " portfolio performance over the past 5 trading sessions. Vectorized"
      " returns are computed via matrix-vector product (r_port = R @ w). ",
      unsafe_allow_html=True,
  )

  portfolio_returns = RETURNS @ weights
  bench_returns = RETURNS @ BENCHMARK
  mean_return = float(portfolio_returns.mean()) * 100
  cumulative = float(np.prod(1 + portfolio_returns) - 1) * 100

  m_cols = st.columns(2)
  m_cols[0].metric(
      "Expected Daily Return",
      f"{mean_return:+.2f}%",
  )
  m_cols[1].metric(
      f"{len(RETURN_DATES)}-Day Cumulative Return",
      f"{cumulative:+.2f}%",
  )

  fig_bar = go.Figure()
  colors = [
      theme.PROBABILITY if v >= 0 else theme.QUANT_FINANCE
      for v in portfolio_returns
  ]
  fig_bar.add_trace(
      go.Bar(
          x=RETURN_DATES,
          y=portfolio_returns,
          marker_color=colors,
          text=[f"{v*100:+.2f}%" for v in portfolio_returns],
          textposition="outside",
          name="Your book",
      )
  )
  fig_bar.update_layout(
      template="quant_dark",
      height=260 if mobile else 300,
      showlegend=False,
      margin=dict(l=10, r=10, t=30, b=10),
      title="Daily Portfolio Returns",
  )
  st.plotly_chart(
      fig_bar, use_container_width=True, config={"displayModeBar": False}
  )

  cum_port = np.cumprod(1 + portfolio_returns) - 1
  cum_bench = np.cumprod(1 + bench_returns) - 1
  fig_line = go.Figure()
  fig_line.add_trace(
      go.Scatter(
          x=RETURN_DATES,
          y=cum_port,
          mode="lines+markers",
          line=dict(color=theme.LINEAR_ALGEBRA, width=3),
          name="Strategy",
      )
  )
  fig_line.add_trace(
      go.Scatter(
          x=RETURN_DATES,
          y=cum_bench,
          mode="lines+markers",
          line=dict(color=theme.TEXT_MUTED, width=2, dash="dot"),
          name="Benchmark",
      )
  )
  fig_line.update_layout(
      template="quant_dark",
      height=260 if mobile else 300,
      margin=dict(l=10, r=10, t=35, b=10),
      title="Cumulative Return vs Benchmark",
      legend=dict(
          orientation="h", yanchor="bottom", y=-0.3 if mobile else 0.95
      ),
  )
  st.plotly_chart(
      fig_line, use_container_width=True, config={"displayModeBar": False}
  )

  math_code_card(
      [r"\mathbf{r}_{\text{port}} = R\,\mathbf{w}"],
      f"R = np.array({np.round(RETURNS, 4).tolist()})  # Shape (5, 3)\n"
      "portfolio_returns = R @ weights  # (5, 3) @ (3, 1) -> (5, 1)\n"
      "cumulative = np.cumprod(1 + portfolio_returns) - 1",
  )

# ================================================================ STEP 4 — LINEAR TRANSFORMATIONS
elif current_step == 3:
  weights = st.session_state["w1_weights"]
  st.markdown(
      f"<p style='color:{theme.TEXT_MUTED};'>Step 4: Turn performance into"
      " action. Rebalancing rules work as linear transformations: we multiply"
      " your portfolio vector by a diagonal scaling matrix to resize each"
      " stock.</p>",
      unsafe_allow_html=True,
  )

  STRATEGIES = {
      "Momentum: Overweight winner, underweight loser": (1.5, 1.0, 0.5),
      "De-Risk: Scale all positions down by 50%": (0.5, 0.5, 0.5),
      "Lever Up: Scale all positions up by 50%": (1.5, 1.5, 1.5),
      "Hedge: Short the worst performer": (1.0, 1.0, -1.0),
  }
  strategy_label = st.radio(
      "Pick a strategy rule:", list(STRATEGIES.keys()), key="w1_strategy"
  )
  s1, s2, s3 = STRATEGIES[strategy_label]

  A = np.diag([s1, s2, s3])
  new_weights = A @ weights
  delta = new_weights - weights
  st.session_state["w1_strategy_tilt"] = float(new_weights[0] - new_weights[1])

  st.markdown("**Rebalance Execution & Required Trades:**")
  rows = []
  for i, ticker in enumerate(TICKERS):
    rows.append(
        f"| {ticker} ({SECTORS[i]}) | {weights[i]:.3f} | {new_weights[i]:.3f} |"
        f" {delta[i]:+.3f} |"
    )
  st.markdown(
      "| Stock | Before | After | Δw (Trade) |\n|---|---|---|---|\n"
      + "\n".join(rows)
  )

  new_total = new_weights.sum()
  st.markdown(
      f"New weights sum to **{new_total:.2f}** — "
      + (
          "fully invested."
          if abs(new_total - 1.0) < 1e-6
          else "budget constraint violated ($w_{new} \\neq 1.00$)."
      )
  )
  st.caption(
      f"Tactical spread: {TICKERS[0]} − {TICKERS[1]} ="
      f" {new_weights[0] - new_weights[1]:+.3f}. In Step 5, we restore budget"
      " neutrality while locking in this exact tilt."
  )

  math_code_card(
      [
          r"A = \operatorname{diag}(s_1, s_2, s_3), \qquad"
          r" \mathbf{w}_{\text{new}} = A\mathbf{w}"
      ],
      f"A = np.diag([{s1}, {s2}, {s3}])\n"
      "new_weights = A @ weights\n"
      "trades_needed = new_weights - weights",
  )

# ================================================================ STEP 5 — LINEAR SYSTEMS
elif current_step == 4:
  st.markdown(
      f"<p style='color:{theme.TEXT_MUTED};'>Last step: Find the unique"
      " allocation vector w that satisfies three market constraints"
      " simultaneously. We set up a 3 * 3 linear system (Aw = b) to solve for"
      " exact weights without guessing.</p>",
      unsafe_allow_html=True,
  )

  mean_returns = RETURNS.mean(axis=0)
  r1, r2, r3 = mean_returns
  tilt = st.session_state.get("w1_strategy_tilt", 0.0)

  st.markdown(
      "**The 3 Market Constraints:**\n"
      "1. **Budget Constraint:** $w_1 + w_2 + w_3 = 1$ (fully invested capital)\n"
      "2. **Target Return:** $\\mathbb{E}[R]^T w = r_{\\text{target}}$ (historical expected daily return)\n"
      f"3. **Tactical Tilt:** $w_1 - w_2 = {tilt:+.3f}$ (from Step 4)"
  )

  w2_grid = np.linspace(0.0, 1.0, 401)
  feasible_targets = []
  for w2 in w2_grid:
    w1_candidate = w2 + tilt
    w3_candidate = 1.0 - w1_candidate - w2
    if -1e-9 <= w1_candidate <= 1 + 1e-9 and -1e-9 <= w3_candidate <= 1 + 1e-9:
      feasible_targets.append(r1 * w1_candidate + r2 * w2 + r3 * w3_candidate)

  if feasible_targets:
    t_min, t_max = min(feasible_targets), max(feasible_targets)
    margin = max((t_max - t_min) * 0.5, 0.0005)
    slider_min, slider_max = t_min - margin, t_max + margin
    default_target = (t_min + t_max) / 2
    st.caption(
        "Feasible long-only return bounds:"
        f" {t_min*100:.2f}% to {t_max*100:.2f}% daily."
    )
  else:
    slider_min, slider_max = float(mean_returns.min()), float(
        mean_returns.max()
    )
    default_target = float(mean_returns.mean())
    st.caption("Active tilt requires short positions for all target returns.")

  long_only = st.checkbox(
      "Enforce long-only (no shorting)", value=True, key="w1_longonly"
  )
  target_return = st.slider(
      "TARGET DAILY RETURN",
      float(slider_min),
      float(slider_max),
      float(default_target),
      0.0001,
      format="%.4f",
      key="w1_target5",
  )

  A = np.array([[1.0, 1.0, 1.0], [r1, r2, r3], [1.0, -1.0, 0.0]])
  b = np.array([1.0, target_return, tilt])
  det = float(np.linalg.det(A))

  if abs(det) < 1e-9:
    st.error("Singular matrix: No unique solution exists.")
  else:
    x = np.linalg.solve(A, b)
    m_cols = st.columns(1 if mobile else 3)
    m_cols[0].metric(f"{TICKERS[0]} Weight", f"{x[0]:.3f}")
    m_cols[1 if not mobile else 0].metric(f"{TICKERS[1]} Weight", f"{x[1]:.3f}")
    m_cols[2 if not mobile else 0].metric(f"{TICKERS[2]} Weight", f"{x[2]:.3f}")
    st.caption(f"det(A) = {det:.5f} ≠ 0 (unique solution confirmed).")

    infeasible = long_only and np.any(x < -1e-9)
    if infeasible:
      st.warning(
          "Infeasible under long-only bounds ($w_i < 0$). Lower the return"
          " target or reduce Step 4 tilt."
      )
    else:
      st.success("Feasible: Solution satisfies long-only non-negativity.")

  math_code_card(
      [
          r"A\mathbf{w} = \mathbf{b}, \quad A = \begin{bmatrix} 1 & 1 & 1 \\"
          r" \mathbb{E}[R_1] & \mathbb{E}[R_2] & \mathbb{E}[R_3] \\ 1 & -1 & 0"
          r" \end{bmatrix}, \quad \mathbf{b} = \begin{bmatrix} 1 \\"
          r" r_{\text{target}} \\ \text{tilt} \end{bmatrix}"
      ],
      "mean_returns = R.mean(axis=0)\n"
      "tilt = new_weights[0] - new_weights[1]\n"
      "A = np.array([\n"
      "    [1.0, 1.0, 1.0],\n"
      "    mean_returns,\n"
      "    [1.0, -1.0, 0.0]\n"
      "])\n"
      "b = np.array([1.0, target_return, tilt])\n"
      "w_solved = np.linalg.solve(A, b)",
  )

# ================================================================ SUMMARY
elif current_step == 5:
  weights = st.session_state["w1_weights"]
  st.markdown(
      "You built a quantitative portfolio pipeline from the ground up: moving"
      " from capital allocations to benchmark alignment, historical"
      " simulation, systematic tilting, and multi-constraint optimization."
  )

  with st.container(border=True):
    st.markdown(
        f"**Active Book:** {TICKERS[0]} {weights[0]:.0%} · {TICKERS[1]}"
        f" {weights[1]:.0%} · {TICKERS[2]} {weights[2]:.0%}"
    )
    st.markdown("""
        ---
        * **Day 1 (Vectors):** Allocation vector $w \in \mathbb{R}^3$
        * **Day 2 (Dot Product):** Alignment & tilt via $\cos \\theta$
        * **Day 3 (Matrix Multiply):** Historical backtest ($r = Rw$)
        * **Day 4 (Transformations):** Systematic rebalancing ($w_{\\text{new}} = Aw$)
        * **Day 5 (Linear Systems):** Exact multi-constraint solver ($Aw = b$)
        """)

  if 1 in completed_projects:
    st.success("Week 1 Project already marked complete.")
  else:
    if st.button(
        "Mark Week 1 Project Complete", type="primary", use_container_width=True
    ):
      progress.mark_project_complete(1)
      st.balloons()
      st.rerun()

# ---------------------------------------------------------------- Mobile Bottom Touch Bar
st.divider()
col_prev, col_spacer, col_next = st.columns([1, 1 if mobile else 2, 1])
with col_prev:
  st.button(
      "← Back",
      on_click=prev_step,
      disabled=(current_step == 0),
      use_container_width=True,
  )
with col_next:
  st.button(
      "Next →",
      on_click=next_step,
      disabled=(current_step == len(STEPS) - 1),
      type="primary",
      use_container_width=True,
  )

st.write("")
st.page_link("Home.py", label="Back to all concepts")