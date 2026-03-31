import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# --- 頁面設定 ---
st.set_page_config(page_title="TwinWin Dashboard", layout="wide")
plt.style.use('dark_background')

# --- 側邊欄：放置固定產品參數 ---
with st.sidebar:
    st.header("⚙️ Product Setup")
    eki_barrier = st.slider("EKI Barrier (%)", 40, 90, 60) / 100
    strike_price = st.slider("Strike Price (%)", 40.0, 100.0, 61.95) / 100
    st.markdown("---")
    st.caption("Adjust static product terms here.")

# --- 主頁面：動態情境測試 ---
st.title("💹 TwinWin Interactive Dashboard")

# 把 Live Scenario 放到主頁最上方
st.subheader("🎮 Live Market Scenario")
market_perf = st.select_slider(
    "Slide to simulate Stock Performance (Relative to Initial Price %)",
    options=list(range(20, 151)),
    value=85
)
market_change = market_perf / 100

st.markdown("---")

# --- 計算當前邏輯 ---
if market_change >= eki_barrier:
    # TwinWin 核心：abs(1-perf)
    profit_pct = abs(market_change - 1.0) * 100
    current_payoff = 100 + profit_pct
    status_msg = "✅ Safe Zone: TwinWin Active"
    status_type = "success"
else:
    # 觸發 KI
    current_payoff = (market_change / strike_price) * 100
    status_msg = "⚠️ KI Event: Forced Delivery"
    status_type = "error"

# --- 數據看板 ---
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Market Price", f"{market_perf}%", delta=f"{market_perf-100}%", delta_color="normal")
with col2:
    # 這裡顯示最終拿回多少錢
    st.metric("Final Payoff", f"{current_payoff:.2f}", delta=f"{current_payoff-100:.2f}%")
with col3:
    st.info(f"**Strategy Status**\n\n{status_msg}")

# --- 繪圖 ---
perf_range = np.linspace(0, 1.5, 500)
payoff_curve = [
    (p / strike_price * 100) if p < eki_barrier else (100 + abs(p - 1.0) * 100) 
    for p in perf_range
]

fig, ax = plt.subplots(figsize=(12, 5))
ax.plot(perf_range * 100, payoff_curve, color='#00ffcc', linewidth=3, alpha=0.8)

# 畫出當前情境點 (黃色大點)
ax.scatter([market_perf], [current_payoff], color='yellow', s=150, zorder=10, label='Current Spot')
# 畫出 EKI 警戒區域
ax.axvspan(0, eki_barrier*100, color='red', alpha=0.1, label='KI Danger Zone')
ax.axvline(x=100, color='white', linestyle='--', alpha=0.3)

ax.set_xlabel("Underlying Performance (%)", color='gray')
ax.set_ylabel("Payoff Value", color='gray')
ax.legend()
st.pyplot(fig)

st.markdown("""
### 💡 How to Read this Chart:
* **V-Shape Zone:** Between the Red Zone and 150%, you profit from **both** upside and downside.
* **Red Zone:** If the stock drops below the EKI Barrier, the 'Double Win' disappears, and you receive stocks at the Strike Price.
""")
