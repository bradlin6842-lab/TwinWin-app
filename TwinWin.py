import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# --- 頁面設定 ---
st.set_page_config(page_title="TwinWin Analysis", layout="wide")
plt.style.use('dark_background') # 圖表內仍維持深色以利對比

# --- 側邊欄參數 ---
with st.sidebar:
    st.header("⚙️ Product Terms")
    eki_barrier = st.slider("EKI Barrier (%)", 40, 90, 60) / 100
    strike_price = st.slider("Strike Price (%)", 40.0, 100.0, 61.95) / 100

# --- 主頁面 ---
st.title("💹 TwinWin Investment Simulation")

# --- 1. Live Scenario 滑桿 (放在最上方，操作動線流暢) ---
market_perf = st.select_slider(
    "🎮 **Live Market Simulation (%)**",
    options=list(range(20, 151)),
    value=84
)
market_change = market_perf / 100

st.markdown("---")

# --- 💡 核心繪圖區 (大大大版本) ---
perf_range = np.linspace(0, 1.5, 500)
payoff_curve = [
    (p / strike_price * 100) if p < eki_barrier else (100 + abs(p - 1.0) * 100) 
    for p in perf_range
]
current_payoff = (market_change / strike_price * 100) if market_change < eki_barrier else (100 + abs(market_change - 1.0) * 100)

fig, ax = plt.subplots(figsize=(16, 10)) 
ax.plot(perf_range * 100, payoff_curve, color='#00ffcc', linewidth=5, alpha=0.9)
ax.axvspan(0, eki_barrier*100, color='#ff4444', alpha=0.1) 
ax.axvline(x=100, color='white', linestyle='--', alpha=0.2)
ax.scatter([market_perf], [current_payoff], color='yellow', s=350, zorder=10, edgecolor='white')

ax.set_title("Payoff Trajectory Analysis", fontsize=18, color='white', pad=20)
ax.grid(True, alpha=0.05)
st.pyplot(fig, use_container_width=True)

st.markdown("---")

# --- 2. 專業簡約數據列 (移除黑底，縮小字體，增加專業感) ---
# 使用 CSS 打造細線格線與精緻文字
st.markdown("""
    <style>
    .data-row {
        display: flex;
        justify-content: space-around;
        align-items: center;
        padding: 20px 0;
        border-top: 1px solid #EEEEEE;
        border-bottom: 1px solid #EEEEEE;
        margin-top: 20px;
    }
    .data-item {
        text-align: center;
        flex: 1;
    }
    .data-label {
        color: #666;
        font-size: 14px;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        margin-bottom: 8px;
    }
    .data-value {
        color: #31333F; /* 深色文字，白底背景 */
        font-size: 32px; /* 縮小到適中專業大小 */
        font-weight: 700;
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
    }
    .data-sub {
        font-size: 14px;
        margin-top: 4px;
    }
    </style>
    """, unsafe_allow_html=True)

# 準備數據顯示顏色
delta_val = market_perf - 100
d_color = "#d9534f" if delta_val < 0 else "#5cb85c"
payoff_delta = current_payoff - 100
p_color = "#d9534f" if payoff_delta < 0 else "#5cb85c"
status = "ACTIVE" if market_change >= eki_barrier else "TRIGGERED"
s_color = "#5cb85c" if market_change >= eki_barrier else "#d9534f"

# 渲染數據列 (呈現為白底背景下的簡潔列)
st.markdown(f"""
    <div class="data-row">
        <div class="data-item">
            <div class="data-label">Underlying Price</div>
            <div class="data-value" style="color: #31333F;">{market_perf}%</div>
            <div class="data-sub" style="color: {d_color};">
                {"▼" if delta_val < 0 else "▲"} {abs(delta_val)}% vs Initial
            </div>
        </div>
        <div class="data-item" style="border-left: 1px solid #EEE; border-right: 1px solid #EEE;">
            <div class="data-label">Final Payoff</div>
            <div class="data-value" style="color: #008080;">{current_payoff:.2f}</div>
            <div class="data-sub" style="color: {p_color};">
                EXPECTED RETURN: {payoff_delta:+.2f}%
            </div>
        </div>
        <div class="data-item">
            <div class="data-label">Execution Status</div>
            <div class="data-value" style="color: {s_color}; font-size: 24px;">{status}</div>
            <div class="data-sub" style="color: #999;">BARRIER AT {eki_barrier*100:.0f}%</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br><p style='text-align: center; color: #BBB; font-size: 12px;'>FOR PROFESSIONAL INVESTOR USE ONLY</p>", unsafe_allow_html=True)
