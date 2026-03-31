import numpy as np
import matplotlib.pyplot as plt

# --- 參數設定 (根據你的報價單) ---
strike_price = 0.6195  # 執行價 (以 ASML/LRCX 為例)
eki_barrier = 0.60     # 下限觸發門檻 (60%)
face_value = 100       # 原始本金

# 模擬標的到期時的表現 (從 0% 到 150%)
underlying_perf = np.linspace(0, 1.5, 500)
payoff = []

for perf in underlying_perf:
    # 情況 1: 沒破 EKI (大於 60%)
    if perf >= eki_barrier:
        if perf >= 1.0:
            # 漲多少賺多少 (1 + [Perf - 100%])
            payoff.append(face_value * (1 + (perf - 1.0)))
        else:
            # 跌多少賺多少 (1 + [100% - Perf]) -> TwinWin 核心
            payoff.append(face_value * (1 + (1.0 - perf)))
            
    # 情況 2: 跌破 EKI (小於 60%) -> 實物結算
    else:
        # 拿到的股票價值 = (當前股價 / 執行價) * 本金
        stock_value = (perf / strike_price) * face_value
        payoff.append(stock_value)

# --- 繪圖 Vibe ---
plt.figure(figsize=(10, 6))
plt.plot(underlying_perf * 100, payoff, label='TwinWin Payoff', color='#00ffcc', linewidth=3)
plt.axvline(x=100, color='white', linestyle='--', alpha=0.5, label='Initial Price')
plt.axvline(x=60, color='#ff4444', linestyle='-', label='EKI Barrier (60%)')

# 裝飾美化
plt.fill_between(underlying_perf * 100, payoff, 100, where=(underlying_perf >= 0.6), 
                 color='#00ffcc', alpha=0.2, label='Profit Zone')
plt.title('TwinWin (Bullish Bearish) Structure Payoff', fontsize=14, color='white')
plt.xlabel('Underlying Performance (%)', color='white')
plt.ylabel('Payoff Amount', color='white')
plt.grid(True, alpha=0.1)
plt.legend()
plt.style.use('dark_background')
plt.show()
