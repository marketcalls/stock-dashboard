import os
from flask import Flask, render_template, request, jsonify
from openalgo import api
import pandas as pd
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

def get_api_client():
    # Get the API key from environment variables loaded from .env
    api_key = os.environ.get('OPENALGO_API_KEY', '')
    api_host = os.environ.get('OPENALGO_API_HOST', 'http://127.0.0.1:5000')
    
    if not api_key:
        print("WARNING: OPENALGO_API_KEY environment variable not set. Check your .env file.")
    
    return api(api_key=api_key, host=api_host)

def calculate_ema(data, period=20):
    """Calculate Exponential Moving Average"""
    return data.ewm(span=period, adjust=False).mean()

def calculate_rsi(data, period=14):
    """Calculate Relative Strength Index"""
    delta = data.diff()
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)
    
    avg_gain = gain.rolling(window=period).mean()
    avg_loss = loss.rolling(window=period).mean()
    
    # For periods > first period
    for i in range(period, len(gain)):
        avg_gain.iloc[i] = (avg_gain.iloc[i-1] * (period-1) + gain.iloc[i]) / period
        avg_loss.iloc[i] = (avg_loss.iloc[i-1] * (period-1) + loss.iloc[i]) / period
    
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

def fetch_openalgo_data(symbol, exchange, interval, ema_period=20, rsi_period=14):
    # Determine start and end dates based on interval
    end_date = datetime.now().strftime('%Y-%m-%d')
    
    if interval in ['1m', '5m', '15m']:
        # For smaller timeframes, get a week of data
        start_date = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
    elif interval in ['30m', '1h']:
        # For hourly data, get a month
        start_date = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
    else:
        # For daily and above, get more history
        start_date = (datetime.now() - timedelta(days=365)).strftime('%Y-%m-%d')
    
    # Standardize interval format for OpenAlgo
    if interval == '1m': openalgo_interval = '1m'
    elif interval == '2m': openalgo_interval = '2m'
    elif interval == '3m': openalgo_interval = '3m'
    elif interval == '5m': openalgo_interval = '5m'
    elif interval == '10m': openalgo_interval = '10m'
    elif interval == '15m': openalgo_interval = '15m'
    elif interval == '20m': openalgo_interval = '20m'
    elif interval == '30m': openalgo_interval = '30m'
    elif interval == '1h': openalgo_interval = '1h'
    elif interval == '2h': openalgo_interval = '2h'
    elif interval == '4h': openalgo_interval = '4h'
    elif interval == '1d' or interval == 'D': openalgo_interval = 'D'
    elif interval == '1wk' or interval == 'W': openalgo_interval = 'W'
    elif interval == '1mo' or interval == 'M': openalgo_interval = 'M'
    else: openalgo_interval = 'D'  # default
    
    try:
        # Get the client
        client = get_api_client()
        
        # Fetch historical data
        df = client.history(
            symbol=symbol,
            exchange=exchange,
            interval=openalgo_interval,
            start_date=start_date,
            end_date=end_date
        )
        
        # Ensure the dataframe has the necessary columns
        if df.empty:
            return [], [], []
        
        # If the index is a timestamp, reset it to a column
        if isinstance(df.index, pd.DatetimeIndex):
            df = df.reset_index()
        
        # Calculate indicators
        df['EMA'] = calculate_ema(df['close'], period=ema_period)
        df['RSI'] = calculate_rsi(df['close'], period=rsi_period)
        
        # Format data for TradingView charts
        candlestick_data = []
        for _, row in df.iterrows():
            # Convert timestamp to Unix timestamp (seconds since epoch)
            if 'timestamp' in df.columns:
                time_val = pd.Timestamp(row['timestamp']).timestamp()
            else:
                # If no timestamp column, use index
                time_val = pd.Timestamp(row.name).timestamp()
            
            candlestick_data.append({
                'time': int(time_val),
                'open': float(row['open']),
                'high': float(row['high']),
                'low': float(row['low']),
                'close': float(row['close']),
                'volume': int(row['volume'])
            })
        
        # Format EMA data
        ema_data = []
        for _, row in df.iterrows():
            if not pd.isna(row['EMA']):
                if 'timestamp' in df.columns:
                    time_val = pd.Timestamp(row['timestamp']).timestamp()
                else:
                    time_val = pd.Timestamp(row.name).timestamp()
                
                ema_data.append({
                    'time': int(time_val),
                    'value': float(row['EMA'])
                })
        
        # Format RSI data
        rsi_data = []
        for _, row in df.iterrows():
            rsi_value = 50  # Default value if RSI is NaN
            if not pd.isna(row['RSI']):
                rsi_value = float(row['RSI'])
            
            if 'timestamp' in df.columns:
                time_val = pd.Timestamp(row['timestamp']).timestamp()
            else:
                time_val = pd.Timestamp(row.name).timestamp()
            
            rsi_data.append({
                'time': int(time_val),
                'value': rsi_value
            })
        
        return candlestick_data, ema_data, rsi_data
    
    except Exception as e:
        print(f"Error fetching data: {e}")
        return [], [], []

@app.route('/')
def index():
    exchanges = ["NSE", "BSE", "MCX", "NFO", "CDS", "BFO"]
    return render_template('index.html', exchanges=exchanges)

@app.route('/charts')
def charts():
    exchanges = ["NSE", "BSE", "MCX", "NFO", "CDS", "BFO"]
    intervals = ["1m", "2m", "3m", "5m", "10m", "15m", "20m", "30m", "1h", "2h", "4h", "D", "W", "M"]
    
    # Get default values from URL parameters or use defaults
    symbol = request.args.get('symbol', 'SBIN')
    exchange = request.args.get('exchange', 'NSE')
    interval = request.args.get('interval', 'D')
    
    return render_template('charts.html', 
                          exchanges=exchanges, 
                          intervals=intervals,
                          default_symbol=symbol,
                          default_exchange=exchange,
                          default_interval=interval)

@app.route('/api/data', methods=['GET'])
def get_data():
    symbol = request.args.get('symbol', '')
    exchange = request.args.get('exchange', '')
    interval = request.args.get('interval', '1d')
    ema_period = int(request.args.get('ema_period', 20))
    rsi_period = int(request.args.get('rsi_period', 14))
    
    if not symbol or not exchange:
        return jsonify({'status': 'error', 'message': 'Symbol and exchange are required'})
    
    try:
        candlestick_data, ema_data, rsi_data = fetch_openalgo_data(
            symbol, exchange, interval, ema_period, rsi_period
        )
        
        return jsonify({
            'status': 'success',
            'data': {
                'candlestick': candlestick_data, 
                'ema': ema_data, 
                'rsi': rsi_data
            }
        })
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

@app.route('/get_quote', methods=['POST'])
def get_quote():
    symbol = request.form.get('symbol', '')
    exchange = request.form.get('exchange', '')
    
    if not symbol or not exchange:
        return jsonify({'status': 'error', 'message': 'Symbol and exchange are required'})
    
    try:
        # Get the client
        client = get_api_client()
        
        # Get the quote
        response = client.quotes(symbol=symbol, exchange=exchange)
        
        return jsonify(response)
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

if __name__ == '__main__':
    app.run(debug=True, port=5001)