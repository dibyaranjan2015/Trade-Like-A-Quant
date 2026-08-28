FULL_CURRICULUM = [
    {"day": 1, "name": "Vectors & Vector Operations", "pillar": "Linear Algebra", "week": 1},
    {"day": 2, "name": "Dot Product & Geometry", "pillar": "Linear Algebra", "week": 1},
    {"day": 3, "name": "Matrices & Matrix Operations", "pillar": "Linear Algebra", "week": 1},
    {"day": 4, "name": "Linear Transformations", "pillar": "Linear Algebra", "week": 1},
    {"day": 5, "name": "Systems of Linear Equations", "pillar": "Linear Algebra", "week": 1},
    {"day": 6, "name": "Matrix Inverse & Solving Systems", "pillar": "Linear Algebra", "week": 2},
    {"day": 7, "name": "Rank, Linear Independence & Basis", "pillar": "Linear Algebra", "week": 2},
    {"day": 8, "name": "Eigenvalues & Eigenvectors", "pillar": "Linear Algebra", "week": 2},
    {"day": 9, "name": "Covariance Matrices", "pillar": "Linear Algebra", "week": 2},
    {"day": 10, "name": "PCA \u2013 Principal Component Analysis", "pillar": "Linear Algebra", "week": 2},

    {"day": 11, "name": "Functions, Limits & Derivatives", "pillar": "Calculus", "week": 3},
    {"day": 12, "name": "Partial Derivatives", "pillar": "Calculus", "week": 3},
    {"day": 13, "name": "Gradients & Directional Derivatives", "pillar": "Calculus", "week": 3},
    {"day": 14, "name": "Optimization (Unconstrained & Constrained)", "pillar": "Calculus", "week": 3},
    {"day": 15, "name": "Taylor Approximation", "pillar": "Calculus", "week": 3},
    {"day": 16, "name": "Multivariable Calculus", "pillar": "Calculus", "week": 4},

    {"day": 17, "name": "Probability Fundamentals", "pillar": "Probability & Stats", "week": 4},
    {"day": 18, "name": "Random Variables", "pillar": "Probability & Stats", "week": 4},
    {"day": 19, "name": "Expected Value", "pillar": "Probability & Stats", "week": 4},
    {"day": 20, "name": "Variance & Standard Deviation", "pillar": "Probability & Stats", "week": 4},
    {"day": 21, "name": "Covariance & Correlation", "pillar": "Probability & Stats", "week": 5},
    {"day": 22, "name": "Probability Distributions", "pillar": "Probability & Stats", "week": 5},
    {"day": 23, "name": "Normal Distribution", "pillar": "Probability & Stats", "week": 5},
    {"day": 24, "name": "Conditional Probability & Bayes' Theorem", "pillar": "Probability & Stats", "week": 5},
    {"day": 25, "name": "Maximum Likelihood Estimation", "pillar": "Probability & Stats", "week": 5},
    {"day": 26, "name": "Hypothesis Testing", "pillar": "Probability & Stats", "week": 6},

    {"day": 27, "name": "Portfolio Mathematics", "pillar": "Quant Finance", "week": 6},
    {"day": 28, "name": "Mean-Variance Optimization", "pillar": "Quant Finance", "week": 6},
    {"day": 29, "name": "CAPM", "pillar": "Quant Finance", "week": 6},
    {"day": 30, "name": "Efficient Frontier", "pillar": "Quant Finance", "week": 6},
    {"day": 31, "name": "Factor Models", "pillar": "Quant Finance", "week": 7},
    {"day": 32, "name": "Time Series Analysis", "pillar": "Quant Finance", "week": 7},
    {"day": 33, "name": "Monte Carlo Simulation", "pillar": "Quant Finance", "week": 7},
    {"day": 34, "name": "Options Mathematics", "pillar": "Quant Finance", "week": 7},
    {"day": 35, "name": "Black-Scholes Model", "pillar": "Quant Finance", "week": 7},
    {"day": 36, "name": "Greeks", "pillar": "Quant Finance", "week": 8},
    {"day": 37, "name": "VaR / Expected Shortfall", "pillar": "Quant Finance", "week": 8},
    {"day": 38, "name": "Stochastic Processes", "pillar": "Quant Finance", "week": 8},
    {"day": 39, "name": "Brownian Motion", "pillar": "Quant Finance", "week": 8},
    {"day": 40, "name": "Quant Interview Projects", "pillar": "Quant Finance", "week": 8},
]


WEEKLY_PROJECTS = {
    1: "Linear AlgebraToolkit",
    2: "Portfolio Optimizer (Markowitz)",
    3: "CalculusToolkit",
    4: "Risk Model Engine",
    5: "StatsToolkit",
    6: "Portfolio Optimizer (full MPT)",
    7: "Options Pricing Engine",
    8: "Capstone: Full Quant Research Dashboard",
}


def by_pillar():
    """Returns an ordered dict-like list of (pillar, [entries]) preserving
    curriculum order, for grouped rendering on Home.py."""
    order = []
    grouped = {}
    for entry in FULL_CURRICULUM:
        p = entry["pillar"]
        if p not in grouped:
            grouped[p] = []
            order.append(p)
        grouped[p].append(entry)
    return [(p, grouped[p]) for p in order]
