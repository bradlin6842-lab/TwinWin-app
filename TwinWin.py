import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# --- 頁面設定 ---
st.set_page_config(page_title="TwinWin Professional", layout="wide")
plt.style.use('dark_background')

# --- 側邊欄參數 ---
with st.sidebar:
    st.header("⚙️ Settings")
    eki_barrier = st.slider("EKI Barrier (%)", 40, 90, 60) / 100
    strike_price = st.slider("Strike Price (%)", 40.0, 100.0, 61.95) / 100

# --- 主頁面 ---
st.title("💹 TwinWin Investment Simulation")

# --- 1. Live Scenario 滑桿 ---
market_perf = st.select_slider(
    "🎮 **Market Performance Simulation (%)**",
    options=list(range(20, 151)),
    value=84
)
market_change = market_perf / 100

st.markdown("---")

# --- 💡 計算與繪圖 ---
perf_range = np.linspace(0, 1.5, 500)
payoff_curve = [
    (p / strike_price * 100) if p < eki_barrier else (100 + abs(p - 1.0) * 100) 
    for p in perf_range
]
current_payoff = (market_change / strike_price * 100) if market_change < eki_barrier else (100 + abs(market_change - 1.0) * 100)

# 繪圖 (調整比例)
fig, ax = plt.subplots(figsize=(16, 6))
ax.plot(perf_range * 100, payoff_curve, color='#00ffcc', linewidth=4, alpha=0.9)
ax.axvspan(0, eki_barrier*100, color='#ff4444', alpha=0.15)
ax.axvline(x=100, color='white', linestyle='--', alpha=0.2)
ax.scatter([market_perf], [current_payoff], color='yellow', s=200, zorder=10)

ax.set_title("Expected Payoff Curve", fontsize=14, color='gray')
ax.grid(True, alpha=0.05)
st.pyplot(fig, use_container_width=True)

st.markdown("---")

# --- 2. 自定義專業級黑格看板 ---
# 這裡透過 CSS 控制：格子上下撐大 (padding)，文字大小適中
st.markdown("""
    <style>
    .metric-container {
        background-color: #161616;
        padding: 40px 20px; /* 上下 40px 拉大格子 */
        border-radius: 12px;
        border: 1px solid #333;
        text-align: center;
        margin: 10px;
    }
    .metric-label {
        color: #888;
        font-size: 16px;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 10px;
    }
    .metric-value {
        color: #00ffcc;
        font-size: 48px; /* 專業適中的大小 */
        font-weight: 600;
        font-family: 'Courier New', Courier, monospace;
    }
    .metric-delta {
        font-size: 18px;
        margin-top: 8px;
    }
    </style>
    """, unsafe_allow_html=True)

# 渲染數據格
c1, c2, c3 = st.columns(3)

with c1:
    delta_val = market_perf - 100
    color = "#ff4b4b" if delta_val < 0 else "#00f000"
    st.markdown(f"""
        <div class="metric-container">
            <div class="metric-label">Underlying Price</div>
            <div class="metric-value">{market_perf}%</div>
            <div class="metric-delta" style="color: {color};">
                {"↓" if delta_val < 0 else "↑"} {abs(delta_val)}% vs Initial
            </div>
        </div>
    """, unsafe_allow_html=True)

with c2:
    payoff_delta = current_payoff - 100
    p_color = "#ff4b4b" if payoff_delta < 0 else "#00f000"
    st.markdown(f"""
        <div class="metric-container">
            <div class="metric-label">Final Payoff</div>
            <div class="metric-value">{current_payoff:.2f}</div>
            <div class="metric-delta" style="color: {p_color};">
                {payoff_delta:+.2f}% Return
            </div>
        </div>
    """, unsafe_allow_html=True)

with c3:
    status = "TwinWin Active" if market_change >= eki_barrier else "KI Triggered"
    s_color = "#00ffcc" if market_change >= eki_barrier else "#ff4b4b"
    st.markdown(f"""
        <div class="metric-container">
            <div class="metric-label">Execution Status</div>
            <div class="metric-value" style="color: {s_color}; font-size: 32px;">{status}</div>
            <div class="metric-delta" style="color: gray;">Barrier at {eki_barrier*100:.0f}%</div>
        </div>
    """, unsafe_allow_html=True)

st.markdown("---")
st.caption("Internal Use Only - Private Wealth Management Terminal")
