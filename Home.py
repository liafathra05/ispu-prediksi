import streamlit as st
import os
import sys

sys.path.append(os.path.dirname(__file__))

st.set_page_config(
    page_title="Prediksi ISPU Jakarta",
    page_icon="🌫️",
    layout="wide"
)

from utils.sidebar import tampilkan_sidebar
tampilkan_sidebar()

st.title("🌫️ Prediksi ISPU DKI Jakarta")
st.markdown("""
Aplikasi prediksi **Indeks Standar Pencemar Udara (ISPU)** DKI Jakarta
menggunakan model **Hybrid ARIMA-Bidirectional LSTM**.
""")

MODEL_ARIMA_PATH = "models/arima_model.pkl"
MODEL_LSTM_PATH = "models/lstm_model.h5"

if 'models_loaded' not in st.session_state:
    from utils.train_model import (
        load_and_preprocess, train_arima,
        train_bilstm, load_all_models
    )

    # Load & preprocess data
    with st.spinner("📂 Memuat dan memproses data..."):
        df, ispu_series, numeric_cols = load_and_preprocess()
        st.session_state['df_processed'] = df
        st.session_state['ispu_series'] = ispu_series
        st.session_state['numeric_cols'] = numeric_cols

    # Cek apakah model sudah tersimpan
    if os.path.exists(MODEL_ARIMA_PATH) and os.path.exists(MODEL_LSTM_PATH):
        with st.spinner("⚙️ Memuat model yang sudah tersimpan..."):
            result = load_all_models(ispu_series)
        st.success("✅ Model berhasil dimuat!")
    else:
        # Training dari awal
        import pandas as pd

        train_size = int(len(ispu_series) * 0.8)
        train_data = ispu_series[:train_size]
        test_data = ispu_series[train_size:]

        with st.spinner("📉 Melatih model ARIMA... (1-3 menit)"):
            model_arima = train_arima(train_data)

        arima_pred = model_arima.predict(n_periods=len(test_data))
        arima_predictions = pd.Series(arima_pred, index=test_data.index)
        arima_residuals_train = train_data - model_arima.predict_in_sample()
        arima_residuals_test = test_data - arima_predictions

        with st.spinner("🧠 Melatih model BiLSTM... (3-5 menit)"):
            model_lstm, scaler = train_bilstm(
                arima_residuals_train, arima_residuals_test,
                train_data, test_data, arima_predictions
            )

        with st.spinner("✅ Memuat hasil training..."):
            result = load_all_models(ispu_series)
        st.success("✅ Training selesai dan model tersimpan!")

    # Simpan semua ke session state
    for key, value in result.items():
        st.session_state[key] = value
    st.session_state['models_loaded'] = True
    st.rerun()

# Tampilan setelah semua siap
st.success("✅ Sistem siap digunakan!")

col1, col2, col3 = st.columns(3)
col1.metric("Total Data", len(st.session_state['ispu_series']))
col2.metric("RMSE ARIMA",
            f"{st.session_state['arima_metrics']['RMSE']:.4f}")
col3.metric("RMSE Hybrid",
            f"{st.session_state['hybrid_metrics']['RMSE']:.4f}")

st.markdown("""
### 📌 Panduan Navigasi
Gunakan sidebar kiri untuk navigasi:
- 📊 **EDA** — Lihat visualisasi dan statistik data
- 📉 **ARIMA** — Lihat hasil model ARIMA
- 🧠 **BiLSTM** — Lihat hasil model BiLSTM
- 🏆 **Evaluasi** — Bandingkan semua model
- 🔮 **Prediksi** — Prediksi ISPU hari ke depan
""")