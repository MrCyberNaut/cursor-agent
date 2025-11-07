"""
Statistical Arbitrage Pairs Trading Bot

This module implements a pairs trading strategy based on cointegration analysis.
It identifies pairs of stocks that move together and exploits short-term deviations
in their price relationship.
"""

import numpy as np
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
from statsmodels.tsa.stattools import adfuller, coint
from scipy import stats
from datetime import datetime, timedelta
from typing import Tuple, List, Dict, Optional


class PairsFinder:
    """Find cointegrated pairs of stocks from a given universe."""
    
    def __init__(self, tickers: List[str], start_date: str, end_date: str):
        """
        Initialize the PairsFinder.
        
        Args:
            tickers: List of stock ticker symbols
            start_date: Start date for historical data (YYYY-MM-DD)
            end_date: End date for historical data (YYYY-MM-DD)
        """
        self.tickers = tickers
        self.start_date = start_date
        self.end_date = end_date
        self.price_data = None
        
    def fetch_data(self) -> pd.DataFrame:
        """
        Download historical price data for all tickers.
        
        Returns:
            DataFrame with adjusted close prices for all tickers
        """
        print(f"Fetching data for {len(self.tickers)} tickers...")
        data = yf.download(self.tickers, start=self.start_date, end=self.end_date, progress=False)
        
        if len(self.tickers) == 1:
            self.price_data = pd.DataFrame(data['Adj Close'])
            self.price_data.columns = self.tickers
        else:
            self.price_data = data['Adj Close']
        
        # Drop any tickers with missing data
        self.price_data = self.price_data.dropna(axis=1)
        print(f"Successfully fetched data for {len(self.price_data.columns)} tickers")
        return self.price_data
    
    def test_cointegration(self, stock1: str, stock2: str, significance_level: float = 0.05) -> Tuple[bool, float]:
        """
        Test for cointegration between two stocks using Engle-Granger test.
        
        Args:
            stock1: First stock ticker
            stock2: Second stock ticker
            significance_level: P-value threshold for cointegration
            
        Returns:
            Tuple of (is_cointegrated, p_value)
        """
        if self.price_data is None:
            raise ValueError("Price data not loaded. Call fetch_data() first.")
        
        series1 = self.price_data[stock1].dropna()
        series2 = self.price_data[stock2].dropna()
        
        # Align the series
        common_idx = series1.index.intersection(series2.index)
        series1 = series1.loc[common_idx]
        series2 = series2.loc[common_idx]
        
        # Engle-Granger test
        score, p_value, _ = coint(series1, series2)
        
        is_cointegrated = p_value < significance_level
        return is_cointegrated, p_value
    
    def find_cointegrated_pairs(self, significance_level: float = 0.05) -> pd.DataFrame:
        """
        Find all cointegrated pairs from the ticker universe.
        
        Args:
            significance_level: P-value threshold for cointegration
            
        Returns:
            DataFrame with cointegrated pairs and their p-values
        """
        if self.price_data is None:
            self.fetch_data()
        
        pairs = []
        n = len(self.price_data.columns)
        
        print(f"Testing {n * (n - 1) // 2} pairs for cointegration...")
        
        for i in range(n):
            for j in range(i + 1, n):
                stock1 = self.price_data.columns[i]
                stock2 = self.price_data.columns[j]
                
                is_coint, p_value = self.test_cointegration(stock1, stock2, significance_level)
                
                if is_coint:
                    pairs.append({
                        'stock1': stock1,
                        'stock2': stock2,
                        'p_value': p_value
                    })
        
        pairs_df = pd.DataFrame(pairs)
        if not pairs_df.empty:
            pairs_df = pairs_df.sort_values('p_value')
        
        print(f"Found {len(pairs_df)} cointegrated pairs")
        return pairs_df


class PairsTradingStrategy:
    """Implement pairs trading strategy with spread calculation and signal generation."""
    
    def __init__(self, stock1: str, stock2: str, start_date: str, end_date: str):
        """
        Initialize the trading strategy.
        
        Args:
            stock1: First stock ticker
            stock2: Second stock ticker
            start_date: Start date for historical data (YYYY-MM-DD)
            end_date: End date for historical data (YYYY-MM-DD)
        """
        self.stock1 = stock1
        self.stock2 = stock2
        self.start_date = start_date
        self.end_date = end_date
        self.price_data = None
        self.spread = None
        self.zscore = None
        self.hedge_ratio = None
        
    def fetch_data(self) -> pd.DataFrame:
        """
        Download historical price data for the pair.
        
        Returns:
            DataFrame with prices for both stocks
        """
        print(f"Fetching data for {self.stock1} and {self.stock2}...")
        data = yf.download([self.stock1, self.stock2], start=self.start_date, 
                          end=self.end_date, progress=False)
        
        self.price_data = pd.DataFrame({
            self.stock1: data['Adj Close'][self.stock1],
            self.stock2: data['Adj Close'][self.stock2]
        }).dropna()
        
        print(f"Fetched {len(self.price_data)} data points")
        return self.price_data
    
    def calculate_spread(self, lookback_period: Optional[int] = None) -> pd.Series:
        """
        Calculate the spread between the two stocks.
        
        The spread is calculated as: price_stock1 - hedge_ratio * price_stock2
        The hedge ratio is determined by linear regression.
        
        Args:
            lookback_period: Number of periods to use for calculating hedge ratio.
                           If None, uses all available data.
        
        Returns:
            Series containing the spread values
        """
        if self.price_data is None:
            self.fetch_data()
        
        # Calculate hedge ratio using linear regression
        if lookback_period is None:
            X = self.price_data[self.stock2].values
            y = self.price_data[self.stock1].values
        else:
            X = self.price_data[self.stock2].iloc[-lookback_period:].values
            y = self.price_data[self.stock1].iloc[-lookback_period:].values
        
        # Add constant term for regression
        X_with_const = np.column_stack([np.ones(len(X)), X])
        coefficients = np.linalg.lstsq(X_with_const, y, rcond=None)[0]
        self.hedge_ratio = coefficients[1]
        
        # Calculate spread
        self.spread = self.price_data[self.stock1] - self.hedge_ratio * self.price_data[self.stock2]
        
        return self.spread
    
    def calculate_zscore(self, window: int = 20) -> pd.Series:
        """
        Calculate the Z-score of the spread.
        
        Z-score = (spread - rolling_mean) / rolling_std
        
        Args:
            window: Rolling window size for mean and std calculation
            
        Returns:
            Series containing the Z-score values
        """
        if self.spread is None:
            self.calculate_spread()
        
        # Calculate rolling statistics
        rolling_mean = self.spread.rolling(window=window).mean()
        rolling_std = self.spread.rolling(window=window).std()
        
        # Calculate Z-score
        self.zscore = (self.spread - rolling_mean) / rolling_std
        
        return self.zscore
    
    def generate_signals(self, entry_threshold: float = 2.0, 
                        exit_threshold: float = 0.0) -> pd.DataFrame:
        """
        Generate trading signals based on Z-score thresholds.
        
        Signal logic:
        - When Z-score > entry_threshold: Short stock1, Long stock2 (signal = -1)
        - When Z-score < -entry_threshold: Long stock1, Short stock2 (signal = 1)
        - When Z-score crosses exit_threshold: Close position (signal = 0)
        
        Args:
            entry_threshold: Z-score threshold for entering a position (default 2.0)
            exit_threshold: Z-score threshold for exiting a position (default 0.0)
            
        Returns:
            DataFrame with signals and positions
        """
        if self.zscore is None:
            self.calculate_zscore()
        
        signals = pd.DataFrame(index=self.price_data.index)
        signals['price1'] = self.price_data[self.stock1]
        signals['price2'] = self.price_data[self.stock2]
        signals['spread'] = self.spread
        signals['zscore'] = self.zscore
        signals['signal'] = 0
        
        # Generate entry signals
        signals.loc[signals['zscore'] > entry_threshold, 'signal'] = -1  # Short spread
        signals.loc[signals['zscore'] < -entry_threshold, 'signal'] = 1   # Long spread
        
        # Generate position based on signals (forward fill until exit)
        positions = []
        position = 0
        
        for i in range(len(signals)):
            current_signal = signals['signal'].iloc[i]
            current_zscore = signals['zscore'].iloc[i]
            
            # Enter new position
            if current_signal != 0 and position == 0:
                position = current_signal
            # Exit position when zscore crosses zero
            elif position != 0 and abs(current_zscore) < abs(exit_threshold):
                position = 0
            
            positions.append(position)
        
        signals['position'] = positions
        
        return signals


class Backtester:
    """Backtest the pairs trading strategy."""
    
    def __init__(self, strategy: PairsTradingStrategy, initial_capital: float = 100000):
        """
        Initialize the backtester.
        
        Args:
            strategy: PairsTradingStrategy instance
            initial_capital: Starting capital for backtesting
        """
        self.strategy = strategy
        self.initial_capital = initial_capital
        self.results = None
        
    def run_backtest(self, entry_threshold: float = 2.0, 
                    exit_threshold: float = 0.0,
                    position_size: float = 0.5) -> pd.DataFrame:
        """
        Run backtest simulation.
        
        Args:
            entry_threshold: Z-score threshold for entering positions
            exit_threshold: Z-score threshold for exiting positions
            position_size: Fraction of capital to use per position (0 to 1)
            
        Returns:
            DataFrame with backtest results including returns and equity curve
        """
        signals = self.strategy.generate_signals(entry_threshold, exit_threshold)
        
        results = signals.copy()
        
        # Calculate returns for each leg of the trade
        results['returns1'] = results['price1'].pct_change()
        results['returns2'] = results['price2'].pct_change()
        
        # Calculate strategy returns
        # When position = 1: Long stock1, Short stock2
        # When position = -1: Short stock1, Long stock2
        results['strategy_returns'] = (
            results['position'].shift(1) * results['returns1'] - 
            results['position'].shift(1) * self.strategy.hedge_ratio * results['returns2']
        ) * position_size
        
        # Calculate cumulative returns
        results['cumulative_returns'] = (1 + results['strategy_returns']).cumprod()
        results['equity'] = self.initial_capital * results['cumulative_returns']
        
        # Fill NaN values
        results = results.ffill().fillna(0)
        
        self.results = results
        return results
    
    def calculate_metrics(self) -> Dict[str, float]:
        """
        Calculate performance metrics.
        
        Returns:
            Dictionary containing performance metrics
        """
        if self.results is None:
            raise ValueError("Run backtest first using run_backtest()")
        
        returns = self.results['strategy_returns'].dropna()
        
        # Total return
        total_return = (self.results['equity'].iloc[-1] / self.initial_capital - 1) * 100
        
        # Annualized return
        trading_days = len(returns)
        years = trading_days / 252
        annualized_return = ((1 + total_return / 100) ** (1 / years) - 1) * 100 if years > 0 else 0
        
        # Sharpe ratio (assuming 252 trading days per year)
        sharpe_ratio = (returns.mean() / returns.std()) * np.sqrt(252) if returns.std() > 0 else 0
        
        # Maximum drawdown
        cumulative = self.results['cumulative_returns']
        running_max = cumulative.expanding().max()
        drawdown = (cumulative - running_max) / running_max
        max_drawdown = drawdown.min() * 100
        
        # Win rate
        winning_trades = len(returns[returns > 0])
        total_trades = len(returns[returns != 0])
        win_rate = (winning_trades / total_trades * 100) if total_trades > 0 else 0
        
        metrics = {
            'total_return': total_return,
            'annualized_return': annualized_return,
            'sharpe_ratio': sharpe_ratio,
            'max_drawdown': max_drawdown,
            'win_rate': win_rate,
            'total_trades': total_trades
        }
        
        return metrics
    
    def plot_results(self, save_path: Optional[str] = None):
        """
        Plot backtest results including spread, Z-score, and equity curve.
        
        Args:
            save_path: Optional path to save the plot
        """
        if self.results is None:
            raise ValueError("Run backtest first using run_backtest()")
        
        fig, axes = plt.subplots(4, 1, figsize=(14, 12))
        
        # Plot 1: Price series
        ax1 = axes[0]
        ax1.plot(self.results.index, self.results['price1'], label=self.strategy.stock1, linewidth=1.5)
        ax1.plot(self.results.index, self.results['price2'], label=self.strategy.stock2, linewidth=1.5)
        ax1.set_title('Stock Prices', fontsize=12, fontweight='bold')
        ax1.set_ylabel('Price ($)')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # Plot 2: Spread
        ax2 = axes[1]
        ax2.plot(self.results.index, self.results['spread'], label='Spread', color='purple', linewidth=1.5)
        ax2.axhline(y=self.results['spread'].mean(), color='black', linestyle='--', 
                   label='Mean', linewidth=1)
        ax2.set_title('Price Spread', fontsize=12, fontweight='bold')
        ax2.set_ylabel('Spread')
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        
        # Plot 3: Z-score with entry/exit signals
        ax3 = axes[2]
        ax3.plot(self.results.index, self.results['zscore'], label='Z-score', color='blue', linewidth=1.5)
        ax3.axhline(y=0, color='black', linestyle='-', linewidth=1)
        ax3.axhline(y=2.0, color='red', linestyle='--', label='Entry threshold', linewidth=1)
        ax3.axhline(y=-2.0, color='red', linestyle='--', linewidth=1)
        
        # Mark entry and exit points
        entry_long = self.results[(self.results['signal'] == 1)]
        entry_short = self.results[(self.results['signal'] == -1)]
        
        if not entry_long.empty:
            ax3.scatter(entry_long.index, entry_long['zscore'], color='green', 
                       marker='^', s=100, label='Long entry', zorder=5)
        if not entry_short.empty:
            ax3.scatter(entry_short.index, entry_short['zscore'], color='red', 
                       marker='v', s=100, label='Short entry', zorder=5)
        
        ax3.set_title('Z-Score and Trading Signals', fontsize=12, fontweight='bold')
        ax3.set_ylabel('Z-score')
        ax3.legend()
        ax3.grid(True, alpha=0.3)
        
        # Plot 4: Equity curve
        ax4 = axes[3]
        ax4.plot(self.results.index, self.results['equity'], label='Portfolio Value', 
                color='green', linewidth=2)
        ax4.axhline(y=self.initial_capital, color='black', linestyle='--', 
                   label='Initial Capital', linewidth=1)
        ax4.set_title('Equity Curve', fontsize=12, fontweight='bold')
        ax4.set_xlabel('Date')
        ax4.set_ylabel('Portfolio Value ($)')
        ax4.legend()
        ax4.grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"Plot saved to {save_path}")
        
        plt.show()


def test_stationarity(series: pd.Series, significance_level: float = 0.05) -> Tuple[bool, float]:
    """
    Test for stationarity using Augmented Dickey-Fuller test.
    
    Args:
        series: Time series to test
        significance_level: P-value threshold for stationarity
        
    Returns:
        Tuple of (is_stationary, p_value)
    """
    result = adfuller(series.dropna())
    adf_statistic = result[0]
    p_value = result[1]
    
    is_stationary = p_value < significance_level
    
    return is_stationary, p_value


if __name__ == "__main__":
    # Example usage: Find pairs and run backtest
    
    print("=" * 80)
    print("STATISTICAL ARBITRAGE PAIRS TRADING BOT")
    print("=" * 80)
    print()
    
    # Define parameters
    end_date = datetime.now().strftime('%Y-%m-%d')
    start_date = (datetime.now() - timedelta(days=2*365)).strftime('%Y-%m-%d')  # 2 years of data
    
    # Example 1: Test specific pairs (PEP vs KO, F vs GM)
    print("Testing predefined pairs for cointegration...")
    print("-" * 80)
    
    test_pairs = [
        ('PEP', 'KO'),   # Pepsi vs Coca-Cola
        ('F', 'GM')      # Ford vs General Motors
    ]
    
    for stock1, stock2 in test_pairs:
        finder = PairsFinder([stock1, stock2], start_date, end_date)
        finder.fetch_data()
        is_coint, p_value = finder.test_cointegration(stock1, stock2)
        
        print(f"\n{stock1} vs {stock2}:")
        print(f"  Cointegrated: {is_coint}")
        print(f"  P-value: {p_value:.6f}")
        
        if is_coint:
            # Test stationarity of the spread
            strategy = PairsTradingStrategy(stock1, stock2, start_date, end_date)
            strategy.fetch_data()
            spread = strategy.calculate_spread()
            is_stationary, adf_p = test_stationarity(spread)
            print(f"  Spread is stationary: {is_stationary} (ADF p-value: {adf_p:.6f})")
    
    print("\n" + "=" * 80)
    print("RUNNING BACKTEST ON BEST PAIR")
    print("=" * 80)
    
    # Choose a pair for detailed analysis (e.g., PEP vs KO)
    stock1, stock2 = 'PEP', 'KO'
    
    print(f"\nAnalyzing pair: {stock1} vs {stock2}")
    print(f"Period: {start_date} to {end_date}")
    print("-" * 80)
    
    # Initialize strategy
    strategy = PairsTradingStrategy(stock1, stock2, start_date, end_date)
    strategy.fetch_data()
    
    # Calculate spread and Z-score
    spread = strategy.calculate_spread()
    zscore = strategy.calculate_zscore(window=20)
    
    print(f"\nHedge ratio: {strategy.hedge_ratio:.4f}")
    print(f"Mean spread: {spread.mean():.4f}")
    print(f"Std spread: {spread.std():.4f}")
    
    # Run backtest
    backtester = Backtester(strategy, initial_capital=100000)
    results = backtester.run_backtest(entry_threshold=2.0, exit_threshold=0.5, position_size=0.5)
    
    # Calculate and display metrics
    metrics = backtester.calculate_metrics()
    
    print("\n" + "=" * 80)
    print("BACKTEST RESULTS")
    print("=" * 80)
    print(f"Total Return: {metrics['total_return']:.2f}%")
    print(f"Annualized Return: {metrics['annualized_return']:.2f}%")
    print(f"Sharpe Ratio: {metrics['sharpe_ratio']:.2f}")
    print(f"Maximum Drawdown: {metrics['max_drawdown']:.2f}%")
    print(f"Win Rate: {metrics['win_rate']:.2f}%")
    print(f"Total Trades: {metrics['total_trades']:.0f}")
    print("=" * 80)
    
    # Plot results
    print("\nGenerating plots...")
    backtester.plot_results(save_path='pairs_trading_results.png')
    
    print("\nBacktest complete!")
