import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import sys
sys.path.append('.')
from utils.sidebar import tampilkan_sidebar
tampilkan_sidebar()

st.title("📉 Model ARIMA")

if 'data_loaded' not in st.session_state:
    st.warning("⚠️ Harap kembali ke halaman Dashboard terlebih dahulu.")
    st.stop()

arima_df = st.session_state['arima_df']
arima_metrics = st.session_state['arima_metrics']

# Info model
st.subheader("📋 Informasi Model ARIMA")
col1, col2, col3 = st.columns(3)
col1.metric("Order ARIMA", "(1, 1, 2)")
col2.metric("Data Training", "511")
col3.metric("Data Testing", "128")

# Visualisasi pembagian data
st.subheader("📊 Pembagian Data Training & Testing")
ispu_series = st.session_state['ispu_series']
train_size = int(len(ispu_series) * 0.8)
train_data = ispu_series[:train_size]
test_data = ispu_series[train_size:]

fig1 = go.Figure()
fig1.add_trace(go.Scatter(x=train_data.index, y=train_data.values,
                          name='Training', line=dict(color='blue')))
fig1.add_trace(go.Scatter(x=test_data.index, y=test_data.values,
                          name='Testing', line=dict(color='orange')))
fig1.update_layout(title='Pembagian Data Training & Testing',
                   xaxis_title='Tanggal', yaxis_title='Nilai ISPU')
st.plotly_chart(fig1, use_container_width=True)

# Visualisasi prediksi vs aktual
st.subheader("📈 Prediksi ARIMA vs Aktual")
fig2 = go.Figure()
fig2.add_trace(go.Scatter(x=pd.to_datetime(arima_df['tanggal']),
                          y=arima_df['aktual'],
                          name='Aktual', line=dict(color='blue')))
fig2.add_trace(go.Scatter(x=pd.to_datetime(arima_df['tanggal']),
                          y=arima_df['prediksi_arima'],
                          name='Prediksi ARIMA',
                          line=dict(color='green', dash='dot')))
fig2.update_layout(title='ARIMA: Prediksi vs Aktual',
                   xaxis_title='Tanggal', yaxis_title='Nilai ISPU')
st.plotly_chart(fig2, use_container_width=True)

# Evaluasi
st.subheader("📊 Hasil Evaluasi ARIMA")
col1, col2 = st.columns(2)
col1.metric("MAE", f"{arima_metrics['MAE']:.4f}")
col2.metric("RMSE", f"{arima_metrics['RMSE']:.4f}")
