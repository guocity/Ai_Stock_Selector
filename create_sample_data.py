import pandas as pd
import sqlite3
import numpy as np
from datetime import datetime, timedelta

def create_sample_data():
    """Create sample stock data for testing report generation"""
    
    # Sample stock information
    stocks = [
        ('000001', '平安银行'),
        ('000002', '万科A'),
        ('600000', '浦发银行'),
        ('600036', '招商银行'),
        ('000858', '五粮液')
    ]
    
    # Connect to database
    conn = sqlite3.connect('stock_data.db')
    cursor = conn.cursor()
    
    # Insert stock info
    for stock_code, stock_name in stocks:
        cursor.execute('INSERT OR IGNORE INTO stock_info (stock_code, stock_name) VALUES (?, ?)', 
                      (stock_code, stock_name))
    
    # Generate sample price data for each stock
    end_date = datetime.now()
    start_date = end_date - timedelta(days=60)
    
    for stock_code, stock_name in stocks:
        dates = pd.date_range(start=start_date, end=end_date, freq='D')
        dates = [d for d in dates if d.weekday() < 5]  # Only weekdays
        
        # Generate realistic stock price data
        base_price = np.random.uniform(10, 100)
        prices = []
        
        for i, date in enumerate(dates):
            # Random walk with slight upward trend
            if i == 0:
                price = base_price
            else:
                change = np.random.normal(0, 0.02)  # 2% daily volatility
                price = prices[-1] * (1 + change)
                price = max(price, 0.01)  # Ensure positive price
            prices.append(price)
        
        # Generate OHLC data
        for i, (date, close_price) in enumerate(zip(dates, prices)):
            high = close_price * np.random.uniform(1.0, 1.05)
            low = close_price * np.random.uniform(0.95, 1.0)
            open_price = np.random.uniform(low, high)
            
            volume = np.random.randint(1000000, 10000000)
            amount = volume * close_price
            
            change_pct = 0 if i == 0 else (close_price - prices[i-1]) / prices[i-1] * 100
            change_amount = 0 if i == 0 else close_price - prices[i-1]
            amplitude = (high - low) / close_price * 100
            turnover_rate = np.random.uniform(0.5, 5.0)
            
            # Insert into database
            cursor.execute('''
                INSERT OR REPLACE INTO daily_quote 
                (stock_code, trade_date, open_price, close_price, high_price, low_price, 
                 volume, amount, amplitude, change_percent, change_amount, turnover_rate)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (stock_code, date.strftime('%Y-%m-%d'), open_price, close_price, 
                  high, low, volume, amount, amplitude, change_pct, change_amount, turnover_rate))
        
        # Also create CSV file
        data = {
            '日期': [d.strftime('%Y-%m-%d') for d in dates],
            '开盘': [prices[i] * np.random.uniform(0.98, 1.02) for i in range(len(dates))],
            '收盘': prices,
            '最高': [prices[i] * np.random.uniform(1.0, 1.05) for i in range(len(dates))],
            '最低': [prices[i] * np.random.uniform(0.95, 1.0) for i in range(len(dates))],
            '成交量': [np.random.randint(1000000, 10000000) for _ in dates],
            '成交额': [prices[i] * np.random.randint(1000000, 10000000) for i in range(len(dates))],
            '振幅': [np.random.uniform(1, 8) for _ in dates],
            '涨跌幅': [np.random.uniform(-5, 5) for _ in dates],
            '涨跌额': [np.random.uniform(-2, 2) for _ in dates],
            '换手率': [np.random.uniform(0.5, 5) for _ in dates]
        }
        
        df = pd.DataFrame(data)
        df.to_csv(f'data/{stock_code}_{stock_name}.csv', index=False)
        print(f'Created sample data for {stock_name}({stock_code})')
    
    conn.commit()
    conn.close()
    print('Sample data creation complete!')

if __name__ == "__main__":
    create_sample_data()
