import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from utils.sidebar import tampilkan_sidebar
tampilkan_sidebar()

st.title("📊 Exploratory Data Analysis")

if 'df_processed' not in st.session_state:
    st.warning("⚠️ Harap lakukan preprocessing terlebih dahulu di halaman Home.")
    st.stop()

df = st.session_state['df_processed']
numeric_cols = st.session_state['numeric_cols']

# Statistik Deskriptif
st.subheader("📋 Statistik Deskriptif")
st.dataframe(df[numeric_cols].describe().round(2))

# Time Series Plot
st.subheader("📈 Time Series ISPU Harian")

ispu_series = df.groupby('tanggal_lengkap')['max'].max().sort_index()
st.session_state['ispu_series'] = ispu_series

fig = px.line(
    x=ispu_series.index,
    y=ispu_series.values,
    labels={'x': 'Tanggal', 'y': 'Nilai ISPU'},
    title='Time Series Nilai ISPU Harian (Maksimum)'
)
fig.update_traces(line_color='steelblue')
st.plotly_chart(fig, use_container_width=True)

# Distribusi per polutan
st.subheader("📦 Distribusi Per Polutan")
col_pilih = st.selectbox("Pilih polutan:", numeric_cols)

fig2 = px.histogram(df, x=col_pilih, nbins=50,
                    title=f"Distribusi Nilai {col_pilih}")
st.plotly_chart(fig2, use_container_width=True)

# Korelasi
st.subheader("🔥 Heatmap Korelasi Antar Polutan")
corr = df[numeric_cols].corr().round(2)
fig3 = px.imshow(corr, text_auto=True, color_continuous_scale='RdBu_r',
                 title="Korelasi Antar Polutan")
st.plotly_chart(fig3, use_container_width=True)

st.info("✅ Eksplorasi selesai! Lanjutkan ke halaman ARIMA.")