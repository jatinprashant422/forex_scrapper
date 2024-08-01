from flask import Flask, request, jsonify
import sqlite3
import pandas as pd
import os
from datetime import datetime

app = Flask(__name__)

def get_date_range(period):
    """
    Get the start and end dates based on the specified period.

    Args:
        period (str): The time period for the data. Supported values: '1W', '1M', '3M', '6M', '1Y'.

    Returns:
        tuple: Start date and end date in 'YYYY-MM-DD' format. If period is invalid, returns (None, None).
    """
    now = datetime.now()
    if period == '1W':
        start_date = now - pd.DateOffset(weeks=1)
    elif period == '1M':
        start_date = now - pd.DateOffset(months=1)
    elif period == '3M':
        start_date = now - pd.DateOffset(months=3)
    elif period == '6M':
        start_date = now - pd.DateOffset(months=6)
    elif period == '1Y':
        start_date = now - pd.DateOffset(years=1)
    else:
        return None, None
    return start_date.strftime('%Y-%m-%d'), now.strftime('%Y-%m-%d')

@app.route('/')
def index():
    """
    Base route to confirm the API is live.
    """
    return "Forex Scraper API is live!"

@app.route('/api/forex-data', methods=['POST'])
def forex_data():
    """
    API endpoint to get historical forex data based on the specified parameters.

    Request JSON format:
    {
        "from": "USD",
        "to": "EUR",
        "period": "1M"
    }

    Returns:
        JSON: The historical forex data in JSON format or an error message.

    Possible responses:
        - 200 OK: If data is found and successfully returned.
        - 400 Bad Request: If the request is missing required parameters or if the period is invalid.
        - 404 Not Found: If no data is found for the specified parameters.
        - 500 Internal Server Error: If an unexpected error occurs.
    """
    try:
        # Parse JSON data from the request
        data = request.get_json()
        from_currency = data.get('from')
        to_currency = data.get('to')
        period = data.get('period')

        # Validate the input parameters
        if not from_currency or not to_currency or not period:
            return jsonify({'error': 'Invalid parameters'}), 400

        start_date, end_date = get_date_range(period)
        if start_date is None or end_date is None:
            return jsonify({'error': 'Invalid period'}), 400

        # Connect to the SQLite database and query data
        conn = sqlite3.connect('forex_data.db')
        query = f'''
        SELECT * FROM historical_data
        WHERE Date BETWEEN "{start_date}" AND "{end_date}"
        '''
        df = pd.read_sql_query(query, conn)
        conn.close()

        # Filter data by the date range
        filtered_df = df[(df['Date'] >= start_date) & (df['Date'] <= end_date)]
        result = filtered_df.to_dict(orient='records')
        
        if not result:
            return jsonify({'error': 'No data found for the specified parameters'}), 404

        return jsonify(result)

    except Exception as e:
        # Log the exception and return a server error response
        print(f"Exception occurred: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
