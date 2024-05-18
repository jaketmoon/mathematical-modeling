import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei']  # 设置简黑字体
plt.rcParams['axes.unicode_minus'] = False  # 解决负号'-'显示为方块的问题

# 价格
prices = list(range(15, 31))  # 从 15 元到 30 元，步长为 1 元

# 计算每天的销售量和利润
quantities = [540 - 20 * (p - 15) for p in prices]
profits = [(p - 12) * q for p, q in zip(prices, quantities)]

# 画图
plt.plot(prices, profits, marker='o')
plt.title('酱香拿铁售价与利润关系')
plt.xlabel('售价（元/杯）')
plt.ylabel('每日利润（元）')
plt.grid(True)
plt.show()