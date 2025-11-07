"""
Unit tests for the pairs trading bot

Run with: python -m pytest test_pairs_trading.py -v
Or: python test_pairs_trading.py
"""

import unittest
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from pairs_trading_bot import (
    PairsFinder, 
    PairsTradingStrategy, 
    Backtester, 
    test_stationarity
)


class TestPairsFinder(unittest.TestCase):
    """Test the PairsFinder class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.tickers = ['AAPL', 'MSFT']
        self.start_date = '2023-01-01'
        self.end_date = '2023-12-31'
        
    def test_initialization(self):
        """Test PairsFinder initialization."""
        finder = PairsFinder(self.tickers, self.start_date, self.end_date)
        self.assertEqual(finder.tickers, self.tickers)
        self.assertEqual(finder.start_date, self.start_date)
        self.assertEqual(finder.end_date, self.end_date)
        self.assertIsNone(finder.price_data)


class TestPairsTradingStrategy(unittest.TestCase):
    """Test the PairsTradingStrategy class with synthetic data."""
    
    def setUp(self):
        """Set up test fixtures with synthetic cointegrated data."""
        # Generate synthetic cointegrated pair
        np.random.seed(42)
        n_days = 100
        
        # Create dates
        start_date = datetime.now() - timedelta(days=n_days)
        dates = pd.date_range(start=start_date, periods=n_days, freq='D')
        
        # Generate cointegrated series
        common_trend = np.cumsum(np.random.randn(n_days) * 0.01)
        noise1 = np.cumsum(np.random.randn(n_days) * 0.005)
        noise2 = np.cumsum(np.random.randn(n_days) * 0.005)
        
        stock1 = 100 * np.exp(common_trend + noise1)
        stock2 = 100 * np.exp(common_trend + noise2)
        
        self.synthetic_data = pd.DataFrame({
            'STOCK_A': stock1,
            'STOCK_B': stock2
        }, index=dates)
        
        # Create strategy instance
        self.strategy = PairsTradingStrategy('STOCK_A', 'STOCK_B', 
                                            dates[0].strftime('%Y-%m-%d'),
                                            dates[-1].strftime('%Y-%m-%d'))
        self.strategy.price_data = self.synthetic_data
        
    def test_initialization(self):
        """Test strategy initialization."""
        self.assertEqual(self.strategy.stock1, 'STOCK_A')
        self.assertEqual(self.strategy.stock2, 'STOCK_B')
        
    def test_calculate_spread(self):
        """Test spread calculation."""
        spread = self.strategy.calculate_spread()
        
        # Check that spread is calculated
        self.assertIsNotNone(spread)
        self.assertEqual(len(spread), len(self.synthetic_data))
        
        # Check that hedge ratio is calculated
        self.assertIsNotNone(self.strategy.hedge_ratio)
        self.assertIsInstance(self.strategy.hedge_ratio, (int, float))
        
        # Hedge ratio should be positive and reasonable
        self.assertGreater(self.strategy.hedge_ratio, 0)
        self.assertLess(self.strategy.hedge_ratio, 10)
        
    def test_calculate_zscore(self):
        """Test Z-score calculation."""
        zscore = self.strategy.calculate_zscore(window=20)
        
        # Check that zscore is calculated
        self.assertIsNotNone(zscore)
        self.assertEqual(len(zscore), len(self.synthetic_data))
        
        # Z-score should have mean near 0 (after warming up)
        zscore_valid = zscore.dropna()
        self.assertLess(abs(zscore_valid.mean()), 1.0)
        
    def test_generate_signals(self):
        """Test signal generation."""
        signals = self.strategy.generate_signals(entry_threshold=2.0, exit_threshold=0.5)
        
        # Check that signals DataFrame has expected columns
        expected_cols = ['price1', 'price2', 'spread', 'zscore', 'signal', 'position']
        for col in expected_cols:
            self.assertIn(col, signals.columns)
        
        # Check that signals are in valid range
        self.assertTrue(signals['signal'].isin([-1, 0, 1]).all())
        self.assertTrue(signals['position'].isin([-1, 0, 1]).all())
        
        # Check data types
        self.assertEqual(len(signals), len(self.synthetic_data))


class TestBacktester(unittest.TestCase):
    """Test the Backtester class."""
    
    def setUp(self):
        """Set up test fixtures with synthetic data."""
        # Generate synthetic cointegrated pair
        np.random.seed(42)
        n_days = 100
        
        start_date = datetime.now() - timedelta(days=n_days)
        dates = pd.date_range(start=start_date, periods=n_days, freq='D')
        
        common_trend = np.cumsum(np.random.randn(n_days) * 0.01)
        noise1 = np.cumsum(np.random.randn(n_days) * 0.005)
        noise2 = np.cumsum(np.random.randn(n_days) * 0.005)
        
        stock1 = 100 * np.exp(common_trend + noise1)
        stock2 = 100 * np.exp(common_trend + noise2)
        
        synthetic_data = pd.DataFrame({
            'STOCK_A': stock1,
            'STOCK_B': stock2
        }, index=dates)
        
        # Create strategy
        strategy = PairsTradingStrategy('STOCK_A', 'STOCK_B', 
                                       dates[0].strftime('%Y-%m-%d'),
                                       dates[-1].strftime('%Y-%m-%d'))
        strategy.price_data = synthetic_data
        
        self.backtester = Backtester(strategy, initial_capital=100000)
        
    def test_initialization(self):
        """Test backtester initialization."""
        self.assertEqual(self.backtester.initial_capital, 100000)
        self.assertIsNone(self.backtester.results)
        
    def test_run_backtest(self):
        """Test running a backtest."""
        results = self.backtester.run_backtest(entry_threshold=2.0, 
                                              exit_threshold=0.5,
                                              position_size=0.5)
        
        # Check that results are generated
        self.assertIsNotNone(results)
        
        # Check expected columns
        expected_cols = ['price1', 'price2', 'spread', 'zscore', 'signal', 
                        'position', 'returns1', 'returns2', 'strategy_returns',
                        'cumulative_returns', 'equity']
        for col in expected_cols:
            self.assertIn(col, results.columns)
        
        # Check that equity is calculated properly
        # The first few rows might be NaN due to rolling calculations
        valid_equity = results['equity'].dropna()
        self.assertGreater(len(valid_equity), 0)
        
        # Check that equity values are reasonable (not all zero)
        self.assertTrue((valid_equity != 0).any())
        
    def test_calculate_metrics(self):
        """Test performance metrics calculation."""
        # Run backtest first
        self.backtester.run_backtest()
        
        # Calculate metrics
        metrics = self.backtester.calculate_metrics()
        
        # Check that all expected metrics are present
        expected_metrics = ['total_return', 'annualized_return', 'sharpe_ratio',
                          'max_drawdown', 'win_rate', 'total_trades']
        for metric in expected_metrics:
            self.assertIn(metric, metrics)
            self.assertIsInstance(metrics[metric], (int, float))
        
        # Check metric ranges
        self.assertGreaterEqual(metrics['max_drawdown'], -100)
        self.assertLessEqual(metrics['max_drawdown'], 0)
        self.assertGreaterEqual(metrics['win_rate'], 0)
        self.assertLessEqual(metrics['win_rate'], 100)
        self.assertGreaterEqual(metrics['total_trades'], 0)
        
    def test_metrics_without_backtest(self):
        """Test that calculating metrics without running backtest raises error."""
        backtester = Backtester(self.backtester.strategy, initial_capital=100000)
        
        with self.assertRaises(ValueError):
            backtester.calculate_metrics()


class TestStationarityTest(unittest.TestCase):
    """Test the stationarity testing function."""
    
    def test_stationary_series(self):
        """Test with a stationary series (white noise)."""
        np.random.seed(42)
        stationary_series = pd.Series(np.random.randn(200))
        
        is_stationary, p_value = test_stationarity(stationary_series)
        
        # White noise should be stationary
        self.assertTrue(is_stationary)
        self.assertLess(p_value, 0.05)
        
    def test_nonstationary_series(self):
        """Test with a non-stationary series (random walk)."""
        np.random.seed(42)
        random_walk = pd.Series(np.cumsum(np.random.randn(200)))
        
        is_stationary, p_value = test_stationarity(random_walk)
        
        # Random walk should be non-stationary
        self.assertFalse(is_stationary)
        self.assertGreater(p_value, 0.05)


class TestSyntheticDataGeneration(unittest.TestCase):
    """Test synthetic data generation from demo script."""
    
    def test_synthetic_pair_properties(self):
        """Test that synthetic pairs have expected properties."""
        from demo_pairs_trading import generate_synthetic_pair
        
        synthetic_data = generate_synthetic_pair(n_days=100, seed=42)
        
        # Check shape
        self.assertEqual(len(synthetic_data), 100)
        self.assertEqual(len(synthetic_data.columns), 2)
        
        # Check column names
        self.assertIn('STOCK_A', synthetic_data.columns)
        self.assertIn('STOCK_B', synthetic_data.columns)
        
        # Check that prices are positive
        self.assertTrue((synthetic_data > 0).all().all())
        
        # Check that data is numeric
        self.assertTrue(synthetic_data.dtypes['STOCK_A'] in [np.float64, np.float32])
        self.assertTrue(synthetic_data.dtypes['STOCK_B'] in [np.float64, np.float32])


class TestEdgeCases(unittest.TestCase):
    """Test edge cases and error handling."""
    
    def test_empty_dataframe(self):
        """Test handling of empty DataFrames."""
        strategy = PairsTradingStrategy('A', 'B', '2023-01-01', '2023-12-31')
        strategy.price_data = pd.DataFrame()
        
        # Should handle empty data gracefully
        with self.assertRaises((ValueError, IndexError, KeyError)):
            strategy.calculate_spread()
    
    def test_single_data_point(self):
        """Test with minimal data."""
        dates = pd.date_range(start='2023-01-01', periods=1, freq='D')
        data = pd.DataFrame({
            'STOCK_A': [100.0],
            'STOCK_B': [100.0]
        }, index=dates)
        
        strategy = PairsTradingStrategy('STOCK_A', 'STOCK_B', '2023-01-01', '2023-01-01')
        strategy.price_data = data
        
        # Minimal data should raise errors or return invalid results
        try:
            spread = strategy.calculate_spread()
            # If it succeeds, check that spread exists
            self.assertEqual(len(spread), 1)
        except (ValueError, np.linalg.LinAlgError):
            # Expected - not enough data for regression
            pass


if __name__ == '__main__':
    # Run tests
    unittest.main(verbosity=2)
