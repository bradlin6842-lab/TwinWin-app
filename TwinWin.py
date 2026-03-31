import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# --- 頁面設定 ---
st.set_page_config(page_title="TwinWin Payoff", layout="wide")
plt.style.use('dark_background')

# --- 自定義 CSS：讓 Metric 數字變大，間距加寬 ---
st.markdown("""
    <style>
    [data-testid="stMetricValue"] {
        font-size: 50px !important;
        font-weight: bold !important;
        color: #00ffcc !important;
    }
    [data-testid="stMetricLabel"] {
        font-size: 20px !important;
    }
    .stMetric {
        background-color: #1e1e1e;
        padding: 20px;
        border-radius: 10px;
        border: 1px solid #333;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 側邊欄參數 ---
with st.sidebar:
    st.header("⚙️ Product Setup")
    eki_barrier = st.slider("EKI Barrier (%)", 40, 90, 60) / 100
    strike_price = st.slider("Strike Price (%)", 40.0, 100.0, 61.95) / 100
    st.markdown("---")
    st.caption("Adjust static product terms here.")

# --- 主頁面 ---
st.title("💹 TwinWin Interactive Dashboard")
st.markdown("---")

# --- 💡 計算與繪圖 ---
perf_range = np.linspace(0, 1.5, 500)
payoff_curve = [
    (p / strike_price * 100) if p < eki_barrier else (100 + abs(p - 1.0) * 100) 
    for p in perf_range
]

# --- 1. 大圖顯示 ---
fig, ax = plt.subplots(figsize=(16, 7)) # 再加高一點
ax.plot(perf_range * 100, payoff_curve, color='#00ffcc', linewidth=5, alpha=0.9)
ax.axvspan(0, eki_barrier*100, color='red', alpha=0.15)
ax.axvline(x=100, color='white', linestyle='--', alpha=0.3)
ax.axhline(y=100, color='white', linestyle='--', alpha=0.3)

ax.set_title(f"TwinWin Payoff Curve (Strike: {strike_price*100:.2f}%)", fontsize=18, pad=20, color='white')
ax.set_xlabel("Underlying Performance (%)", color='gray', fontsize=14)
ax.set_ylabel("Payoff Value", color='gray', fontsize=14)
ax.grid(True, alpha=0.05)

# --- 2. Live Scenario 滑桿 ---
market_perf = st.select_slider(
    "🎮 **Live Market Simulation**: Drag to see how payoff changes with stock performance (%)",
    options=list(range(20, 151)),
    value=84
)
market_change = market_perf / 100

# 在圖上畫點
current_payoff = (market_change / strike_price * 100) if market_change < eki_barrier else (100 + abs(market_change - 1.0) * 100)
ax.scatter([market_perf], [current_payoff], color='yellow', s=300, zorder=15, edgecolor='black')
st.pyplot(fig, use_container_width=True)

st.markdown("---")

# --- 3. 數據看板 (CSS 加大版) ---
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Underlying Price", f"{market_perf}%", delta=f"{market_perf-100}%")

with col2:
    # 這裡就是你要的巨大數字
    st.metric("Final Payoff", f"{current_payoff:.2f}", delta=f"{current_payoff-100:.2f}%")

with col3:
    status_msg = "Safe Zone" if market_change >= eki_barrier else "KI Triggered"
    st.metric("Strategy Status", status_msg, delta=None)

st.markdown("---")
st.info(f"💡 Strategy Logic: At {market_perf}%, you are earning {abs(market_perf-100) if market_change >= eki_barrier else 'stock value'} payoff.")
