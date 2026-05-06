import pandas as pd
import numpy as np
import pickle
import os
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_absolute_error, mean_squared_error

# Path file
MODEL_ARIMA_PATH = "models/arima_model.pkl"
MODEL_LSTM_PATH = "models/lstm_model.h5"
SCALER_PATH = "models/scaler.pkl"
META_PATH = "models/lstm_meta.pkl"
DATA_PATH = "data/data-ispu-jakarta.xlsx"

# Parameter BiLSTM (sama dengan Google Colab)
N_STEPS = 15
EPOCHS = 150
UNITS = 75
UNITS_SECOND = 37

def load_and_preprocess():
    df = pd.read_excel(DATA_PATH)
    df['tanggal_lengkap'] = (
        df['tahun'].astype(str) + '-' +
        df['bulan'].astype(str) + '-' +
        df['tanggal'].astype(str)
    )
    df['tanggal_lengkap'] = pd.to_datetime(df['tanggal_lengkap'], errors='coerce')
    df.dropna(subset=['tanggal_lengkap'], inplace=True)
    df = df.set_index('tanggal_lengkap')
    df = df.drop(columns=['Unnamed: 13', 'Unnamed: 14'], errors='ignore')

    numeric_cols = ['pm_sepuluh', 'pm_duakomalima', 'sulfur_dioksida',
                    'karbon_monoksida', 'ozon', 'nitrogen_dioksida', 'max']
    for col in numeric_cols:
        if col in df.columns:
            df[col] = df[col].interpolate(method='linear').ffill()

    ispu_series = df.groupby('tanggal_lengkap')['max'].max().sort_index()
    return df, ispu_series, numeric_cols


def train_arima(train_data):
    import pmdarima as pm
    model_arima = pm.auto_arima(
        train_data, seasonal=False,
        suppress_warnings=True, stepwise=True,
        trace=False, error_action='ignore',
        max_p=5, max_d=2, max_q=5
    )
    os.makedirs("models", exist_ok=True)
    with open(MODEL_ARIMA_PATH, 'wb') as f:
        pickle.dump(model_arima, f)
    return model_arima


def train_bilstm(arima_residuals_train, arima_residuals_test,
                 train_data, test_data, arima_predictions):
    from tensorflow.keras.models import Sequential
    from tensorflow.keras.layers import Bidirectional, LSTM, Dense, Dropout, Input

    scaler = MinMaxScaler()
    train_scaled = scaler.fit_transform(
        arima_residuals_train.values.reshape(-1, 1))
    test_scaled = scaler.transform(
        arima_residuals_test.values.reshape(-1, 1))

    def create_sequences(data, n_steps):
        X, y = [], []
        for i in range(len(data) - n_steps):
            X.append(data[i:i + n_steps])
            y.append(data[i + n_steps])
        return np.array(X), np.array(y)

    X_train, y_train = create_sequences(train_scaled, N_STEPS)
    X_test, y_test = create_sequences(test_scaled, N_STEPS)

    # Arsitektur sama persis dengan Google Colab
    model_lstm = Sequential()
    model_lstm.add(Input(shape=(N_STEPS, 1)))
    model_lstm.add(Bidirectional(LSTM(UNITS, activation='relu',
                                      return_sequences=True)))
    model_lstm.add(Bidirectional(LSTM(UNITS_SECOND, activation='relu',
                                      return_sequences=False)))
    model_lstm.add(Dropout(0.3))
    model_lstm.add(Dense(1))

    model_lstm.compile(optimizer='adam', loss='mean_squared_error')
    model_lstm.fit(X_train, y_train, epochs=EPOCHS, batch_size=32,
                   verbose=0, validation_data=(X_test, y_test))

    os.makedirs("models", exist_ok=True)
    model_lstm.save(MODEL_LSTM_PATH)
    with open(SCALER_PATH, 'wb') as f:
        pickle.dump(scaler, f)
    with open(META_PATH, 'wb') as f:
        pickle.dump({'n_steps': N_STEPS}, f)

    return model_lstm, scaler


def load_all_models(ispu_series):
    with open(MODEL_ARIMA_PATH, 'rb') as f:
        model_arima = pickle.load(f)

    from tensorflow.keras.models import load_model
    model_lstm = load_model(MODEL_LSTM_PATH)

    with open(SCALER_PATH, 'rb') as f:
        scaler = pickle.load(f)
    with open(META_PATH, 'rb') as f:
        meta = pickle.load(f)

    n_steps = meta['n_steps']
    train_size = int(len(ispu_series) * 0.8)
    train_data = ispu_series[:train_size]
    test_data = ispu_series[train_size:]

    arima_pred_values = model_arima.predict(n_periods=len(test_data))
    arima_predictions = pd.Series(arima_pred_values, index=test_data.index)

    arima_residuals_test = test_data - arima_predictions
    test_scaled = scaler.transform(
        arima_residuals_test.values.reshape(-1, 1))

    def create_sequences(data, n_steps):
        X, y = [], []
        for i in range(len(data) - n_steps):
            X.append(data[i:i + n_steps])
            y.append(data[i + n_steps])
        return np.array(X), np.array(y)

    X_test, _ = create_sequences(test_scaled, n_steps)
    lstm_pred_scaled = model_lstm.predict(X_test, verbose=0)
    lstm_pred = scaler.inverse_transform(lstm_pred_scaled).flatten()

    lstm_series = pd.Series(
        lstm_pred,
        index=test_data.index[n_steps:n_steps + len(lstm_pred)]
    )
    hybrid_predictions = (
        arima_predictions[n_steps:n_steps + len(lstm_pred)] + lstm_series
    )
    actual_aligned = test_data[n_steps:n_steps + len(hybrid_predictions)]

    arima_mae = mean_absolute_error(test_data, arima_predictions)
    arima_mse = mean_squared_error(test_data, arima_predictions)
    hybrid_mae = mean_absolute_error(actual_aligned, hybrid_predictions)
    hybrid_mse = mean_squared_error(actual_aligned, hybrid_predictions)

    return {
        'model_arima': model_arima,
        'model_lstm': model_lstm,
        'scaler': scaler,
        'n_steps': n_steps,
        'train_data': train_data,
        'test_data': test_data,
        'arima_predictions': arima_predictions,
        'hybrid_predictions': hybrid_predictions,
        'actual_aligned': actual_aligned,
        'arima_metrics': {
            'MAE': arima_mae,
            'MSE': arima_mse,
            'RMSE': np.sqrt(arima_mse)
        },
        'hybrid_metrics': {
            'MAE': hybrid_mae,
            'MSE': hybrid_mse,
            'RMSE': np.sqrt(hybrid_mse)
        }
    }