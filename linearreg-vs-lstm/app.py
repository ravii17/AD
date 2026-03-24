from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from sklearn.linear_model import LinearRegression
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Input
import os

app = Flask(__name__)
CORS(app)

# Configuration
DATA_PATH = "All_Stocks_Data.csv"
symbol = "20MICRONS"
seq_length = 20

# Global models and scalers
scaler = MinMaxScaler(feature_range=(0, 1))
lr_model = LinearRegression()
lstm_model = None

def load_and_train():
    global lstm_model, lr_model, scaler
    
    if not os.path.exists(DATA_PATH):
        print(f"Error: {DATA_PATH} not found.")
        return False
        
    # 1. Load Data
    df = pd.read_csv(DATA_PATH)
    df = df[df['symbol'] == symbol]
    df = df.drop(columns=['Unnamed: 0', 'symbol'], errors='ignore')
    
    # 2. Preprocess
    df = df.T
    df.index = pd.to_datetime(df.index)
    df.columns = ['Close']
    df.sort_index(inplace=True)
    
    # 3. Scale
    df_scaled = scaler.fit_transform(df)
    
    # 4. Train Linear Regression
    X_train_lr = np.array(range(len(df_scaled))).reshape(-1, 1)
    y_train_lr = df_scaled.flatten()
    lr_model.fit(X_train_lr, y_train_lr)
    
    # 5. Train LSTM
    def create_sequences(data, seq_length=10):
        X, y = [], []
        for i in range(len(data)-seq_length):
            X.append(data[i:i+seq_length])
            y.append(data[i+seq_length])
        return np.array(X), np.array(y)

    X_lstm, y_lstm = create_sequences(df_scaled, seq_length)
    X_lstm = X_lstm.reshape(X_lstm.shape[0], seq_length, 1)

    lstm_model = Sequential()
    lstm_model.add(Input(shape=(seq_length, 1)))
    lstm_model.add(LSTM(50, return_sequences=True))
    lstm_model.add(LSTM(50))
    lstm_model.add(Dense(25))
    lstm_model.add(Dense(1))
    lstm_model.compile(optimizer="adam", loss="mean_squared_error")
    lstm_model.fit(X_lstm, y_lstm, epochs=30, batch_size=16, verbose=0)
    
    print("Models trained successfully.")
    return True

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/data', methods=['GET'])
def get_data():
    if not os.path.exists(DATA_PATH):
        return jsonify({"error": "Data file not found"}), 404
        
    df = pd.read_csv(DATA_PATH)
    df = df[df['symbol'] == symbol]
    df = df.drop(columns=['Unnamed: 0', 'symbol'], errors='ignore')
    df = df.T
    df.index = pd.to_datetime(df.index)
    df.columns = ['Close']
    df.sort_index(inplace=True)
    
    # Return as list of dicts {date, value}
    result = []
    for date, row in df.iterrows():
        result.append({
            "date": date.strftime('%Y-%m-%d'),
            "value": float(row['Close'])
        })
    return jsonify(result)

@app.route('/api/predict', methods=['POST'])
def predict():
    req_data = request.get_json()
    days = int(req_data.get('days', 30))
    
    # Reload and Scale
    df = pd.read_csv(DATA_PATH)
    df = df[df['symbol'] == symbol]
    df = df.drop(columns=['Unnamed: 0', 'symbol'], errors='ignore').T
    df.index = pd.to_datetime(df.index)
    df.sort_index(inplace=True)
    df_scaled = scaler.transform(df)
    
    current_len = len(df_scaled)
    
    # 1. Linear Regression Prediction
    X_future = np.array(range(current_len, current_len + days)).reshape(-1, 1)
    lr_pred_scaled = lr_model.predict(X_future)
    lr_predictions = scaler.inverse_transform(lr_pred_scaled.reshape(-1, 1)).flatten()
    
    # 2. LSTM Prediction (Iterative)
    lstm_predictions = []
    last_sequence = df_scaled[-seq_length:]
    
    for _ in range(days):
        pred_scaled = lstm_model.predict(last_sequence.reshape(1, seq_length, 1), verbose=0)
        lstm_predictions.append(float(scaler.inverse_transform(pred_scaled)[0][0]))
        # Update sequence
        last_sequence = np.append(last_sequence[1:], pred_scaled, axis=0)
        
    # Create date list for future
    last_date = df.index[-1]
    future_dates = [(last_date + pd.Timedelta(days=i+1)).strftime('%Y-%m-%d') for i in range(days)]
    
    return jsonify({
        "dates": future_dates,
        "lr": lr_predictions.tolist(),
        "lstm": lstm_predictions
    })

if __name__ == '__main__':
    if load_and_train():
        app.run(debug=True, port=5001)
