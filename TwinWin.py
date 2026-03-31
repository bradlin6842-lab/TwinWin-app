import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# --- 頁面設定 (使用 Wide Mode 讓圖表更明顯) ---
st.set_page_config(page_title="TwinWin Payoff", layout="wide")
plt.style.use('dark_background')

# --- 側邊欄：放置固定產品參數 (EKI & Strike) ---
with st.sidebar:
    st.header("⚙️ Product Setup")
    eki_barrier = st.slider("EKI Barrier (%)", 40, 90, 60) / 100
    strike_price = st.slider("Strike Price (%)", 40.0, 100.0, 61.95) / 100
    st.markdown("---")
    st.caption("Adjust static product terms here.")

# --- 主頁面 ---
st.title("💹 TwinWin Interactive Dashboard")
st.markdown("---")

# --- 💡 計算與繪圖 (在繪圖前先準備好曲線) ---
perf_range = np.linspace(0, 1.5, 500)
# 準備 TwinWin 獲利曲線 (考慮 KI 機制)
payoff_curve = [
    (p / strike_price * 100) if p < eki_barrier else (100 + abs(p - 1.0) * 100) 
    for p in perf_range
]

# --- 1. 大圖：把圖移到最上面，並設定寬度 (figsize=(16, 6)) ---
# 放大圖表，讓客戶更明顯看到 V 字型
fig, ax = plt.subplots(figsize=(16, 6))
# 畫出 TwinWin 獲利曲線 (亮青色)
ax.plot(perf_range * 100, payoff_curve, color='#00ffcc', linewidth=4, alpha=0.9, label='TwinWin Payoff')

# 畫出 EKI 警戒區域 (淡紅色底色)
ax.axvspan(0, eki_barrier*100, color='red', alpha=0.1, label='KI Danger Zone')
# 畫出 100% 參考線 (白色虛線)
ax.axvline(x=100, color='white', linestyle='--', alpha=0.3)
# 畫出 100% 價值線 (白色虛線)
ax.axhline(y=100, color='white', linestyle='--', alpha=0.3)

# 圖表美化
ax.set_title("TwinWin Payoff Curve (KI Barrier at 60%)", fontsize=16, pad=20)
ax.set_xlabel("Underlying Performance (%)", color='gray', fontsize=12)
ax.set_ylabel("Payoff Value", color='gray', fontsize=12)
ax.legend(loc='upper left', fontsize=10)
ax.grid(True, alpha=0.05)

# 在 Streamlit 顯示圖表 (use_container_width=True 讓圖表隨視窗放大)
st.pyplot(fig, use_container_width=True)

# --- 2. Live Scenario 滑桿：移到圖的正下方 ---
# 使用 select_slider 讓拉動更滑順
market_perf = st.select_slider(
    "🎮 **Live Market Simulation**: Drag to see how payoff changes with stock performance (%)",
    options=list(range(20, 151)),
    value=85
)
market_change = market_perf / 100

st.markdown("---")

# --- 計算當前情境數據 (用於 Metric 展示) ---
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

# --- 3. 數據看板：放在最下方 ---
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Underlying Price", f"{market_perf}%", delta=f"{market_perf-100}%")
with col2:
    # 這裡顯示最終拿回多少錢 (Final Payoff)
    st.metric("Final Payoff", f"{current_payoff:.2f}", delta=f"{current_payoff-100:.2f}%")
with col3:
    # 策略狀態
    st.info(f"**Strategy Status**\n\n{status_msg}")

# --- 更新：即時在圖表上顯示當前點 ---
# (為了即時更新，需重新繪製 scatter，但 Streamlit 的 Rerun 機制會處理)
# 在圖表上畫出黃色大點 (Current Scenario)
ax.scatter([market_perf], [current_payoff], color='yellow', s=200, zorder=15, edgecolor='black')
# 手動 rerun 圖表 (這是 Streamlit 畫散點圖跟滑桿結合的關鍵)
# st.pyplot(fig, use_container_width=True) # 這一行程式碼不需存在，streamlit 會自動 rerun。
