import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# --- 頁面設定 (使用 Light Mode 視覺感) ---
st.set_page_config(page_title="TwinWin Payoff", layout="wide")

# --- 側邊欄參數 ---
with st.sidebar:
    st.header("⚙️ Product Setup")
    eki_barrier = st.slider("EKI Barrier (%)", 40, 90, 60) / 100
    strike_price = st.slider("Strike Price (%)", 40.0, 100.0, 61.95) / 100
    st.markdown("---")
    st.caption("Adjust static product terms here.")

# --- 主頁面 ---
st.title("💹 TwinWin Interactive Dashboard")

# --- 1. Live Scenario 滑桿 (放在圖表上方，符合你操作邏輯) ---
market_perf = st.select_slider(
    "🎮 **Live Market Simulation**: Drag to see how payoff changes (%)",
    options=list(range(20, 151)),
    value=84
)
market_change = market_perf / 100

st.markdown("---")

# --- 💡 計算與繪圖 ---
# 曲線背景使用 dark_background 維持專業感，或是你可以註解掉改用白底
plt.style.use('dark_background') 

perf_range = np.linspace(0, 1.5, 500)
payoff_curve = [
    (p / strike_price * 100) if p < eki_barrier else (100 + abs(p - 1.0) * 100) 
    for p in perf_range
]

# 當前點計算
current_payoff = (market_change / strike_price * 100) if market_change < eki_barrier else (100 + abs(market_change - 1.0) * 100)

# 繪圖
fig, ax = plt.subplots(figsize=(16, 6))
ax.plot(perf_range * 100, payoff_curve, color='#00ffcc', linewidth=5, alpha=0.9)
ax.axvspan(0, eki_barrier*100, color='red', alpha=0.2) # 紅色警戒區
ax.axvline(x=100, color='white', linestyle='--', alpha=0.3)
ax.scatter([market_perf], [current_payoff], color='yellow', s=300, zorder=15, edgecolor='black')

ax.set_title(f"TwinWin Payoff Curve (Strike: {strike_price*100:.2f}%)", fontsize=16)
ax.grid(True, alpha=0.1)

st.pyplot(fig, use_container_width=True)

st.markdown("---")

# --- 2. 原始格式但「特大字體」的數據看板 ---
# 我們使用 HTML/Markdown 來達成比原本 Metric 更大的視覺效果

c1, c2 = st.columns(2)

with c1:
    st.markdown("### Underlying Price")
    st.markdown(f"<h1 style='font-size: 80px; color: #31333F;'>{market_perf}%</h1>", unsafe_allow_html=True)
    delta = market_perf - 100
    color = "red" if delta < 0 else "green"
    st.markdown(f"<p style='font-size: 25px; color: {color};'>{'↓' if delta < 0 else '↑'} {abs(delta)}% from Initial</p>", unsafe_allow_html=True)

with c2:
    st.markdown("### Final Payoff")
    # 這裡就是你要的巨大字體，顏色用醒目的青藍色
    st.markdown(f"<h1 style='font-size: 100px; color: #008080;'>{current_payoff:.2f}</h1>", unsafe_allow_html=True)
    payoff_delta = current_payoff - 100
    p_color = "red" if payoff_delta < 0 else "green"
    st.markdown(f"<p style='font-size: 25px; color: {p_color};'>Expected Return: {payoff_delta:+.2f}%</p>", unsafe_allow_html=True)

st.markdown("---")
if market_change < eki_barrier:
    st.error(f"⚠️ Warning: EKI Barrier Triggered! Physical delivery at strike {strike_price*100:.2f}%")
else:
    st.success("✅ Safe Zone: Enjoying Double Win (Bullish & Bearish) returns.")
