import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# --- 頁面設定 ---
st.set_page_config(page_title="TwinWin Payoff Simulator", layout="wide")

# 套用深色風格
plt.style.use('dark_background')

st.title("💹 TwinWin (Bullish Bearish) 結構模擬器")
st.markdown("---")

# --- 側邊欄：讓你可以跟客戶互動調參數 ---
with st.sidebar:
    st.header("🛠️ 產品參數設定")
    
    face_value = 100
    
    # 根據報價單預設值
    coupon_rate = st.slider("年化配息率 (%)", 0.0, 20.0, 12.0) / 100
    eki_barrier = st.slider("EKI 下限觸發門檻 (%)", 40, 90, 60) / 100
    strike_price = st.slider("Strike 執行價 (%)", 40.0, 100.0, 61.95) / 100
    
    st.info("""
    **邏輯說明：**
    1. 未破 EKI：漲多少賺多少，跌多少也賺多少。
    2. 跌破 EKI：按執行價 (Strike) 換算股票價值。
    """)

# --- 核心計算邏輯 ---
# 模擬標的表現從 0% 到 150%
underlying_perf = np.linspace(0, 1.5, 500)
payoff = []

for perf in underlying_perf:
    # 情況 A：未觸發 EKI (表現 >= 60%)
    if perf >= eki_barrier:
        # 計算絕對值漲跌幅 (TwinWin 核心)
        # 100% + |100% - 當前表現|
        gain = abs(perf - 1.0)
        payoff.append(face_value * (1 + gain))
    
    # 情況 B：觸發 EKI (表現 < 60%)
    else:
        # 實物結算：(當前表現 / 執行價) * 面額
        # 這代表如果執行價低於 100%，會有緩衝
        stock_value = (perf / strike_price) * face_value
        payoff.append(stock_value)

# --- 繪圖呈現 ---
fig, ax = plt.subplots(figsize=(10, 6))

# 繪製主線
ax.plot(underlying_perf * 100, payoff, color='#00ffcc', linewidth=3, label='TwinWin 到期價值')

# 繪製 100% 參考線
ax.axvline(x=100, color='white', linestyle='--', alpha=0.3)
ax.axhline(y=100, color='white', linestyle='--', alpha=0.3)

# 繪製 EKI 警戒線
ax.axvline(x=eki_barrier * 100, color='#ff4444', linestyle='-', label=f'EKI 門檻 ({int(eki_barrier*100)}%)')

# 著色獲利區 (TwinWin Zone)
ax.fill_between(underlying_perf * 100, payoff, 100, 
                where=(underlying_perf >= eki_barrier), 
                color='#00ffcc', alpha=0.1, label='獲利區間')

# 圖表美化
ax.set_title(f"TwinWin Payoff Curve (Strike: {strike_price*100:.2f}%)", fontsize=14, pad=20)
ax.set_xlabel("標的表現 (%)", fontsize=12)
ax.set_ylabel("到期結算價值 (不含配息)", fontsize=12)
ax.legend(loc='upper left')
ax.grid(True, alpha=0.1)

# 在 Streamlit 顯示圖表
st.pyplot(fig)

# --- 下方數據解說 ---
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("若標的上漲 15%", "115.0", "Bullish 勝")
with col2:
    st.metric("若標的小跌 15%", "115.0", "Bearish 勝 (雙贏點)")
with col3:
    st.error(f"若跌破 {eki_barrier*100:.0f}% 門檻")
    st.write(f"將依執行價 {strike_price*100:.2f}% 接貨")

st.markdown("---")
st.caption("註：本模擬器僅供說明 TwinWin 結構之邏輯，實際結算金額請依銀行正式對帳單為準。")
