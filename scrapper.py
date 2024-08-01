import sqlite3
import pandas as pd
from datetime import datetime
from yfinance import Ticker

def fetch_forex_data(ticker_symbol, start_date, end_date):
    # Use yfinance to fetch data
    ticker = Ticker(ticker_symbol)
    data = ticker.history(start=start_date, end=end_date)
    return data

def save_to_db(data, db_path='forex_data.db'):
    # Connect to SQLite database
    conn = sqlite3.connect(db_path)
    # Convert data to DataFrame
    df = pd.DataFrame(data)
    df.reset_index(inplace=True)
    df.columns = ['Date', 'Open', 'High', 'Low', 'Close', 'Volume', 'Dividends', 'Stock Splits']
    # Save data to the database
    df.to_sql('historical_data', conn, if_exists='replace', index=False)
    conn.close()

if __name__ == '__main__':
    # Define the parameters for the data you want to scrape
    symbol = 'EURUSD=X'  # Change this to your desired currency pair
    start_date = '2021-01-01'
    end_date = '2024-08-01'
    
    # Fetch and save data
    data = fetch_forex_data(symbol, start_date, end_date)
    save_to_db(data)
    print("Data has been successfully fetched and stored.")
