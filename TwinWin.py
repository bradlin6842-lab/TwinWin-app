import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# --- 頁面設定 ---
st.set_page_config(page_title="TwinWin Wealth Terminal", layout="wide")
plt.style.use('dark_background') 

# --- 側邊欄參數 ---
with st.sidebar:
    st.header("⚙️ Product Terms")
    eki_barrier = st.slider("EKI Barrier (%)", 40, 90, 60) / 100
    strike_price = st.slider("Strike Price (%)", 40.0, 100.0, 61.95) / 100
    st.markdown("---")
    st.caption("Standard basket: ASML, AMAT, LRCX, 8035 JT.")

# --- 主頁面 ---
# 1. 縮小標題字體，並調整間距
st.markdown("<h3 style='margin-bottom: 0px; font-weight: 500; color: #EEEEEE;'>TwinWin Investment Simulation</h3>", unsafe_allow_html=True)

# 2. Live Scenario 滑桿 (主要互動區)
market_perf = st.select_slider(
    "🎮 **Live Market Simulation (%)**",
    options=list(range(20, 151)),
    value=84
)
market_change = market_perf / 100

# --- 💡 核心計算與繪圖 (大大大圖表) ---
perf_range = np.linspace(0, 1.5, 500)
payoff_curve = [
    (p / strike_price * 100) if p < eki_barrier else (100 + abs(p - 1.0) * 100) 
    for p in perf_range
]
current_payoff = (market_change / strike_price * 100) if market_change < eki_barrier else (100 + abs(market_change - 1.0) * 100)

# 繪圖設定 (16, 10 大圖)
fig, ax = plt.subplots(figsize=(16, 10)) 
ax.plot(perf_range * 100, payoff_curve, color='#00ffcc', linewidth=5, alpha=0.9)
ax.axhline(y=100, color='white', linestyle=':', alpha=0.4)
ax.axvline(x=100, color='white', linestyle='--', alpha=0.2)
ax.axvspan(0, eki_barrier*100, color='#ff4444', alpha=0.12) 
ax.scatter([market_perf], [current_payoff], color='yellow', s=400, zorder=10, edgecolor='white', linewidth=2)

ax.set_title("Payoff Trajectory Analysis", fontsize=16, color='gray', pad=20)
ax.grid(True, alpha=0.05)
st.pyplot(fig, use_container_width=True)

st.markdown("---")

# --- 3. 專業簡約數據列 ---
st.markdown("""
    <style>
    .data-row {
        display: flex;
        justify-content: space-around;
        align-items: center;
        padding: 30px 0;
        border-top: 1px solid #EEEEEE;
        border-bottom: 1px solid #EEEEEE;
    }
    .data-item {
        text-align: center;
        flex: 1;
    }
    .data-label {
        color: #888888;
        font-size: 14px;
        text-transform: uppercase;
        letter-spacing: 2px;
        margin-bottom: 10px;
    }
    .data-value {
        color: #222222;
        font-size: 32px; /* 專業適中大小 */
        font-weight: 700;
    }
    .data-sub {
        font-size: 14px;
        margin-top: 6px;
    }
    </style>
    """, unsafe_allow_html=True)

delta_val = market_perf - 100
d_color = "#d9534f" if delta_val < 0 else "#5cb85c"
payoff_delta = current_payoff - 100
p_color = "#d9534f" if payoff_delta < 0 else "#5cb85c"
status = "ACTIVE" if market_change >= eki_barrier else "KI TRIGGERED"
s_color = "#5cb85c" if market_change >= eki_barrier else "#d9534f"

st.markdown(f"""
    <div class="data-row">
        <div class="data-item">
            <div class="data-label">Underlying Price</div>
            <div class="data-value">{market_perf}%</div>
            <div class="data-sub" style="color: {d_color};">
                {"▼" if delta_val < 0 else "▲"} {abs(delta_val)}% vs Spot
            </div>
        </div>
        <div class="data-item" style="border-left: 1px solid #F0F0F0; border-right: 1px solid #F0F0F0;">
            <div class="data-label">Final Payoff</div>
            <div class="data-value" style="color: #008080;">{current_payoff:.2f}</div>
            <div class="data-sub" style="color: {p_color};">
                RETURN: {payoff_delta:+.2f}%
            </div>
        </div>
        <div class="data-item">
            <div class="data-label">Status</div>
            <div class="data-value" style="color: {s_color};">{status}</div>
            <div class="data-sub" style="color: #999;">STRIKE: {strike_price*100:.1f}%</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# 底部提醒
if market_change < eki_barrier:
    st.error(f"🛡️ **Protective Shield:** You are buying at a **{(1-strike_price)*100:.1f}% discount** vs initial price.")
elif market_change < 1.0:
    st.success(f"💰 **TwinWin Advantage:** Capturing {abs(delta_val)}% profit from market downside.")

st.markdown("<p style='text-align: center; color: #CCC; font-size: 11px; margin-top: 40px;'>FOR PROFESSIONAL USE ONLY</p>", unsafe_allow_html=True)
