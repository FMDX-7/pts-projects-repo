import os
import pandas as pd
import matplotlib.pyplot as plt


def ensure_dir(path):
    os.makedirs(path, exist_ok=True)


def load_csv(path='logs/sample_backtest.csv'):
    df = pd.read_csv(path, parse_dates=['timestamp'])
    # normalize timezone-like Z to UTC (pandas handles ISO OK)
    return df


def plot_cumulative_pnl(df, out_path='plots/cumulative_pnl.png'):
    df = df.sort_values('timestamp')
    df['pnl'] = df['pnl'].astype(float)
    df['cum_pnl'] = df['pnl'].cumsum()
    plt.figure(figsize=(8,4))
    plt.plot(df['timestamp'], df['cum_pnl'], marker='o')
    plt.title('Cumulative PnL')
    plt.ylabel('Cumulative PnL')
    plt.xlabel('Time')
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(out_path)
    plt.close()


def plot_pnl_by_symbol(df, out_path='plots/pnl_by_symbol.png'):
    agg = df.groupby('symbol')['pnl'].sum().sort_values()
    plt.figure(figsize=(6,4))
    agg.plot(kind='barh', color='tab:blue')
    plt.title('Total PnL by Symbol')
    plt.xlabel('PnL')
    plt.tight_layout()
    plt.savefig(out_path)
    plt.close()


def main():
    df = load_csv()
    ensure_dir('plots')
    plot_cumulative_pnl(df)
    plot_pnl_by_symbol(df)
    print('Plots written to ./plots (cumulative_pnl.png, pnl_by_symbol.png)')


if __name__ == '__main__':
    main()
