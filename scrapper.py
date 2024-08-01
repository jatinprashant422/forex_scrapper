import sqlite3
import pandas as pd
from datetime import datetime
from yfinance import Ticker

def fetch_forex_data(ticker_symbol, start_date, end_date):
    """
    Fetch forex data from Yahoo Finance for a given ticker symbol between start and end dates.
    
    Args:
        ticker_symbol (str): The ticker symbol for the currency pair.
        start_date (str): The start date for the data (format: YYYY-MM-DD).
        end_date (str): The end date for the data (format: YYYY-MM-DD).
        
    Returns:
        pd.DataFrame: DataFrame containing the fetched forex data.
    """
    # Use yfinance to fetch data
    ticker = Ticker(ticker_symbol)
    data = ticker.history(start=start_date, end=end_date)
    return data

def save_to_db(data, db_path='forex_data.db'):
    """
    Save the fetched forex data to an SQLite database.
    
    Args:
        data (pd.DataFrame): The data to be saved.
        db_path (str): Path to the SQLite database file.
    """
    # Connect to SQLite database
    conn = sqlite3.connect(db_path)
    # Convert data to DataFrame
    df = pd.DataFrame(data)
    df.reset_index(inplace=True)
    df.columns = ['Date', 'Open', 'High', 'Low', 'Close', 'Volume', 'Dividends', 'Stock Splits']
    # Save data to the database
    df.to_sql('historical_data', conn, if_exists='replace', index=False)
    conn.close()

def scrape_data():
    """
    Function to fetch forex data for predefined currency pairs and save to the database.
    """
    # Define the parameters for the data you want to scrape
    pairs = [
        ('GBPUSD=X', '2021-01-01', '2024-08-01'),
        ('AEDUSD=X', '2021-01-01', '2024-08-01')
    ]
    
    for symbol, start_date, end_date in pairs:
        print(f"Fetching data for {symbol} from {start_date} to {end_date}...")
        data = fetch_forex_data(symbol, start_date, end_date)
        save_to_db(data)
        print(f"Data for {symbol} has been successfully fetched and stored.")

if __name__ == '__main__':
    scrape_data()

