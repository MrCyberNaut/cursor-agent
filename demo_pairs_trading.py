"""
Pairs Trading Bot Demo with Synthetic Data

This demo script showcases the pairs trading bot functionality using synthetic
cointegrated stock data. Perfect for testing and demonstration when network
access is limited.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from pairs_trading_bot import PairsTradingStrategy, Backtester, test_stationarity
from scipy import stats


def generate_synthetic_pair(n_days=500, drift=0.0001, volatility=0.02, 
                           cointegration_strength=0.8, seed=42):
    """
    Generate synthetic cointegrated stock pair.
    
    Args:
        n_days: Number of trading days to simulate
        drift: Daily drift rate
        volatility: Daily volatility
        cointegration_strength: Strength of cointegration (0-1)
        seed: Random seed for reproducibility
        
    Returns:
        DataFrame with prices for both stocks
    """
    np.random.seed(seed)
    
    # Generate dates
    start_date = datetime.now() - timedelta(days=n_days)
    dates = pd.date_range(start=start_date, periods=n_days, freq='D')
    
    # Generate common trend (this creates cointegration)
    common_trend = np.cumsum(np.random.randn(n_days) * volatility + drift)
    
    # Generate individual components
    individual_1 = np.cumsum(np.random.randn(n_days) * volatility * (1 - cointegration_strength))
    individual_2 = np.cumsum(np.random.randn(n_days) * volatility * (1 - cointegration_strength))
    
    # Combine to create cointegrated series
    stock1_returns = common_trend + individual_1
    stock2_returns = common_trend + individual_2
    
    # Convert to prices (starting at $100)
    stock1_prices = 100 * np.exp(stock1_returns)
    stock2_prices = 100 * np.exp(stock2_returns)
    
    # Create DataFrame
    df = pd.DataFrame({
        'STOCK_A': stock1_prices,
        'STOCK_B': stock2_prices
    }, index=dates)
    
    return df


def demo_pairs_trading():
    """Run complete pairs trading demo with synthetic data."""
    
    print("=" * 80)
    print("PAIRS TRADING BOT - DEMO WITH SYNTHETIC DATA")
    print("=" * 80)
    print()
    
    # Generate synthetic cointegrated pair
    print("Generating synthetic cointegrated stock pair...")
    synthetic_data = generate_synthetic_pair(n_days=500, cointegration_strength=0.85)
    
    print(f"Generated {len(synthetic_data)} days of price data")
    print(f"Stock A: ${synthetic_data['STOCK_A'].iloc[0]:.2f} → ${synthetic_data['STOCK_A'].iloc[-1]:.2f}")
    print(f"Stock B: ${synthetic_data['STOCK_B'].iloc[0]:.2f} → ${synthetic_data['STOCK_B'].iloc[-1]:.2f}")
    
    # Create a modified strategy class that uses pre-loaded data
    class SyntheticPairsTradingStrategy(PairsTradingStrategy):
        """Modified strategy that uses synthetic data instead of downloading."""
        
        def __init__(self, data: pd.DataFrame):
            self.stock1 = 'STOCK_A'
            self.stock2 = 'STOCK_B'
            self.price_data = data
            self.spread = None
            self.zscore = None
            self.hedge_ratio = None
            self.start_date = data.index[0].strftime('%Y-%m-%d')
            self.end_date = data.index[-1].strftime('%Y-%m-%d')
        
        def fetch_data(self):
            """Override to use synthetic data."""
            return self.price_data
    
    # Initialize strategy with synthetic data
    strategy = SyntheticPairsTradingStrategy(synthetic_data)
    
    print("\n" + "-" * 80)
    print("ANALYZING PAIR RELATIONSHIP")
    print("-" * 80)
    
    # Calculate spread and Z-score
    spread = strategy.calculate_spread()
    zscore = strategy.calculate_zscore(window=20)
    
    print(f"Hedge ratio: {strategy.hedge_ratio:.4f}")
    print(f"Spread - Mean: {spread.mean():.4f}, Std: {spread.std():.4f}")
    print(f"Z-score - Mean: {zscore.mean():.4f}, Std: {zscore.std():.4f}")
    
    # Test stationarity of the spread
    is_stationary, adf_pvalue = test_stationarity(spread)
    print(f"\nSpread stationarity test (ADF):")
    print(f"  Is stationary: {is_stationary}")
    print(f"  P-value: {adf_pvalue:.6f}")
    
    # Run backtest with different parameter sets
    print("\n" + "=" * 80)
    print("BACKTESTING STRATEGY")
    print("=" * 80)
    
    param_sets = [
        {'entry': 2.0, 'exit': 0.5, 'size': 0.5},
        {'entry': 2.5, 'exit': 0.5, 'size': 0.5},
        {'entry': 1.5, 'exit': 0.3, 'size': 0.5},
    ]
    
    best_sharpe = -999
    best_params = None
    all_results = []
    
    for params in param_sets:
        backtester = Backtester(strategy, initial_capital=100000)
        results = backtester.run_backtest(
            entry_threshold=params['entry'],
            exit_threshold=params['exit'],
            position_size=params['size']
        )
        metrics = backtester.calculate_metrics()
        
        all_results.append({
            'params': params,
            'metrics': metrics,
            'backtester': backtester
        })
        
        if metrics['sharpe_ratio'] > best_sharpe:
            best_sharpe = metrics['sharpe_ratio']
            best_params = params
        
        print(f"\nParameters: Entry={params['entry']}, Exit={params['exit']}, Size={params['size']}")
        print(f"  Total Return: {metrics['total_return']:.2f}%")
        print(f"  Sharpe Ratio: {metrics['sharpe_ratio']:.2f}")
        print(f"  Max Drawdown: {metrics['max_drawdown']:.2f}%")
        print(f"  Total Trades: {metrics['total_trades']:.0f}")
    
    # Display best results
    print("\n" + "=" * 80)
    print("BEST STRATEGY RESULTS")
    print("=" * 80)
    print(f"Best Parameters: Entry={best_params['entry']}, Exit={best_params['exit']}, Size={best_params['size']}")
    
    # Get the best backtester
    best_result = [r for r in all_results if r['params'] == best_params][0]
    best_backtester = best_result['backtester']
    best_metrics = best_result['metrics']
    
    print(f"\nPerformance Metrics:")
    print(f"  Total Return: {best_metrics['total_return']:.2f}%")
    print(f"  Annualized Return: {best_metrics['annualized_return']:.2f}%")
    print(f"  Sharpe Ratio: {best_metrics['sharpe_ratio']:.2f}")
    print(f"  Maximum Drawdown: {best_metrics['max_drawdown']:.2f}%")
    print(f"  Win Rate: {best_metrics['win_rate']:.2f}%")
    print(f"  Total Trades: {best_metrics['total_trades']:.0f}")
    
    # Plot results
    print("\n" + "=" * 80)
    print("GENERATING VISUALIZATIONS")
    print("=" * 80)
    
    fig, axes = plt.subplots(4, 1, figsize=(14, 12))
    
    results = best_backtester.results
    
    # Plot 1: Price series
    ax1 = axes[0]
    ax1.plot(results.index, results['price1'], label='Stock A', linewidth=1.5, color='blue')
    ax1.plot(results.index, results['price2'], label='Stock B', linewidth=1.5, color='orange')
    ax1.set_title('Synthetic Stock Prices (Cointegrated Pair)', fontsize=12, fontweight='bold')
    ax1.set_ylabel('Price ($)')
    ax1.legend(loc='best')
    ax1.grid(True, alpha=0.3)
    
    # Plot 2: Spread
    ax2 = axes[1]
    ax2.plot(results.index, results['spread'], label='Spread', color='purple', linewidth=1.5)
    ax2.axhline(y=results['spread'].mean(), color='black', linestyle='--', 
               label=f'Mean ({results["spread"].mean():.2f})', linewidth=1)
    ax2.fill_between(results.index, 
                     results['spread'].mean() - results['spread'].std(),
                     results['spread'].mean() + results['spread'].std(),
                     alpha=0.2, color='purple', label='±1 Std Dev')
    ax2.set_title('Price Spread', fontsize=12, fontweight='bold')
    ax2.set_ylabel('Spread')
    ax2.legend(loc='best')
    ax2.grid(True, alpha=0.3)
    
    # Plot 3: Z-score with entry/exit signals
    ax3 = axes[2]
    ax3.plot(results.index, results['zscore'], label='Z-score', color='blue', linewidth=1.5)
    ax3.axhline(y=0, color='black', linestyle='-', linewidth=1, label='Mean')
    ax3.axhline(y=best_params['entry'], color='red', linestyle='--', 
               label=f'Entry threshold (±{best_params["entry"]})', linewidth=1)
    ax3.axhline(y=-best_params['entry'], color='red', linestyle='--', linewidth=1)
    ax3.axhline(y=best_params['exit'], color='green', linestyle=':', 
               label=f'Exit threshold (±{best_params["exit"]})', linewidth=1)
    ax3.axhline(y=-best_params['exit'], color='green', linestyle=':', linewidth=1)
    
    # Mark entry points
    entry_long = results[(results['signal'] == 1)]
    entry_short = results[(results['signal'] == -1)]
    
    if not entry_long.empty:
        ax3.scatter(entry_long.index, entry_long['zscore'], color='green', 
                   marker='^', s=100, label='Long entry', zorder=5)
    if not entry_short.empty:
        ax3.scatter(entry_short.index, entry_short['zscore'], color='red', 
                   marker='v', s=100, label='Short entry', zorder=5)
    
    ax3.set_title('Z-Score and Trading Signals', fontsize=12, fontweight='bold')
    ax3.set_ylabel('Z-score')
    ax3.legend(loc='best', fontsize=8)
    ax3.grid(True, alpha=0.3)
    
    # Plot 4: Equity curve
    ax4 = axes[3]
    ax4.plot(results.index, results['equity'], label='Portfolio Value', 
            color='green', linewidth=2)
    ax4.axhline(y=best_backtester.initial_capital, color='black', linestyle='--', 
               label='Initial Capital ($100,000)', linewidth=1)
    
    # Shade profitable/unprofitable regions
    final_value = results['equity'].iloc[-1]
    color = 'green' if final_value > best_backtester.initial_capital else 'red'
    ax4.fill_between(results.index, best_backtester.initial_capital, results['equity'], 
                     where=(results['equity'] >= best_backtester.initial_capital),
                     alpha=0.2, color='green', label='Profit')
    ax4.fill_between(results.index, best_backtester.initial_capital, results['equity'],
                     where=(results['equity'] < best_backtester.initial_capital),
                     alpha=0.2, color='red', label='Loss')
    
    ax4.set_title(f'Equity Curve (Final: ${final_value:,.0f}, Return: {best_metrics["total_return"]:.2f}%)', 
                 fontsize=12, fontweight='bold')
    ax4.set_xlabel('Date')
    ax4.set_ylabel('Portfolio Value ($)')
    ax4.legend(loc='best')
    ax4.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('pairs_trading_demo_results.png', dpi=300, bbox_inches='tight')
    print("\nVisualization saved to: pairs_trading_demo_results.png")
    
    # Create summary statistics plot
    fig2, axes2 = plt.subplots(2, 2, figsize=(12, 8))
    
    # Trade distribution
    ax1 = axes2[0, 0]
    trade_returns = results[results['strategy_returns'] != 0]['strategy_returns'] * 100
    ax1.hist(trade_returns, bins=30, alpha=0.7, color='blue', edgecolor='black')
    ax1.axvline(x=0, color='red', linestyle='--', linewidth=2)
    ax1.set_title('Distribution of Trade Returns', fontweight='bold')
    ax1.set_xlabel('Return (%)')
    ax1.set_ylabel('Frequency')
    ax1.grid(True, alpha=0.3)
    
    # Cumulative returns
    ax2 = axes2[0, 1]
    cumulative_pct = (results['cumulative_returns'] - 1) * 100
    ax2.plot(results.index, cumulative_pct, linewidth=2, color='green')
    ax2.axhline(y=0, color='black', linestyle='--', linewidth=1)
    ax2.set_title('Cumulative Returns Over Time', fontweight='bold')
    ax2.set_xlabel('Date')
    ax2.set_ylabel('Cumulative Return (%)')
    ax2.grid(True, alpha=0.3)
    
    # Drawdown
    ax3 = axes2[1, 0]
    cumulative = results['cumulative_returns']
    running_max = cumulative.expanding().max()
    drawdown = (cumulative - running_max) / running_max * 100
    ax3.fill_between(results.index, 0, drawdown, alpha=0.5, color='red')
    ax3.plot(results.index, drawdown, linewidth=1, color='darkred')
    ax3.set_title(f'Drawdown (Max: {best_metrics["max_drawdown"]:.2f}%)', fontweight='bold')
    ax3.set_xlabel('Date')
    ax3.set_ylabel('Drawdown (%)')
    ax3.grid(True, alpha=0.3)
    
    # Position distribution
    ax4 = axes2[1, 1]
    position_counts = results['position'].value_counts()
    colors = ['gray', 'green', 'red']
    labels = ['No Position', 'Long Spread', 'Short Spread']
    ax4.pie(position_counts.values, labels=[labels[int(p)+1] for p in position_counts.index],
           autopct='%1.1f%%', colors=[colors[int(p)+1] for p in position_counts.index],
           startangle=90)
    ax4.set_title('Position Distribution', fontweight='bold')
    
    plt.tight_layout()
    plt.savefig('pairs_trading_demo_statistics.png', dpi=300, bbox_inches='tight')
    print("Statistics visualization saved to: pairs_trading_demo_statistics.png")
    
    print("\n" + "=" * 80)
    print("DEMO COMPLETE!")
    print("=" * 80)
    print("\nKey Takeaways:")
    print("1. Successfully identified a cointegrated pair (synthetic data)")
    print("2. Calculated spread with hedge ratio:", f"{strategy.hedge_ratio:.4f}")
    print("3. Generated trading signals based on Z-score thresholds")
    print("4. Backtested strategy with performance metrics")
    print("5. Created comprehensive visualizations")
    print("\nThis demonstrates a complete quantitative trading workflow:")
    print("  ✓ Statistical analysis (cointegration, stationarity)")
    print("  ✓ Signal generation (Z-score based)")
    print("  ✓ Backtesting framework")
    print("  ✓ Performance evaluation")
    print("  ✓ Visualization and reporting")


if __name__ == "__main__":
    demo_pairs_trading()
