import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from utils.sidebar import tampilkan_sidebar
tampilkan_sidebar()

st.title("🧠 Model Bidirectional LSTM")

if 'models_loaded' not in st.session_state:
    st.warning("⚠️ Harap kembali ke Home terlebih dahulu.")
    st.stop()

train_data = st.session_state['train_data']
test_data = st.session_state['test_data']
arima_predictions = st.session_state['arima_predictions']
hybrid_predictions = st.session_state['hybrid_predictions']
actual_aligned = st.session_state['actual_aligned']
hybrid_metrics = st.session_state['hybrid_metrics']
model_arima = st.session_state['model_arima']
n_steps = st.session_state['n_steps']

# Info model
st.subheader("📋 Informasi Model BiLSTM")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Time Steps", n_steps)
col2.metric("Units Layer 1", 75)
col3.metric("Units Layer 2", 37)
col4.metric("Dropout", "0.3")

# Residual ARIMA
st.subheader("📊 Residual ARIMA")
arima_residuals_train = train_data - model_arima.predict_in_sample()
arima_residuals_test = test_data - arima_predictions

fig1 = go.Figure()
fig1.add_trace(go.Scatter(x=arima_residuals_train.index,
                          y=arima_residuals_train.values,
                          name='Residual Training', line=dict(color='blue')))
fig1.add_trace(go.Scatter(x=arima_residuals_test.index,
                          y=arima_residuals_test.values,
                          name='Residual Testing', line=dict(color='orange')))
fig1.update_layout(title='Residual ARIMA',
                   xaxis_title='Tanggal', yaxis_title='Residual')
st.plotly_chart(fig1, use_container_width=True)

# Prediksi Hybrid vs Aktual
st.subheader("📈 Prediksi Hybrid ARIMA-BiLSTM vs Aktual")
fig2 = go.Figure()
fig2.add_trace(go.Scatter(x=actual_aligned.index, y=actual_aligned.values,
                          name='Aktual', line=dict(color='blue')))
fig2.add_trace(go.Scatter(x=hybrid_predictions.index, y=hybrid_predictions.values,
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