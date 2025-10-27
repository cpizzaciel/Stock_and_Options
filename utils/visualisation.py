import matplotlib.pyplot as plt
import seaborn as sns
from datetime import date
from mpl_toolkits.mplot3d import Axes3D
import pandas as pd
import numpy as np

plt.style.use('seaborn-v0_8-darkgrid')

def plot_monte_carlo(simulation_df: pd.DataFrame, title:str = "Monte Carlo Simulation", last_n_days: int = None):
    fig, ax = plt.subplots(figsize=(12, 7))
    plot_data = simulation_df.tail(last_n_days) if last_n_days else simulation_df
    plot_data.plot(ax=ax,
                   legend = False,
                   alpha = 0.1,
                   color = 'blue',
                   linewidth = 1,
                   )
    mean_path = plot_data.mean(axis=1)
    median_path = plot_data.median(axis=1)
    mean_path.plot(ax=ax, legend=False, color='red', linewidth=2.5, label='Mean Path')
    median_path.plot(ax=ax, legend=False, color='green', linewidth=2.5, linestyle='--', label='Median Path')


    ax.set_title(title, fontsize=16)
    ax.set_xlabel("Trading Days", fontsize=12)
    ax.set_ylabel("Stock Price", fontsize=12)

    initial_price = simulation_df.iloc[0].mean()
    ax.axhline(y=initial_price, color='grey', linestyle=':', linewidth=2, label=f'Initial Price: ${initial_price:.2f}')


def simulation_price_distribution(simulation_df: pd.DataFrame, title: str = "Price distribution", num_bins: int = 100):
    last_day_prices = simulation_df.iloc[-1]
    tickers = last_day_prices.index.get_level_values('ticker').unique()
    num_tickers = len(tickers)
    fig, axes = plt.subplots(
        nrows=num_tickers,
        ncols=1,
        figsize=(10, 6 * num_tickers),
        squeeze=False  # 即使只有一个子图，也保持 axes 是一个二维数组
    )
    axes = axes.flatten()
    for i, ticker in enumerate(tickers):
        # a. 选取当前这只股票的所有模拟价格
        ticker_prices = last_day_prices.loc[(slice(None), ticker)]

        # b. 在对应的子图 (ax) 上绘制直方图
        #    sns.histplot 提供了比 plt.hist 更美观的默认样式和核密度估计曲线 (kde)
        sns.histplot(ticker_prices, ax=axes[i], bins=num_bins, kde=True)

        # c. 在图上标记出统计数据，让图表信息更丰富
        mean_price = ticker_prices.mean()
        median_price = ticker_prices.median()
        std_dev = ticker_prices.std()

        # 标记平均值
        axes[i].axvline(mean_price, color='red', linestyle='--', linewidth=2, label=f'Mean: ${mean_price:.2f}')
        # 标记中位数
        axes[i].axvline(median_price, color='green', linestyle=':', linewidth=2, label=f'Median: ${median_price:.2f}')

        # d. 设置子图的标题和标签
        axes[i].set_title(f'Final Price Distribution for {ticker}', fontsize=14)
        axes[i].set_xlabel("Simulated Stock Price", fontsize=10)
        axes[i].set_ylabel("Frequency", fontsize=10)
        axes[i].legend()

        # 5. 设置整个图表的总标题，并调整布局
    fig.suptitle(title, fontsize=20, y=1.02)
    fig.tight_layout()  # 自动调整子图间距，防止重叠

    # 6. 显示图表
