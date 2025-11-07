# Statistical Arbitrage Pairs Trading Bot

A complete implementation of a pairs trading strategy based on statistical arbitrage. This project demonstrates quantitative finance concepts including cointegration testing, spread calculation, and algorithmic trading signal generation.

## 📊 Overview

This bot identifies pairs of stocks that move together (cointegrated) and exploits short-term deviations in their price relationship. It's based on the mean-reversion principle: when the price spread between two cointegrated stocks deviates from its historical average, it tends to revert back.

## 🎯 Key Features

- **Cointegration Analysis**: Uses the Engle-Granger test to identify statistically related stock pairs
- **Stationarity Testing**: Implements the Augmented Dickey-Fuller (ADF) test for spread stationarity
- **Automated Signal Generation**: Generates trading signals based on Z-score thresholds
- **Backtesting Framework**: Complete backtesting engine with performance metrics
- **Visualization**: Comprehensive plotting of spreads, Z-scores, and equity curves

## 🚀 Getting Started

### Prerequisites

Python 3.8 or higher is required.

### Installation

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the trading bot:
   ```bash
   python pairs_trading_bot.py
   ```

## 📈 How It Works

### 1. Finding Cointegrated Pairs

The bot uses statistical tests to find pairs of stocks that move together:

```python
from pairs_trading_bot import PairsFinder

# Define stock universe
tickers = ['PEP', 'KO', 'F', 'GM']
finder = PairsFinder(tickers, start_date='2022-01-01', end_date='2024-01-01')

# Find cointegrated pairs
pairs = finder.find_cointegrated_pairs(significance_level=0.05)
print(pairs)
```

### 2. Calculating the Spread

The spread represents the price difference between the two stocks, adjusted by a hedge ratio:

```
spread = price_A - hedge_ratio × price_B
```

The hedge ratio is calculated using linear regression to determine the optimal relationship.

### 3. Z-Score Calculation

The Z-score measures how many standard deviations the current spread is from its historical mean:

```
Z-score = (spread - rolling_mean) / rolling_std
```

### 4. Trading Signals

**Entry Signals:**
- Z-score > +2.0: Spread is unusually wide → Short stock A, Long stock B
- Z-score < -2.0: Spread is unusually narrow → Long stock A, Short stock B

**Exit Signals:**
- Z-score returns to 0: Close the position and capture profit

### 5. Example Usage

```python
from pairs_trading_bot import PairsTradingStrategy, Backtester

# Initialize strategy for PEP and KO
strategy = PairsTradingStrategy('PEP', 'KO', '2022-01-01', '2024-01-01')
strategy.fetch_data()

# Run backtest
backtester = Backtester(strategy, initial_capital=100000)
results = backtester.run_backtest(entry_threshold=2.0, exit_threshold=0.5)

# Get performance metrics
metrics = backtester.calculate_metrics()
print(f"Total Return: {metrics['total_return']:.2f}%")
print(f"Sharpe Ratio: {metrics['sharpe_ratio']:.2f}")

# Visualize results
backtester.plot_results(save_path='results.png')
```

## 📊 Performance Metrics

The backtester calculates the following metrics:

- **Total Return**: Overall percentage return on investment
- **Annualized Return**: Return normalized to a yearly basis
- **Sharpe Ratio**: Risk-adjusted return measure
- **Maximum Drawdown**: Largest peak-to-trough decline
- **Win Rate**: Percentage of profitable trades
- **Total Trades**: Number of round-trip trades executed

## 🔬 Statistical Tests

### Engle-Granger Cointegration Test
Tests whether two non-stationary time series have a stationary linear combination (the spread). A p-value < 0.05 indicates cointegration.

### Augmented Dickey-Fuller (ADF) Test
Tests whether a time series is stationary. Used to verify that the spread is mean-reverting.

## 📁 Project Structure

```
pairs_trading_bot.py       # Main implementation
requirements.txt           # Python dependencies
PAIRS_TRADING_README.md   # This file
```

## 🎓 Classes and Functions

### PairsFinder
- `fetch_data()`: Download historical price data
- `test_cointegration()`: Test if two stocks are cointegrated
- `find_cointegrated_pairs()`: Find all cointegrated pairs in a universe

### PairsTradingStrategy
- `fetch_data()`: Download pair data
- `calculate_spread()`: Calculate the price spread
- `calculate_zscore()`: Calculate Z-score of the spread
- `generate_signals()`: Generate trading signals

### Backtester
- `run_backtest()`: Simulate trading strategy
- `calculate_metrics()`: Compute performance metrics
- `plot_results()`: Visualize backtest results

### Utility Functions
- `test_stationarity()`: ADF test for stationarity

## 💡 Example Pairs to Test

**Consumer Goods:**
- PEP (Pepsi) vs KO (Coca-Cola)

**Automotive:**
- F (Ford) vs GM (General Motors)

**Technology:**
- MSFT (Microsoft) vs GOOGL (Google)

**Finance:**
- JPM (JP Morgan) vs BAC (Bank of America)

## 📚 Dependencies

- `numpy`: Numerical computing
- `pandas`: Data manipulation
- `matplotlib`: Plotting and visualization
- `scipy`: Scientific computing
- `statsmodels`: Statistical tests (ADF, cointegration)
- `yfinance`: Download stock data from Yahoo Finance
- `seaborn`: Statistical data visualization

## ⚠️ Disclaimer

This project is for educational purposes only. It demonstrates quantitative trading concepts but should not be used for actual trading without proper risk management, transaction cost modeling, and professional financial advice.

## 🎯 Why This Project Matters

This project demonstrates:

1. **Statistical Expertise**: Implementation of advanced statistical tests (ADF, Engle-Granger)
2. **Algorithmic Thinking**: Translation of statistical relationships into concrete trading rules
3. **End-to-End Development**: Complete workflow from data acquisition to strategy evaluation
4. **Quantitative Finance Knowledge**: Understanding of pairs trading and mean reversion
5. **Python Proficiency**: Clean, well-documented, object-oriented code

## 📖 Further Reading

- Vidyamurthy, G. (2004). *Pairs Trading: Quantitative Methods and Analysis*
- Chan, E. (2009). *Quantitative Trading: How to Build Your Own Algorithmic Trading Business*
- Pole, A. (2007). *Statistical Arbitrage: Algorithmic Trading Insights and Techniques*

## 📝 License

MIT License - See the main repository LICENSE file for details.

---

© 2024 - Statistical Arbitrage Pairs Trading Bot
