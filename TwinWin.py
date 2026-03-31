import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# --- 頁面設定 (極簡專業風) ---
st.set_page_config(page_title="TwinWin Wealth Terminal", layout="wide")
plt.style.use('dark_background') 

# --- 側邊欄參數 (產品固定條款) ---
with st.sidebar:
    st.header("⚙️ Product Terms")
    eki_barrier = st.slider("EKI Barrier (%)", 40, 90, 60) / 100
    strike_price = st.slider("Strike Price (%)", 40.0, 100.0, 61.95) / 100
    st.markdown("---")
    st.caption("Standard semi-conductor equipment basket.")

# --- 主頁面 ---
st.title("💹 TwinWin Investment Simulation")

# --- 1. Live Scenario 滑桿 (主要互動區) ---
market_perf = st.select_slider(
    "🎮 **Live Market Simulation (%)** - Adjust to see payoff movement",
    options=list(range(20, 151)),
    value=84
)
market_change = market_perf / 100

st.markdown("---")

# --- 💡 核心計算與繪圖 (大大大圖表) ---
perf_range = np.linspace(0, 1.5, 500)
payoff_curve = [
    (p / strike_price * 100) if p < eki_barrier else (100 + abs(p - 1.0) * 100) 
    for p in perf_range
]
current_payoff = (market_change / strike_price * 100) if market_change < eki_barrier else (100 + abs(market_change - 1.0) * 100)

# 繪圖設定
fig, ax = plt.subplots(figsize=(16, 9)) 
# 獲利曲線
ax.plot(perf_range * 100, payoff_curve, color='#00ffcc', linewidth=5, alpha=0.9, label='TwinWin Payoff')

# 繪製盈虧平衡線 (Break-even 100%)
ax.axhline(y=100, color='white', linestyle=':', alpha=0.4, label='Break-even')
ax.axvline(x=100, color='white', linestyle='--', alpha=0.2)

# 警戒區
ax.axvspan(0, eki_barrier*100, color='#ff4444', alpha=0.12) 

# 當前情境黃色大點
ax.scatter([market_perf], [current_payoff], color='yellow', s=400, zorder=10, edgecolor='white', linewidth=2)

# 圖表美化
ax.set_title("Expected Payoff Trajectory", fontsize=20, color='white', pad=25)
ax.set_xlabel("Underlying Performance (%)", fontsize=14, color='gray')
ax.set_ylabel("Payoff Value (%)", fontsize=14, color='gray')
ax.grid(True, alpha=0.05)
ax.legend(loc='upper left', frameon=False)

st.pyplot(fig, use_container_width=True)

st.markdown("---")

# --- 2. 專業簡約數據列 (CSS 優化版) ---
st.markdown("""
    <style>
    .data-row {
        display: flex;
        justify-content: space-around;
        align-items: center;
        padding: 30px 0;
        border-top: 1px solid #EEEEEE;
        border-bottom: 1px solid #EEEEEE;
        background-color: transparent;
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
        font-size: 36px;
        font-weight: 700;
        font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
    }
    .data-sub {
        font-size: 15px;
        margin-top: 6px;
        font-weight: 500;
    }
    </style>
    """, unsafe_allow_html=True)

# 數據顏色邏輯
delta_val = market_perf - 100
d_color = "#d9534f" if delta_val < 0 else "#5cb85c"
payoff_delta = current_payoff - 100
p_color = "#d9534f" if payoff_delta < 0 else "#5cb85c"
status = "ACTIVE" if market_change >= eki_barrier else "KI TRIGGERED"
s_color = "#5cb85c" if market_change >= eki_barrier else "#d9534f"

# 渲染數據列
st.markdown(f"""
    <div class="data-row">
        <div class="data-item">
            <div class="data-label">Underlying Price</div>
            <div class="data-value">{market_perf}%</div>
            <div class="data-sub" style="color: {d_color};">
                {"▼" if delta_val < 0 else "▲"} {abs(delta_val)}% from Spot
            </div>
        </div>
        <div class="data-item" style="border-left: 1px solid #F0F0F0; border-right: 1px solid #F0F0F0;">
            <div class="data-label">Final Payoff</div>
            <div class="data-value" style="color: #008080;">{current_payoff:.2f}</div>
            <div class="data-sub" style="color: {p_color};">
                TOTAL RETURN: {payoff_delta:+.2f}%
            </div>
        </div>
        <div class="data-item">
            <div class="data-label">Execution Status</div>
            <div class="data-value" style="color: {s_color};">{status}</div>
            <div class="data-sub" style="color: #999;">BARRIER: {eki_barrier*100:.0f}% | STRIKE: {strike_price*100:.1f}%</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# --- 3. 底部動態提醒 (加強說服力) ---
st.markdown("<br>", unsafe_allow_html=True)
if market_change < eki_barrier:
    discount = (1 - strike_price) * 100
    st.error(f"🛡️ **Protective Shield:** Even in KI event, you are buying the stock at a **{discount:.1f}% discount** compared to initial price.")
elif market_change < 1.0:
    st.success(f"💰 **TwinWin Advantage:** Market is down {abs(delta_val)}%, but you are gaining {payoff_delta:.2f}% profit!")
else:
    st.info("🚀 **Bullish Participation:** You are participating in the upside growth of the semiconductor sector.")

st.markdown("<p style='text-align: center; color: #CCC; font-size: 11px; margin-top: 50px;'>PRIVATE & CONFIDENTIAL | FOR ILLUSTRATION PURPOSES ONLY</p>", unsafe_allow_html=True)
