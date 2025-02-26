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

1. Clone this repository or download the files

2. Create and activate a virtual environment (recommended):
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use: venv\Scripts\activate
   ```

3. Install the required packages:
   ```
   pip install flask openalgo pandas
   ```

## Project Structure

```
stock-market-dashboard/
├── app.py                 # Flask application
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

The application uses the following API key for OpenAlgo API:
```
93ae406f21d54ad32e79c98ba1174dcaa22f63ab92fc9b9615c9cd4ce2d2cdf2
```

Make sure this key is valid for your OpenAlgo API instance.