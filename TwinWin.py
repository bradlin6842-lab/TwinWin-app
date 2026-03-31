import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# --- 頁面設定 ---
st.set_page_config(page_title="TwinWin Simulator", layout="wide")
plt.style.use('dark_background')

st.title("🚀 TwinWin Payoff Simulator")
st.write("Adjust scenarios to see the 'Double Win' logic.")

# --- 側邊欄參數 ---
with st.sidebar:
    st.header("Product Parameters")
    face_value = 100
    # 根據你的報價單設定
    eki_barrier = st.slider("EKI Barrier (%)", 40, 90, 60) / 100
    strike_price = st.slider("Strike Price (%)", 40.0, 100.0, 61.95) / 100
    
    st.markdown("---")
    st.header("🎮 Live Scenario")
    # 這裡就是你要的：調整標的漲跌情境
    market_change = st.slider("Market Performance (Relative to Initial %)", 20, 150, 85) / 100

# --- 計算當前情境獲利 ---
if market_change >= eki_barrier:
    current_payoff = face_value * (1 + abs(market_change - 1.0))
    status_text = "Safe Zone: TwinWin Active"
    status_color = "green"
else:
    current_payoff = (market_change / strike_price) * face_value
    status_text = "KI Event: Physical Delivery"
    status_color = "red"

# --- 核心繪圖邏輯 ---
perf_range = np.linspace(0, 1.5, 500)
payoff_curve = []

for p in perf_range:
    if p >= eki_barrier:
        payoff_curve.append(face_value * (1 + abs(p - 1.0)))
    else:
        payoff_curve.append((p / strike_price) * face_value)

fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(perf_range * 100, payoff_curve, color='#00ffcc', linewidth=2)
# 標記當前情境點
ax.scatter([market_change * 100], [current_payoff], color='yellow', s=100, zorder=5, label='Current Scenario')
ax.axvline(x=100, color='white', linestyle='--', alpha=0.3)
ax.axvline(x=eki_barrier*100, color='#ff4444', label='EKI Barrier')

# 使用英文標籤避免亂碼
ax.set_xlabel("Underlying Performance (%)")
ax.set_ylabel("Payoff Value")
ax.legend()
st.pyplot(fig)

# --- 儀表板顯示 ---
st.markdown(f"### Current Market Scenario: **{market_change*100:.1f}%**")
c1, c2 = st.columns(2)
with c1:
    st.metric("Final Payoff Value", f"{current_payoff:.2f}")
with c2:
    if market_change < 1.0 and market_change >= eki_barrier:
        st.success(f"Profit from Drop: +{abs(1.0 - market_change)*100:.1f}%")
    elif market_change >= 1.0:
        st.success(f"Profit from Rise: +{(market_change - 1.0)*100:.1f}%")
    else:
        st.error("Loss due to KI Event")

st.info(f"Status: {status_text}")
