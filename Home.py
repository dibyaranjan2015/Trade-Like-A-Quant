import streamlit as st

# Page Config must be the first Streamlit command
st.set_page_config(
    page_title="The Faceless Quant",
    page_icon="📈",
    layout="wide"
)

# --- BRANDING & IDENTITY SNIPPET ---
with st.sidebar:
    st.markdown("### 👨‍💻 Built by The Faceless Quant")
    st.markdown(
        "Bridging the gap between code and markets. \n\n"
        "Catch my latest Python & Quant Finance tutorials below:"
    )
    
    # Using your actual Instagram handle
    st.link_button("📱 Follow @TheFacelessQuant", "https://instagram.com/thefacelessquant")
    st.link_button("🤝 Connect on LinkedIn", "https://www.linkedin.com/in/drs2015/")
    st.divider()
# -----------------------------------

st.title("📈 The Quant Lab")
st.markdown("### Your launchpad into Quant Finance.")

st.markdown("""
Demystifying quantitative finance, algorithmic trading, and market mechanics. 
I build interactive Python & Streamlit apps to help aspiring quants master the math and pass their interviews.

**👈 Use the sidebar to explore the daily quant simulators and build a hireable portfolio with me!**
""")

st.divider()

col1, col2 = st.columns(2)

with col1:
    st.markdown("### Current Sprint: Linear Algebra")
    st.markdown("""
    *Mastering the math behind multi-asset portfolios and algorithmic trading.*
    
    * **Day 1:** Vectors, Scalars & Capital Allocation ✅
    * **Day 2:** Matrix Addition & Portfolio Rebalancing *(Coming Soon)*
    * **Day 3:** The Dot Product & Total Returns *(Coming Soon)*
    * **Day 4:** Systems of Equations & Arbitrage *(Coming Soon)*
    """)
    
with col2:
    st.markdown("### The Master Roadmap")
    st.markdown("""
    * **Phase 1: Foundations & Math** (Linear algebra, statistics, and probability)
    * **Phase 2: Strategy & Risk Management** (Time series analysis and performance metrics)
    * **Phase 3: Alpha Generation** (Portfolio optimization and machine learning)
    """)