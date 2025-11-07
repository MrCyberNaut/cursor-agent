#!/usr/bin/env python3
"""
Quick Start Guide for Pairs Trading Bot

This script provides a simple tutorial on using the pairs trading bot.
It demonstrates all the main features step-by-step.
"""

import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from pairs_trading_bot import (
    PairsFinder,
    PairsTradingStrategy, 
    Backtester,
    test_stationarity
)


def main():
    print("=" * 80)
    print("PAIRS TRADING BOT - QUICK START GUIDE")
    print("=" * 80)
    print()
    
    print("This guide demonstrates how to use the pairs trading bot.")
    print("For this demo, we'll use synthetic data since real market data")
    print("requires network access.")
    print()
    
    # Step 1: Generate synthetic data
    print("-" * 80)
    print("STEP 1: Prepare Data")
    print("-" * 80)
    print()
    print("For real trading, you would:")
    print("  1. Define a universe of stocks (e.g., ['PEP', 'KO', 'F', 'GM'])")
    print("  2. Use PairsFinder to test for cointegration")
    print("  3. Select the best pair based on p-value")
    print()
    print("Example code:")
    print("  finder = PairsFinder(['PEP', 'KO'], '2022-01-01', '2024-01-01')")
    print("  finder.fetch_data()")
    print("  is_coint, p_value = finder.test_cointegration('PEP', 'KO')")
    print()
    
    # Generate synthetic data for demo
    from demo_pairs_trading import generate_synthetic_pair
    data = generate_synthetic_pair(n_days=252, seed=42)  # 1 year of data
    print("For this demo, we've generated synthetic cointegrated data.")
    print(f"Data shape: {data.shape}")
    print()
    
    # Step 2: Initialize Strategy
    print("-" * 80)
    print("STEP 2: Initialize Trading Strategy")
    print("-" * 80)
    print()
    print("Create a PairsTradingStrategy object:")
    print()
    
    # Create strategy with synthetic data
    class DemoStrategy(PairsTradingStrategy):
        def __init__(self, data):
            self.stock1 = 'STOCK_A'
            self.stock2 = 'STOCK_B'
            self.price_data = data
            self.spread = None
            self.zscore = None
            self.hedge_ratio = None
    
    strategy = DemoStrategy(data)
    print("✓ Strategy initialized with STOCK_A and STOCK_B")
    print()
    
    # Step 3: Calculate Spread
    print("-" * 80)
    print("STEP 3: Calculate Spread and Hedge Ratio")
    print("-" * 80)
    print()
    print("The spread is: price_A - hedge_ratio * price_B")
    print()
    
    spread = strategy.calculate_spread()
    print(f"✓ Spread calculated")
    print(f"  Hedge Ratio: {strategy.hedge_ratio:.4f}")
    print(f"  Mean Spread: {spread.mean():.2f}")
    print(f"  Std Spread: {spread.std():.2f}")
    print()
    
    # Test stationarity
    is_stationary, p_value = test_stationarity(spread)
    print(f"✓ Stationarity Test (ADF):")
    print(f"  Is Stationary: {is_stationary}")
    print(f"  P-value: {p_value:.6f}")
    print()
    
    # Step 4: Calculate Z-score
    print("-" * 80)
    print("STEP 4: Calculate Z-Score")
    print("-" * 80)
    print()
    print("Z-score = (spread - rolling_mean) / rolling_std")
    print()
    
    zscore = strategy.calculate_zscore(window=20)
    print(f"✓ Z-score calculated with 20-day rolling window")
    print(f"  Mean Z-score: {zscore.mean():.4f}")
    print(f"  Std Z-score: {zscore.std():.4f}")
    print(f"  Max Z-score: {zscore.max():.4f}")
    print(f"  Min Z-score: {zscore.min():.4f}")
    print()
    
    # Step 5: Generate Signals
    print("-" * 80)
    print("STEP 5: Generate Trading Signals")
    print("-" * 80)
    print()
    print("Trading Rules:")
    print("  • Z-score > +2.0: Short spread (Short A, Long B)")
    print("  • Z-score < -2.0: Long spread (Long A, Short B)")
    print("  • Z-score → 0: Exit position")
    print()
    
    signals = strategy.generate_signals(entry_threshold=2.0, exit_threshold=0.5)
    num_signals = len(signals[signals['signal'] != 0])
    print(f"✓ Generated {num_signals} entry signals")
    print()
    
    # Step 6: Backtest
    print("-" * 80)
    print("STEP 6: Run Backtest")
    print("-" * 80)
    print()
    print("Simulate trading with:")
    print("  • Initial Capital: $100,000")
    print("  • Entry Threshold: ±2.0")
    print("  • Exit Threshold: ±0.5")
    print("  • Position Size: 50% of capital")
    print()
    
    backtester = Backtester(strategy, initial_capital=100000)
    results = backtester.run_backtest(
        entry_threshold=2.0,
        exit_threshold=0.5,
        position_size=0.5
    )
    
    print(f"✓ Backtest complete")
    print(f"  Simulated {len(results)} trading days")
    print()
    
    # Step 7: Analyze Results
    print("-" * 80)
    print("STEP 7: Analyze Performance")
    print("-" * 80)
    print()
    
    metrics = backtester.calculate_metrics()
    
    print("Performance Metrics:")
    print(f"  Total Return:      {metrics['total_return']:>8.2f}%")
    print(f"  Annualized Return: {metrics['annualized_return']:>8.2f}%")
    print(f"  Sharpe Ratio:      {metrics['sharpe_ratio']:>8.2f}")
    print(f"  Maximum Drawdown:  {metrics['max_drawdown']:>8.2f}%")
    print(f"  Win Rate:          {metrics['win_rate']:>8.2f}%")
    print(f"  Total Trades:      {metrics['total_trades']:>8.0f}")
    print()
    
    # Step 8: Visualize
    print("-" * 80)
    print("STEP 8: Generate Visualizations")
    print("-" * 80)
    print()
    print("Creating comprehensive plots...")
    print()
    
    backtester.plot_results(save_path='quickstart_results.png')
    print("✓ Visualization saved to: quickstart_results.png")
    print()
    
    # Summary
    print("=" * 80)
    print("QUICK START COMPLETE!")
    print("=" * 80)
    print()
    print("What you've learned:")
    print("  1. How to test for cointegration between stock pairs")
    print("  2. How to calculate spread and hedge ratio")
    print("  3. How to compute Z-scores for mean reversion signals")
    print("  4. How to generate trading signals")
    print("  5. How to backtest a pairs trading strategy")
    print("  6. How to evaluate strategy performance")
    print("  7. How to visualize results")
    print()
    print("Next Steps:")
    print("  • Try different entry/exit thresholds")
    print("  • Test with real stock data (requires network)")
    print("  • Experiment with different stock pairs")
    print("  • Add transaction costs to backtest")
    print("  • Implement risk management rules")
    print()
    print("For more information, see PAIRS_TRADING_README.md")
    print()
    

if __name__ == "__main__":
    main()
