# Stock Market Dashboard with TradingView Charts

A Flask-based stock market dashboard that displays TradingView-style charts using OpenAlgo API data with technical indicators like EMA and RSI.

## Features

- Real-time stock quotes from OpenAlgo API
- Interactive TradingView Lightweight Charts
- Multiple timeframes support (1m, 5m, 15m, 30m, 1h, 4h, daily, weekly, monthly)
- Technical indicators (EMA, RSI)
- Theme toggle (light/dark mode)
- Auto-update functionality
- Watchlist for quick access to previously viewed symbols

## Prerequisites

- Python 3.6+
- Flask
- OpenAlgo API client
- pandas

## Installation

1. Clone this repository or download the files:
   ```
   git clone https://github.com/marketcalls/stock-dashboard.git
   cd stock-dashboard
   ```

2. Create and activate a virtual environment (recommended):
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use: venv\Scripts\activate
   ```

3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   ```
   cp .env.sample .env
   ```
   Then edit the `.env` file and add your OpenAlgo API key and other configuration options.

## Project Structure

```
stock-market-dashboard/
├── app.py                 # Flask application
├── .env.sample            # Sample environment variables file
├── .env                   # Your actual environment variables (not committed to git)
├── requirements.txt       # Python dependencies
└── templates/
    ├── index.html         # Home page 
    └── charts.html        # TradingView charts page
```

## Running the Application

1. Make sure the OpenAlgo API server is running on `http://127.0.0.1:5000`

2. Run the Flask application:
   ```
   python app.py
   ```

3. Open your browser and navigate to `http://127.0.0.1:5001`

## Usage

1. Navigate to the Charts page
2. Enter a stock symbol (e.g., SBIN) and select the exchange (NSE, BSE, etc.)
3. Choose a timeframe from the interval dropdown
4. Adjust EMA and RSI periods if desired
5. Click "Fetch Data" to load the chart
6. Toggle between light and dark themes using the "Toggle Theme" button
7. Enable auto-update if you want the chart to refresh automatically

## Supported Intervals

The application supports all intervals provided by the OpenAlgo API:

- Minutes: 1m, 2m, 3m, 5m, 10m, 15m, 20m, 30m
- Hours: 1h, 2h, 4h
- Days: D (daily)
- Weeks: W (weekly)
- Months: M (monthly)

## Troubleshooting Common Issues

If you encounter issues with the chart library:

1. Check the browser console for errors
2. Make sure the TradingView Lightweight Charts library is loading correctly
3. Verify that the OpenAlgo API server is running
4. Check that the data format matches what the charts expect

## API Key

For security purposes, you should store your OpenAlgo API key in an environment variable or a configuration file that is not committed to version control. In the example code, replace the hardcoded API key with:

```python
import os

# Get API key from environment variable
api_key = os.environ.get('OPENALGO_API_KEY')
```

Never share your API keys in public repositories or documentation.