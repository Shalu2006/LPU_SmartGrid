import streamlit as st
import matplotlib.pyplot as plt

st.set_page_config(page_title="Analytics | LPU Smart Grid", layout="wide")
st.title("📊 Real-Time Grid Performance Analysis")

# This part is crucial - it checks if the main app has sent the data yet
if 'df' not in st.session_state:
    st.warning("⚠️ Please run the simulation on the main dashboard first!")
    st.stop()

df = st.session_state['df']

tab1, tab2 = st.tabs(["Energy Flow", "School Performance"])

with tab1:
    fig1, ax1 = plt.subplots(figsize=(10, 4))
    plt.style.use('dark_background')
    ax1.plot(df['Hour'], df['Solar'], color='orange', label='Solar (Supply)')
    ax1.plot(df['Hour'], df['Demand'], color='red', linestyle='--', label='Demand')
    ax1.fill_between(df['Hour'], df['Solar'], alpha=0.2, color='orange')
    ax1.legend()
    st.pyplot(fig1)

with tab2:
    fig2, ax2 = plt.subplots(figsize=(10, 4))
    ax2.bar(df['Hour'], df['Computing_Uptime'], color='cyan', alpha=0.7, label='Computing Labs')
    ax2.bar(df['Hour'], df['Electronics_Uptime'], color='magenta', alpha=0.4, label='Electronics Labs')
    ax2.set_ylabel("Uptime %")
    ax2.legend()
    st.pyplot(fig2)

st.divider()
st.download_button("📩 Download Grid Report (CSV)", df.to_csv(index=False), "grid_report.csv", "text/csv")
