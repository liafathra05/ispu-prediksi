import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import sys
sys.path.append('.')
from utils.sidebar import tampilkan_sidebar
tampilkan_sidebar()

st.title("🏆 Evaluasi & Perbandingan Model")

if 'data_loaded' not in st.session_state:
    st.warning("⚠️ Harap kembali ke halaman Dashboard terlebih dahulu.")
    st.stop()

arima_metrics = st.session_state['arima_metrics']
hybrid_metrics = st.session_state['hybrid_metrics']
arima_df = st.session_state['arima_df']
hybrid_df = st.session_state['hybrid_df']

# Tabel perbandingan
st.subheader("📊 Tabel Perbandingan Metrik")
metrics_data = {
    'ARIMA Standalone': arima_metrics,
    'Hybrid ARIMA-BiLSTM': hybrid_metrics
}
df_metrics = pd.DataFrame(metrics_data).T.round(4)
st.dataframe(df_metrics, use_container_width=True)

# Bar chart MAE
st.subheader("📈 Perbandingan MAE")
fig1 = px.bar(
    x=df_metrics.index,
    y=df_metrics['MAE'],
    text=df_metrics['MAE'],
    color=df_metrics.index,
    color_discrete_sequence=['#3498db', '#e74c3c'],
    title='Perbandingan MAE Antar Model'
)
fig1.update_traces(texttemplate='%{text:.4f}', textposition='auto')
fig1.update_layout(xaxis_title='Model', yaxis_title='MAE', showlegend=False)
st.plotly_chart(fig1, use_container_width=True)

# Bar chart RMSE
st.subheader("📈 Perbandingan RMSE")
fig2 = px.bar(
    x=df_metrics.index,
    y=df_metrics['RMSE'],
    text=df_metrics['RMSE'],
    color=df_metrics.index,
    color_discrete_sequence=['#3498db', '#e74c3c'],
    title='Perbandingan RMSE Antar Model'
)
fig2.update_traces(texttemplate='%{text:.4f}', textposition='auto')
fig2.update_layout(xaxis_title='Model', yaxis_title='RMSE', showlegend=False)
st.plotly_chart(fig2, use_container_width=True)

# Perbandingan prediksi vs aktual
st.subheader("📈 Perbandingan Semua Model vs Aktual")
fig3 = go.Figure()
fig3.add_trace(go.Scatter(
    x=pd.to_datetime(hybrid_df['tanggal']),
    y=hybrid_df['aktual'],
    name='Aktual', line=dict(color='blue')))
fig3.add_trace(go.Scatter(
    x=pd.to_datetime(arima_df['tanggal']),
    y=arima_df['prediksi_arima'],
    name='ARIMA', line=dict(color='green', dash='dot')))
fig3.add_trace(go.Scatter(
    x=pd.to_datetime(hybrid_df['tanggal']),
    y=hybrid_df['prediksi_hybrid'],
    name='Hybrid ARIMA-BiLSTM',
    line=dict(color='red', dash='dash')))
fig3.update_layout(title='Perbandingan Semua Model vs Aktual',
                   xaxis_title='Tanggal', yaxis_title='Nilai ISPU',
                   hovermode='x unified')
st.plotly_chart(fig3, use_container_width=True)

# Kesimpulan
st.subheader("🏆 Kesimpulan")
best_model = df_metrics['RMSE'].idxmin()
best_rmse = df_metrics.loc[best_model, 'RMSE']
best_mae = df_metrics.loc[best_model, 'MAE']

st.success(f"""
**Model Terbaik: {best_model}**
- RMSE: {best_rmse:.4f}
- MAE: {best_mae:.4f}
""")
