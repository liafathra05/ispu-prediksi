import streamlit as st
import plotly.graph_objects as go
import numpy as np
from utils.sidebar import tampilkan_sidebar
tampilkan_sidebar()

st.title("📉 Model ARIMA")

if 'models_loaded' not in st.session_state:
    st.warning("⚠️ Harap kembali ke Home terlebih dahulu.")
    st.stop()

train_data = st.session_state['train_data']
test_data = st.session_state['test_data']
arima_predictions = st.session_state['arima_predictions']
arima_metrics = st.session_state['arima_metrics']
model_arima = st.session_state['model_arima']

# Info model
st.subheader("📋 Informasi Model ARIMA")
col1, col2, col3 = st.columns(3)
col1.metric("Order ARIMA", str(model_arima.order))
col2.metric("Data Training", len(train_data))
col3.metric("Data Testing", len(test_data))

# Visualisasi split data
st.subheader("📊 Pembagian Data Training & Testing")
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
fig2.add_trace(go.Scatter(x=test_data.index, y=test_data.values,
                          name='Aktual', line=dict(color='blue')))
fig2.add_trace(go.Scatter(x=arima_predictions.index, y=arima_predictions.values,
                          name='Prediksi ARIMA', line=dict(color='green', dash='dot')))
fig2.update_layout(title='ARIMA: Prediksi vs Aktual',
                   xaxis_title='Tanggal', yaxis_title='Nilai ISPU')
st.plotly_chart(fig2, use_container_width=True)

# Evaluasi
st.subheader("📊 Hasil Evaluasi ARIMA")
col1, col2, col3 = st.columns(3)
col1.metric("MAE", f"{arima_metrics['MAE']:.4f}")
col2.metric("MSE", f"{arima_metrics['MSE']:.4f}")
col3.metric("RMSE", f"{arima_metrics['RMSE']:.4f}")