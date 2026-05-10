import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import sys
sys.path.append('.')
from utils.sidebar import tampilkan_sidebar
tampilkan_sidebar()

st.title("📊 Exploratory Data Analysis")

if 'data_loaded' not in st.session_state:
    st.warning("⚠️ Harap kembali ke halaman Home terlebih dahulu.")
    st.stop()

df = st.session_state['ispu_series']
numeric_cols = ['pm_sepuluh', 'pm_duakomalima', 'sulfur_dioksida',
                'karbon_monoksida', 'ozon', 'nitrogen_dioksida', 'max']

# Load data asli untuk statistik deskriptif
df_raw = pd.read_excel('data/data-ispu-jakarta.xlsx')
df_raw['tanggal_lengkap'] = (
    df_raw['tahun'].astype(str) + '-' +
    df_raw['bulan'].astype(str) + '-' +
    df_raw['tanggal'].astype(str)
)
df_raw['tanggal_lengkap'] = pd.to_datetime(df_raw['tanggal_lengkap'], errors='coerce')
df_raw.dropna(subset=['tanggal_lengkap'], inplace=True)
df_raw = df_raw.set_index('tanggal_lengkap')
df_raw = df_raw.drop(columns=['Unnamed: 13', 'Unnamed: 14'], errors='ignore')

# Statistik Deskriptif
st.subheader("📋 Statistik Deskriptif")
available_cols = [c for c in numeric_cols if c in df_raw.columns]
st.dataframe(df_raw[available_cols].describe().round(2))

# Time Series Plot
st.subheader("📈 Time Series ISPU Harian")
fig = px.line(
    x=df.index, y=df.values,
    labels={'x': 'Tanggal', 'y': 'Nilai ISPU'},
    title='Time Series Nilai ISPU Harian (Maksimum)'
)
fig.update_traces(line_color='steelblue')
st.plotly_chart(fig, use_container_width=True)

# Distribusi per polutan
st.subheader("📦 Distribusi Per Polutan")
col_pilih = st.selectbox("Pilih polutan:", available_cols)
fig2 = px.histogram(df_raw, x=col_pilih, nbins=50,
                    title=f"Distribusi Nilai {col_pilih}")
st.plotly_chart(fig2, use_container_width=True)
st.markdown("""
    <style>
        /* Warna background selectbox */
        [data-testid="stSelectbox"] div[data-baseweb="select"] > div {
            background-color: #1a1a2e !important;
            color: white !important;
        }
        /* Warna teks di dalam selectbox */
        [data-testid="stSelectbox"] span {
            color: white !important;
        }
        /* Warna opsi saat dropdown dibuka */
        [data-baseweb="popover"] li {
            background-color: #16213e !important;
            color: white !important;
        }
        [data-baseweb="popover"] li:hover {
            background-color: #0f3460 !important;
        }
    </style>
""", unsafe_allow_html=True)

# Korelasi
st.subheader("🔥 Heatmap Korelasi Antar Polutan")
corr = df_raw[available_cols].corr().round(2)
fig3 = px.imshow(corr, text_auto=True, color_continuous_scale='RdBu_r',
                 title="Korelasi Antar Polutan")
st.plotly_chart(fig3, use_container_width=True)
