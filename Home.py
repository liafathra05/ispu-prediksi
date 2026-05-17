import streamlit as st
import pandas as pd
import os

st.set_page_config(
    page_title="Prediksi ISPU Jakarta",
    page_icon="🌫️",
    layout="wide"
)

import sys
sys.path.append('.')
from utils.sidebar import tampilkan_sidebar
tampilkan_sidebar()

# ===================== HALAMAN DASHBOARD =====================
st.markdown("""
    <style>
        .dashboard-container {
            text-align: center;
            padding: 20px;
        }
        .icon-container {
            font-size: 80px;
            margin-bottom: 10px;
        }
        .judul-skripsi {
            font-size: 20px;
            font-weight: bold;
            color: #0f3460;
            text-align: center;
            margin: 20px auto;
            max-width: 800px;
            line-height: 1.6;
            padding: 20px;
            border: 2px solid #0f3460;
            border-radius: 10px;
            background-color: #f0f4ff;
        }
        .identitas-box {
            background-color: #f8f9fa;
            border-radius: 10px;
            padding: 25px;
            margin: 20px auto;
            max-width: 600px;
            border-left: 5px solid #0f3460;
            text-align: left;
        }
        .identitas-row {
            margin-bottom: 10px;
            font-size: 16px;
        }
        .identitas-label {
            font-weight: bold;
            color: #0f3460;
        }
        .divider {
            margin: 30px auto;
            max-width: 600px;
            border: 1px solid #dee2e6;
        }
    </style>
""", unsafe_allow_html=True)

# Judul skripsi
st.markdown("""
    <div class="judul-skripsi">
        PREDIKSI INDEKS STANDAR PENCEMAR UDARA DI DKI JAKARTA 
        MENGGUNAKAN METODE HYBRID 
        <i>AUTOREGRESSIVE INTEGRATED MOVING AVERAGE</i> (ARIMA) 
        DAN <i>BIDIRECTIONAL LSTM</i>
    </div>
""", unsafe_allow_html=True)

# Identitas
st.markdown("""
    <div class="identitas-box">
        <div class="identitas-row">
            <span class="identitas-label">Nama</span><br>
            Liafathra
        </div>
        <div class="identitas-row">
            <span class="identitas-label">NIM</span><br>
            4611422128
        </div>
        <div class="identitas-row">
            <span class="identitas-label">Program Studi</span><br>
            Teknik Informatika
        </div>
        <div class="identitas-row">
            <span class="identitas-label">Fakultas</span><br>
            Fakultas Matematika dan Ilmu Pengetahuan Alam
        </div>
        <div class="identitas-row">
            <span class="identitas-label">Universitas</span><br>
            Universitas Negeri Semarang
        </div>
    </div>
""", unsafe_allow_html=True)

st.markdown("<hr class='divider'>", unsafe_allow_html=True)

# ===================== LOAD DATA (BACKGROUND) =====================
if 'data_loaded' not in st.session_state:
    with st.spinner("📂 Memuat data..."):
        ispu_series = pd.read_csv('data/ispu_series.csv',
                                   index_col=0, parse_dates=True)['nilai_ispu']
        arima_df = pd.read_csv('data/arima_predictions.csv',
                                parse_dates=['tanggal'])
        hybrid_df = pd.read_csv('data/hybrid_predictions.csv',
                                 parse_dates=['tanggal'])
        metrics_df = pd.read_csv('data/metrics.csv')

        st.session_state['ispu_series'] = ispu_series
        st.session_state['arima_df'] = arima_df
        st.session_state['hybrid_df'] = hybrid_df
        st.session_state['metrics_df'] = metrics_df

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

# Metrik
st.subheader("📊 Performa Model")
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
