import streamlit as st

# Page Config must be the first Streamlit command
st.set_page_config(
    page_title="Quant Lab",
    page_icon="📈",
    layout="wide"
)

# --- BRANDING & IDENTITY SNIPPET ---
with st.sidebar:
    st.markdown("### 👨‍💻 Built by [Your First Name]")
    st.markdown(
        "Bridging the gap between code and markets. \n\n"
        "Catch my latest Python & Quant Finance tutorials below:"
    )
    
    # Using the new professional handle strategy 
    st.link_button("📱 Follow The Quant Mentor", "https://instagram.com/your-handle")
    st.link_button("🤝 Connect on LinkedIn", "https://linkedin.com/in/your-profile-url")
    st.divider()
# -----------------------------------

st.title("📈 The Quant Lab")
st.markdown("### 🚀 Your launchpad into Quant Finance.")

st.markdown("""
Demystifying quantitative finance, algorithmic trading, and market mechanics. 
I build interactive Python & Streamlit apps to help aspiring quants master the math and pass their interviews.

**👈 Use the sidebar to explore the daily quant simulators and build a hireable portfolio with me!**

---
### 🛣️ The Roadmap:
* **Phase 1: Foundations & Market Mechanics** (Order books, descriptive statistics, and probability)
* **Phase 2: Strategy & Risk Management** (Time series analysis, core strategies, and performance metrics)
* **Phase 3: Alpha Generation & Optimization** (Portfolio optimization, statistical arbitrage, and machine learning)
""")