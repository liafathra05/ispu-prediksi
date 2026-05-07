import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import sys
sys.path.append('.')
from utils.sidebar import tampilkan_sidebar
tampilkan_sidebar()

st.title("🧠 Model Bidirectional LSTM")

if 'data_loaded' not in st.session_state:
    st.warning("⚠️ Harap kembali ke halaman Home terlebih dahulu.")
    st.stop()

hybrid_df = st.session_state['hybrid_df']
arima_df = st.session_state['arima_df']
hybrid_metrics = st.session_state['hybrid_metrics']
ispu_series = st.session_state['ispu_series']

# Info model
st.subheader("📋 Informasi Model BiLSTM")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Time Steps", "15")
col2.metric("Units Layer 1", "75")
col3.metric("Units Layer 2", "37")
col4.metric("Dropout", "0.3")

# Residual ARIMA
st.subheader("📊 Residual ARIMA")
train_size = int(len(ispu_series) * 0.8)
test_data = ispu_series[train_size:]
arima_pred_series = pd.Series(
    arima_df['prediksi_arima'].values,
    index=pd.to_datetime(arima_df['tanggal'])
)
residuals = test_data.values - arima_df['prediksi_arima'].values

fig1 = go.Figure()
fig1.add_trace(go.Scatter(
    x=pd.to_datetime(arima_df['tanggal']),
    y=residuals,
    name='Residual', line=dict(color='purple')))
fig1.update_layout(title='Residual ARIMA (Aktual - Prediksi ARIMA)',
                   xaxis_title='Tanggal', yaxis_title='Residual')
st.plotly_chart(fig1, use_container_width=True)

# Prediksi Hybrid vs Aktual
st.subheader("📈 Prediksi Hybrid ARIMA-BiLSTM vs Aktual")
fig2 = go.Figure()
fig2.add_trace(go.Scatter(
    x=pd.to_datetime(hybrid_df['tanggal']),
    y=hybrid_df['aktual'],
    name='Aktual', line=dict(color='blue')))
fig2.add_trace(go.Scatter(
    x=pd.to_datetime(hybrid_df['tanggal']),
    y=hybrid_df['prediksi_hybrid'],
    name='Hybrid ARIMA-BiLSTM',
    line=dict(color='red', dash='dash')))
fig2.update_layout(title='Hybrid ARIMA-BiLSTM: Prediksi vs Aktual',
                   xaxis_title='Tanggal', yaxis_title='Nilai ISPU')
st.plotly_chart(fig2, use_container_width=True)

# Evaluasi
st.subheader("📊 Hasil Evaluasi Hybrid ARIMA-BiLSTM")
col1, col2, col3 = st.columns(3)
col1.metric("MAE", f"{hybrid_metrics['MAE']:.4f}")
col2.metric("MSE", f"{hybrid_metrics['MSE']:.4f}")
col3.metric("RMSE", f"{hybrid_metrics['RMSE']:.4f}")