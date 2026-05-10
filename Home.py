import streamlit as st
import pandas as pd
import os
from utils.sidebar import tampilkan_sidebar
tampilkan_sidebar()

st.set_page_config(
    page_title="Prediksi ISPU Jakarta",
    page_icon="🌫️",
    layout="wide"
)

st.title("🌫️ Prediksi ISPU DKI Jakarta")
st.markdown("""
Aplikasi prediksi **Indeks Standar Pencemar Udara (ISPU)** DKI Jakarta
menggunakan model **Hybrid ARIMA-Bidirectional LSTM**.
""")

if 'data_loaded' not in st.session_state:
    with st.spinner("📂 Memuat data..."):
        # Load semua CSV
        ispu_series = pd.read_csv('data/ispu_series.csv',
                                   index_col=0, parse_dates=True)['nilai_ispu']
        arima_df = pd.read_csv('data/arima_predictions.csv',
                                parse_dates=['tanggal'])
        hybrid_df = pd.read_csv('data/hybrid_predictions.csv',
                                 parse_dates=['tanggal'])
        metrics_df = pd.read_csv('data/metrics.csv')

        # Simpan ke session state
        st.session_state['ispu_series'] = ispu_series
        st.session_state['arima_df'] = arima_df
        st.session_state['hybrid_df'] = hybrid_df
        st.session_state['metrics_df'] = metrics_df

        # Metrik
        arima_row = metrics_df[metrics_df['Model'] == 'ARIMA'].iloc[0]
        hybrid_row = metrics_df[metrics_df['Model'] == 'Hybrid ARIMA-BiLSTM'].iloc[0]

        st.session_state['arima_metrics'] = {
            'MAE': arima_row['MAE'],
            'MSE': arima_row['MSE'],
            'RMSE': arima_row['RMSE']
        }
        st.session_state['hybrid_metrics'] = {
            'MAE': hybrid_row['MAE'],
            'MSE': hybrid_row['MSE'],
            'RMSE': hybrid_row['RMSE']
        }
        st.session_state['data_loaded'] = True

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
- 📊 **EDA** - Lihat visualisasi dan statistik data
- 📉 **ARIMA** - Lihat hasil model ARIMA
- 🧠 **BiLSTM** - Lihat hasil model BiLSTM
- 🏆 **Evaluasi** - Bandingkan semua model
- 🔮 **Prediksi** - Prediksi ISPU hari ke depan
""")
