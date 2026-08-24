# The ThefacelessQuant Mentor Guide
### A beginner's complete roadmap to becoming a quant trader / researcher / investor
*Written for you — not for a university catalogue.*

---

## First, the honest conversation most roadmaps skip

Before anything else, you need to understand what you are actually training for, because the internet will pull you in three different directions at once and most of what you will read is either oversimplified or designed to sell you a course.

Here is what the industry actually looks like. There are three real paths, and they require different skills:

**Quant Researcher** — builds the models. Hunts for signals in historical data, tests hypotheses, writes the math that tells the trading system what to do. This is PhD-heavy at top hedge funds (Two Sigma, D.E. Shaw, Renaissance) but genuinely accessible at the research level with strong foundations and a good project portfolio. This is likely closest to what you want.

**Quant Trader** — takes the models live. Manages risk in real time, makes fast calls under pressure. Requires deep market intuition on top of the technical foundation.

**Quant Developer** — builds the systems. Turns research into code that executes in production. The most accessible entry point from a background of strong Python, even without a deep math background yet.

You are starting from beginner. The honest reality is this: **the math comes first, and it takes longer than most roadmaps admit.** Jim Simons was a world-class mathematician before he ever touched a market. Ernest Chan had a PhD in physics from Cornell. Emanuel Derman came from particle physics. This does not mean you need a PhD — it means the math is the actual job, and the finance is the application layer on top of it. Anyone who tells you to skip the math and jump to trading signals is selling you a shortcut that does not exist.

What you are building with ThefacelessQuant is exactly the right approach: learn the math properly, build in public, prove it with code, and let the portfolio of work speak for itself. That is a legitimate path in 2026 even without a traditional academic credential.

---

## The real skill stack, in order of dependency

Think of this as a dependency tree, not a list. You cannot skip a layer.

```
Layer 5 — Alpha Research & Live Systems         ← where you make money
Layer 4 — Quant Finance Models                  ← pricing, risk, portfolios
Layer 3 — Probability & Statistics              ← the language of uncertainty
Layer 2 — Calculus & Optimization               ← the tools for change
Layer 1 — Linear Algebra                        ← the structure of data
Layer 0 — Python & Data (runs in parallel)      ← the execution layer
```

The current 40-day roadmap hits all of these. What I am redesigning below is the **order within each layer**, the **real-world anchors at each step**, and the **pacing** so that you understand *why* each concept matters before you learn *how* it works.

---

## The redesigned curriculum: 6 phases, not 4 pillars

The original roadmap was structured by mathematical pillar (linear algebra, calculus, probability, quant finance). That is correct for a textbook. But a professional quant's mental model is structured by *task*, not by discipline. Here is how the same 40 concepts should be framed as you learn them — each day's concept is unchanged, but the context shifts:

---

### Phase 1 — The Language of Data (Weeks 1–2, Days 1–10)
*Linear Algebra. The tools every quant uses every day without thinking about them.*

The fundamental insight: financial data is not numbers in a spreadsheet, it is vectors and matrices. A portfolio is a vector. A returns table is a matrix. A risk model is a matrix factorisation. Learning linear algebra is not studying maths for its own sake — it is learning the native language of every model you will ever build.

| Day | Concept | What it actually does in the real world |
|---|---|---|
| 1 | Vectors & Vector Operations | Portfolio weights, factor exposures, return series |
| 2 | Dot Product & Geometry | Measuring alignment — tracking error, similarity between strategies |
| 3 | Matrices & Matrix Operations | Returns tables, factor-loading matrices, risk models |
| 4 | Linear Transformations | How data transforms — scenario analysis, stress testing |
| 5 | Systems of Linear Equations | Solving for equilibrium prices, arbitrage conditions |
| 6 | Matrix Inverse & Solving | Portfolio optimisation, regression, Kalman filters |
| 7 | Rank, Independence & Basis | Detecting redundant factors, choosing a minimal factor set |
| 8 | Eigenvalues & Eigenvectors | Risk decomposition, PCA, dynamic factor models |
| 9 | Covariance Matrices | The risk model — the single most important matrix in finance |
| 10 | PCA | Dimensionality reduction, noise filtering, signal extraction |

**Week 2 project (Saturday):** Build a Markowitz Portfolio Optimiser from scratch — weights vector, returns vector, covariance matrix, efficient frontier. This is the thing that cements everything from Days 1–10 into one working system.

**The mentor note for Phase 1:** Most beginners skip linear algebra because it feels abstract. This is the single most expensive mistake you can make. Covariance matrices, PCA, and regression — three things you will use every single week as a working quant — are all just linear algebra. Do not rush this phase.

---

### Phase 2 — The Tools of Change (Week 3, Days 11–16)
*Calculus & Optimisation. How things move and how you find the best.*

Every model in quant finance either measures how something changes (derivatives, sensitivity, Greeks) or tries to find the best possible value of something (portfolio optimisation, model calibration, maximum likelihood). That is calculus. You do not need to be able to prove the fundamental theorem — you need to be able to read a partial derivative and understand what an optimiser is doing.

| Day | Concept | What it actually does in the real world |
|---|---|---|
| 11 | Functions, Limits & Derivatives | Price sensitivity, delta — how a position moves with the market |
| 12 | Partial Derivatives | Sensitivity to each variable independently — the Greeks |
| 13 | Gradients & Directional Derivatives | Which direction makes a portfolio better — gradient descent in model fitting |
| 14 | Optimisation (Constrained & Unconstrained) | Markowitz, Kelly criterion, model calibration |
| 15 | Taylor Approximation | Why option pricing works — approximating complex payoffs with polynomials |
| 16 | Multivariable Calculus | Multi-asset models, joint risk |

**Week 3 project (Saturday):** A Calculus Toolkit — gradient descent portfolio optimiser, sensitivity analysis on a simple payoff, Taylor approximation of a price curve.

---

### Phase 3 — The Language of Uncertainty (Weeks 4–5, Days 17–26)
*Probability & Statistics. The discipline quants use to separate signal from noise.*

This is the phase most beginners underweight and most professionals say they wish they had learned more deeply. The reason is that everything in finance is uncertain — prices are random, correlations are unstable, models are wrong. Probability is not a tool you apply occasionally. It is the lens through which every quant reads data.

The interview insight: quant interviews at prop trading firms (Jane Street, Citadel, IMC) are almost entirely probability problems — not finance questions. Get very good at this phase.

| Day | Concept | What it actually does in the real world |
|---|---|---|
| 17 | Probability Fundamentals | Setting up any problem — sample spaces, events, axioms |
| 18 | Random Variables | Prices, returns, payoffs as mathematical objects |
| 19 | Expected Value | The core of every pricing model — what is this worth on average? |
| 20 | Variance & Standard Deviation | The core of every risk model — how much can this move? |
| 21 | Covariance & Correlation | How assets move together — the input to every portfolio model |
| 22 | Probability Distributions | The shape of randomness — which model fits this data? |
| 23 | Normal Distribution | The assumption behind most models (and why it is wrong) |
| 24 | Conditional Probability & Bayes' Theorem | Updating beliefs with new data — regime detection, signal updating |
| 25 | Maximum Likelihood Estimation | Fitting a model to data — how do you know which parameters are right? |
| 26 | Hypothesis Testing | Is this strategy actually profitable or just lucky? |

**Week 5 project (Saturday):** A Stats Toolkit — distribution fitter, hypothesis tester for a trading strategy's returns, Bayesian signal updater.

**The mentor note for Phase 3:** The normal distribution assumption (Day 23) is one of the most important things you will ever learn — not because it is right, but because most models assume it, and knowing *why it is wrong* (fat tails, skewness, volatility clustering) is what separates an experienced quant from a textbook reader. Study this day twice.

---

### Phase 4 — Building the Models (Weeks 6–7, Days 27–35)
*Quant Finance. Applying everything to actual financial problems.*

This is where the mathematics stops being abstract and starts producing numbers that mean something. Every model here is built on one or more concepts from the first three phases — if you have built the foundation properly, these will feel like natural extensions rather than new subjects.

| Day | Concept | Built on |
|---|---|---|
| 27 | Portfolio Mathematics | Vectors + Expected Value |
| 28 | Mean-Variance Optimisation | Matrices + Calculus + Covariance |
| 29 | CAPM | Expected Value + Regression + Correlation |
| 30 | Efficient Frontier | Optimisation + Covariance Matrices |
| 31 | Factor Models | PCA + Regression + Covariance |
| 32 | Time Series Analysis | Probability + Hypothesis Testing + Statistics |
| 33 | Monte Carlo Simulation | Random Variables + Distributions + Sampling |
| 34 | Options Mathematics | Expected Value + Probability + Payoff functions |
| 35 | Black-Scholes Model | Calculus + Normal Distribution + Stochastic processes |

**Week 7 project (Saturday):** An Options Pricing Engine — Black-Scholes with live price feeds, Monte Carlo pricer for comparison, Greeks dashboard.

---

### Phase 5 — Risk, Complexity & Real Systems (Week 8, Days 36–40)
*The bridge from theory to practice.*

| Day | Concept | Why it matters |
|---|---|---|
| 36 | Greeks | The practitioner's sensitivity toolkit — delta hedging, gamma risk |
| 37 | VaR / Expected Shortfall | The regulatory and operational risk measure at every firm |
| 38 | Stochastic Processes | The mathematical model of how prices actually move |
| 39 | Brownian Motion | The foundation of derivatives pricing |
| 40 | Quant Interview Projects | Synthesis — turn your 40 days into an interview-ready portfolio |

**Week 8 / capstone project:** The Full Quant Research Dashboard — composing every tool built over 8 weeks into one multi-tab Streamlit application with live data, backtesting, risk analytics, and a factor model. This is your LinkedIn flagship.

---

## Phase 6 — After the 40 Days (the map, not the journey)

The 40-day curriculum builds the foundation. Here is what comes after it, so you are not surprised:

**Alpha Research** — learning to generate and test trading signals. Books: *Advances in Financial Machine Learning* (Marcos López de Prado), *Algorithmic Trading* (Ernest Chan). Skills: time series modelling, feature engineering, backtesting without overfitting.

**Portfolio Construction at Scale** — turning signals into an actual portfolio. Requires covariance estimation, transaction cost modelling, execution algorithms.

**Live Trading** — connecting to a broker or exchange, paper trading, risk limits, real-time monitoring. This is where the engineering matters as much as the research.

---

## The resource stack — one source per layer, no more

The internet will offer you hundreds of courses. Here is the mentor's honest selection: one source per layer that is actually worth your time.

### Mathematics
**Gilbert Strang, *Introduction to Linear Algebra* (6th ed.)** — the standard. Pair with his free MIT OCW 18.06 lectures. This is the only linear algebra book you need for this phase. You already have it.

**3Blue1Brown, *Essence of Linear Algebra* (YouTube)** — watch before reading Strang for each chapter. Makes the geometry click before the algebra.

### Probability & Statistics
**Sheldon Ross, *A First Course in Probability*** — rigorous, clear, comprehensive. The standard probability text for quantitative finance students.

**All of Statistics by Larry Wasserman** — broader than Ross, covers the statistical side. Freely available as a PDF from Carnegie Mellon.

### Quant Finance Entry
**Ernest Chan, *Quantitative Trading* (2nd ed.)** — the most honest beginner book about what actually running a quant strategy looks like, including the unglamorous parts (data cleaning, transaction costs, overfitting).

**Emanuel Derman, *My Life as a Quant*** — read this alongside the technical work. Derman went from physics PhD to Goldman Sachs and invented the local volatility model. It tells you what the field actually feels like from the inside.

### The practitioner's advanced shelf (after Day 40)
- **Marcos López de Prado, *Advances in Financial Machine Learning*** — the most important modern quant research book. Read after the 40 days.
- **Paul Wilmott, *Paul Wilmott Introduces Quantitative Finance*** — the standard derivatives and stochastic calculus reference.
- **Gregory Zuckerman, *The Man Who Solved the Market*** — Jim Simons's story. Read when you need motivation, not technical knowledge.

### Free, online, no cost
- **MIT OCW 18.06** (Strang) — https://ocw.mit.edu/courses/18-06-linear-algebra-spring-2010/
- **MIT OCW 18.650** (Statistics for Applications) — rigorous, free
- **QuantLib** — open-source quant finance library, the closest thing to production-grade code you can study for free

---

## The daily learning format you should follow

One thing the original roadmap did not make explicit: how to structure each day's two hours of learning, independent of what the app and reel produce.

**Morning (before the app build, 20 minutes):** Read the concept in Strang or Ross first. Just the explanation — do not do the exercises yet. The goal is to hear the idea in the author's voice before you build it.

**Core session (60–75 minutes):** Build the OOP class, the Streamlit page, and run the computation on real data. This is where the concept moves from something you read to something you can produce on demand.

**Evening reflection (10 minutes, written in a notebook or private doc):** Answer three questions:
1. What did this concept replace? (How did I think about this problem before today?)
2. Where does this connect forward? (Which Day N later will depend on this?)
3. What is the one number or formula I would write on a whiteboard to explain this to someone tomorrow?

The third question is your reel script. The answer to that question is what your hook should be.

---

## The mentor's honest assessment of where beginners go wrong

Based on what industry research and practitioners say consistently:

**Mistake 1: Starting with trading before earning it.** Hundreds of beginners skip the math and jump to backtesting a moving average crossover strategy on Yahoo Finance. This produces overfit, transaction-cost-blind, survivorship-biased results that feel like alpha and are not. The 40-day curriculum is designed specifically to prevent this.

**Mistake 2: Confusing familiarity with understanding.** You can follow along with a linear algebra video and feel like you understand it, then be unable to explain why PCA works two weeks later. The "one number on a whiteboard" exercise above is specifically for this. If you cannot reconstruct the core idea without notes, you do not yet understand it.

**Mistake 3: Jumping between resources.** This is the specific thing you asked me to help with — you are overwhelmed by the internet. The resource stack above has one source per layer. Ignore everything outside it until after Day 40.

**Mistake 4: Building alone without showing anyone.** ThefacelessQuant is not just a marketing project — it is your accountability system. Publishing Day N means you have actually built Day N. The reel is proof of work.

**Mistake 5: Not understanding that probability and statistics, not linear algebra, is the hard part.** Most beginners assume matrices are the difficult bit. They are not — the abstraction is unfamiliar but the mechanics are finite. Probability, specifically the *reasoning* under uncertainty and the *testing* of hypotheses, is where real quant thinking lives. Spend extra time on Phase 3.

---

## The honest timeline

Forty days of content is not forty days of calendar time for a beginner. Here is what realistic pacing looks like if you are learning this from scratch:

- **Phase 1 (Linear Algebra):** 3–4 weeks at a pace that sticks, not the 2 weeks on paper
- **Phase 2 (Calculus):** 2 weeks if you have seen calculus before; 3–4 if not
- **Phase 3 (Probability & Statistics):** 4–6 weeks — do not rush this one
- **Phases 4–5 (Quant Finance):** 4–5 weeks
- **Total realistic timeline:** 4–5 months of serious daily work

That is fine. The goal is not to finish in 40 days. The goal is to finish with genuine, demonstrable understanding. A portfolio of 40 solid, well-built projects produced over 5 months is more valuable than a rushed 40 days of superficial work.

---

## What I will do with you, going forward

Every day you say "Day N", I will:

1. Deliver the full day's content (the OOP class, Streamlit page, reel, caption, reading list) using the skill spec established over the past three days.
2. Add a short **mentor note** for that day — one honest paragraph about how this concept is actually tested in interviews, where most people get it wrong, and what to look for in the reading beyond what the app shows.
3. When you reach the end of a phase, I will write a phase review — what you have now earned the ability to do, and what the next phase will build on top of it.

The one thing I will not do is pretend this is easy or fast. It is neither. But it is absolutely learnable, and what you are building in public — the daily proof of work — is one of the most credible signals you can give to anyone who looks at your profile later on.

This is the right path. Keep going.
