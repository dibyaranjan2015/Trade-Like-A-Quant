import streamlit as st
import numpy as np
import plotly.graph_objects as go
import yfinance as yf

# Page Configuration
st.set_page_config(page_title="Day 1: Vectors & Scalars", page_icon="📐", layout="wide")

with st.sidebar:
    st.markdown("### Built by The Faceless Quant")
    st.markdown(
        "Bridging the gap between code and markets. \n\n"
        "Catch my latest Python & Quant Finance tutorials below:"
    )
    
    # Using your actual Instagram handle
    st.link_button("📱 Follow @TheFacelessQuant", "https://instagram.com/thefacelessquant")
    st.link_button("🤝 Connect on LinkedIn", "https://www.linkedin.com/in/drs2015/")
    st.divider()
# -----------------------------------
    st.markdown("**Sprint:** Linear Algebra (Day 1 / 14)")
# -----------------------------------

st.title("Day 1: Vectors, Scalars & Capital Allocation")
st.markdown("### *Linear Algebra Foundation for Quantitative Trading*")

# ==========================================
# SECTION 1: THE CONCEPT (EDUCATIONAL CORE)
# ==========================================
st.markdown("---")
st.subheader("1. Theoretical Foundation")

col_theory1, col_theory2 = st.columns(2)

with col_theory1:
    st.markdown("""
    #### What is a Scalar?
    A **scalar** is a single numerical value (magnitude only). In trading, scalars represent:
    * Total portfolio capital multiplier or leverage ($C$)
    * Risk-free rate ($r_f$)
    * Uniform stop-loss percentage
    """)

with col_theory2:
    st.markdown("""
    #### What is a Vector?
    A **vector** is an ordered list of values representing a point or direction in multi-dimensional space:
    * 3 assets = **3D Vector Space** ($\mathbb{R}^3$)
    * 50 assets (Nifty 50) = **50D Vector Space** ($\mathbb{R}^{50}$)
    * Each dimension corresponds to an individual asset's return.
    """)

with st.expander(" Why don't Quants use simple loops?"):
    st.write("""
    Amateur coders loop through stocks one by one (`for stock in portfolio:`). 
    Quants treat the entire market as a single vector $\mathbf{v} \in \mathbb{R}^n$. 
    Operating on entire vectors via linear algebra (vectorization in NumPy) leverages SIMD 
    (Single Instruction, Multiple Data) processor instructions, speeding up execution by 100x to 1000x.
    """)

# ==========================================
# SECTION 2: LIVE MARKET DATA & INTERACTIVE MATH
# ==========================================
st.markdown("---")
st.subheader("2. Live NSE Data & Mathematical Scaling")

col_t1, col_t2, col_t3 = st.columns(3)
t1 = col_t1.text_input("Asset 1 (X-Axis)", value="RELIANCE.NS")
t2 = col_t2.text_input("Asset 2 (Y-Axis)", value="TCS.NS")
t3 = col_t3.text_input("Asset 3 (Z-Axis)", value="HDFCBANK.NS")

if 'data_fetched' not in st.session_state:
    st.session_state['data_fetched'] = False

if st.button("Fetch Live Asset Returns"):
    with st.spinner("Pulling real-time market close data from Yahoo Finance..."):
        # Fetching 5 days to ensure we grab the last valid close
        df = yf.download([t1, t2, t3], period="5d", progress=False)['Close']
        pct_returns = df.pct_change().dropna().iloc[-1] * 100
        
        st.session_state['returns'] = np.array([pct_returns[t1], pct_returns[t2], pct_returns[t3]])
        st.session_state['tickers'] = [t1, t2, t3]
        st.session_state['data_fetched'] = True

if st.session_state['data_fetched']:
    r_vec = st.session_state['returns']
    tickers = st.session_state['tickers']
    
    st.markdown("#### Apply Scalar Multiplication ($C \cdot \mathbf{v}$)")
    scalar_c = st.slider("Capital Multiplier (Scalar 'C')", min_value=1.0, max_value=10.0, value=2.0, step=0.5)
    
    scaled_vec = scalar_c * r_vec
    
    # Dynamic LaTeX Math Display
    st.markdown("**The Mathematical Operation:**")
    st.latex(rf"""
    C \cdot \mathbf{{v}} = {scalar_c:.1f} \times \begin{{bmatrix}} {r_vec[0]:.2f}\% \\ {r_vec[1]:.2f}\% \\ {r_vec[2]:.2f}\% \end{{bmatrix}} 
    = \begin{{bmatrix}} {scaled_vec[0]:.2f}\% \\ {scaled_vec[1]:.2f}\% \\ {scaled_vec[2]:.2f}\% \end{{bmatrix}}
    """)

    # ==========================================
    # SECTION 3: 3D VECTOR VISUALIZATION
    # ==========================================
    st.markdown("---")
    st.subheader("3. 3D Vector Space Visualization")
    
    fig = go.Figure()
    
    # Base return vector (Ghosted white)
    fig.add_trace(go.Scatter3d(
        x=[0, r_vec[0]], y=[0, r_vec[1]], z=[0, r_vec[2]],
        mode='lines+markers+text',
        line=dict(color='rgba(255, 255, 255, 0.4)', width=5),
        marker=dict(size=4, color='white'),
        text=["", f"1x Base: [{r_vec[0]:.1f}%, {r_vec[1]:.1f}%, {r_vec[2]:.1f}%]"],
        textposition="top center",
        name="Base Return Vector (1x)"
    ))
    
    # Scaled return vector (Neon Green)
    fig.add_trace(go.Scatter3d(
        x=[0, scaled_vec[0]], y=[0, scaled_vec[1]], z=[0, scaled_vec[2]],
        mode='lines+markers+text',
        line=dict(color='#00ff00', width=8),
        marker=dict(size=6, color='#00ff00'),
        text=["", f"{scalar_c}x Scaled"],
        textposition="top center",
        name=f"Scaled Vector ({scalar_c}x)"
    ))
    
    max_range = np.max(np.abs(r_vec)) * 11
    axis_lim = [-max_range, max_range]
    
    fig.update_layout(
        scene=dict(
            xaxis_title=f'{tickers[0]} Return (%)',
            yaxis_title=f'{tickers[1]} Return (%)',
            zaxis_title=f'{tickers[2]} Return (%)',
            xaxis=dict(range=axis_lim, backgroundcolor="#0e1117", gridcolor="#333333"),
            yaxis=dict(range=axis_lim, backgroundcolor="#0e1117", gridcolor="#333333"),
            zaxis=dict(range=axis_lim, backgroundcolor="#0e1117", gridcolor="#333333"),
        ),
        paper_bgcolor="#0e1117",
        plot_bgcolor="#0e1117",
        font=dict(color='white'),
        height=650,
        margin=dict(l=0, r=0, b=0, t=0)
    )
    
    st.plotly_chart(fig, use_container_width=True)

# ==========================================
# SECTION 4: INTERVIEW KNOWLEDGE CHECK
# ==========================================
st.markdown("---")
st.subheader("4. Quant Interview Concept Check")

quiz_option = st.radio(
    "**Question:** If vector $\mathbf{v}$ represents daily percentage returns of 3 stocks, what does multiplying by scalar $C = -1$ physically represent in quantitative finance?",
    options=[
        "A) Tripling the cash allocation across all stocks.",
        "B) Flipping the portfolio from 100% Long to 100% Short.",
        "C) Calculating portfolio variance.",
        "D) Setting all weights to zero."
    ],
    index=None
)

if st.button("Submit Answer"):
    if quiz_option and "B)" in quiz_option:
        st.success("✅ Correct! Multiplying an asset return vector by $-1$ flips the direction of every return dimension, mathematically representing an inverse/short position.")
    elif quiz_option:
        st.error("❌ Incorrect. Remember: scalar multiplication scales or inverts the magnitude and direction of all elements equally. Multiplying by $-1$ reverses signs, representing a short position.")
    else:
        st.warning("Please select an option first.")