# =================================================================
# TIME-SERIES STOCK PRICE PREDICTION MODEL (PYTHON)
# This file simulates a backend service responsible for training a
# time-series model (e.g., ARIMA or a simple RNN) and generating
# future price predictions.
# =================================================================

import json
import random
from datetime import datetime, timedelta

def generate_mock_historical_data(ticker, days=90):
    """
    Generates a mock set of historical closing prices for a given stock ticker.
    Simulates a slight upward trend with daily noise.
    """
    data = []
    base_price = 150.00
    date = datetime.now() - timedelta(days=days)

    for i in range(days):
        # Apply a slight linear trend and random daily volatility
        price = base_price + (i * 0.15) + (random.random() - 0.5) * 2.0
        data.append({
            "date": date.strftime("%Y-%m-%d"),
            "price": round(price, 2)
        })
        date += timedelta(days=1)
    
    return data

def train_and_predict_stock_price(ticker: str, prediction_days: int) -> dict:
    """
    Simulates the machine learning workflow for stock price prediction.
    In a real application, this would use libraries like NumPy, Pandas, 
    and Scikit-learn or TensorFlow/PyTorch.
    
    Args:
        ticker: The stock ticker symbol (e.g., 'GOOG').
        prediction_days: The number of days into the future to predict.

    Returns:
        A dictionary containing historical and predicted data points, now
        including confidence intervals for the predictions.
    """
    
    # 1. Mock Data Acquisition (Fetch 90 days of history)
    historical_data = generate_mock_historical_data(ticker, days=90)
    
    # 2. Mock Model Training (Simulated)
    # The 'model' learns the upward trend and volatility.
    latest_price = historical_data[-1]['price']
    
    # 3. Generate Predictions
    predicted_prices = []
    current_price = latest_price

    for i in range(1, prediction_days + 1):
        # Simulate price movement based on last price + random walk + trend
        trend = (random.random() * 0.5) + 0.1 # Small positive trend
        noise = (random.random() - 0.5) * 1.5  # Random daily noise
        
        current_price = current_price * (1 + (trend + noise) / 100)
        
        # Ensure prices stay reasonable
        if current_price < 50: current_price = 50 

        # --- NEW FEATURE: Confidence Interval ---
        # Base confidence multiplier starts small (0.5%) and increases slightly (0.1% per day)
        # The further out the prediction, the wider the interval, reflecting higher uncertainty.
        confidence_multiplier = 0.005 + (i * 0.001) 
        
        lower_bound = current_price * (1 - confidence_multiplier)
        upper_bound = current_price * (1 + confidence_multiplier)
        # --- END NEW FEATURE ---
        
        future_date = datetime.now() + timedelta(days=i)
        
        predicted_prices.append({
            "date": future_date.strftime("%Y-%m-%d"),
            "price": round(current_price, 2),
            "lower_bound": round(lower_bound, 2),
            "upper_bound": round(upper_bound, 2)
        })
    
    # 4. Compile Results
    results = {
        "ticker": ticker,
        "latest_price": latest_price,
        "historical_data": historical_data,
        "predicted_data": predicted_prices
    }

    print(f"Prediction complete for {ticker}. Predicted {prediction_days} days into the future.")
    return results

if __name__ == "__main__":
    # Example usage: Predict 14 days of 'TSLA' price movements
    output = train_and_predict_stock_price("TSLA", 14)
    
    # In a real API endpoint, this JSON would be sent back to the web application
    print(json.dumps(output, indent=4))

# Example usage function call (used by the HTML front-end simulator)
# Note: Since the web application runs JavaScript, it must simulate calling this
# Python function via a mock API endpoint.
# simulate_api_call('GOOG', 30)
