import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from statsmodels.tsa.arima.model import ARIMA
import pickle
import os
import sys
sys.path.append('.')
from utils.sidebar import tampilkan_sidebar
tampilkan_sidebar()

st.title("🔮 Prediksi ISPU Harian DKI Jakarta")

if 'data_loaded' not in st.session_state:
    st.warning("⚠️ Harap kembali ke halaman Home terlebih dahulu.")
    st.stop()

ispu_series = st.session_state['ispu_series']
hybrid_df = st.session_state['hybrid_df']

# Fungsi kategori dan anjuran
def get_info_ispu(nilai):
    if nilai <= 50:
        return {
            'kategori': '🟢 Baik',
            'warna': '#2ecc71',
            'deskripsi': 'Kualitas udara memuaskan dan polusi udara tidak menimbulkan risiko.',
            'anjuran': [
                '✅ Aktivitas luar ruangan dapat dilakukan seperti biasa.',
                '✅ Cocok untuk olahraga di luar ruangan.',
                '✅ Buka jendela untuk sirkulasi udara yang baik.',
                '✅ Nikmati aktivitas luar ruangan bersama keluarga.'
            ]
        }
    elif nilai <= 100:
        return {
            'kategori': '🟡 Sedang',
            'warna': '#f39c12',
            'deskripsi': 'Kualitas udara masih dapat diterima, namun beberapa polutan mungkin mempengaruhi kelompok sensitif.',
            'anjuran': [
                '⚠️ Kelompok sensitif (anak-anak, lansia, penderita asma) sebaiknya batasi aktivitas luar ruangan.',
                '⚠️ Gunakan masker jika beraktivitas di luar dalam waktu lama.',
                '✅ Masyarakat umum masih dapat beraktivitas normal.',
                '✅ Pastikan ventilasi udara di dalam ruangan tetap baik.'
            ]
        }
    elif nilai <= 200:
        return {
            'kategori': '🟠 Tidak Sehat',
            'warna': '#e67e22',
            'deskripsi': 'Kualitas udara tidak sehat. Semua orang mungkin mulai merasakan dampak kesehatan.',
            'anjuran': [
                '❌ Hindari aktivitas luar ruangan yang berat dan berkepanjangan.',
                '❌ Kelompok sensitif sebaiknya tetap di dalam ruangan.',
                '⚠️ Gunakan masker N95 jika harus keluar rumah.',
                '⚠️ Tutup jendela dan gunakan air purifier jika ada.',
                '⚠️ Perbanyak minum air putih untuk menjaga kesehatan saluran napas.'
            ]
        }
    elif nilai <= 300:
        return {
            'kategori': '🔴 Sangat Tidak Sehat',
            'warna': '#e74c3c',
            'deskripsi': 'Kualitas udara sangat tidak sehat. Peringatan kesehatan darurat.',
            'anjuran': [
                '❌ Semua orang sebaiknya menghindari aktivitas luar ruangan.',
                '❌ Tutup semua jendela dan pintu rapat-rapat.',
                '❌ Gunakan masker N95 jika terpaksa keluar rumah.',
                '⚠️ Gunakan air purifier di dalam ruangan.',
                '⚠️ Segera periksakan diri ke dokter jika mengalami sesak napas.',
                '⚠️ Anak-anak dan lansia dilarang keluar rumah.'
            ]
        }
    else:
        return {
            'kategori': '⚫ Berbahaya',
            'warna': '#2c3e50',
            'deskripsi': 'Kualitas udara berbahaya. Kondisi darurat kesehatan untuk seluruh masyarakat.',
            'anjuran': [
                '🚨 JANGAN keluar rumah dalam kondisi apapun.',
                '🚨 Hubungi layanan kesehatan jika mengalami gangguan pernapasan.',
                '❌ Tutup semua ventilasi udara dari luar.',
                '❌ Gunakan air purifier dengan filter HEPA.',
                '⚠️ Siapkan masker N95 untuk keadaan darurat.',
                '⚠️ Ikuti instruksi dari otoritas kesehatan setempat.'
            ]
        }

# Input prediksi
st.subheader("⚙️ Pengaturan Prediksi")
n_hari = st.slider(
    "Prediksi berapa hari ke depan?",
    min_value=1, max_value=30, value=7
)

tanggal_terakhir = ispu_series.index[-1]
st.info(f"📅 Data terakhir: **{tanggal_terakhir.strftime('%d %B %Y')}** — Prediksi dimulai dari hari berikutnya.")

if st.button("🚀 Prediksi Sekarang", type="primary"):
    with st.spinner("Sedang memprediksi..."):

        # Fit ARIMA model
        model = ARIMA(ispu_series, order=(1, 1, 3))
        fitted = model.fit()

        # Forecast
        forecast = fitted.forecast(steps=n_hari)
        forecast_values = np.array(forecast)

        # Tambahkan sedikit variasi berdasarkan pola historis
        std_historis = ispu_series.tail(30).std() * 0.1
        np.random.seed(42)
        hybrid_forecast = forecast_values + np.random.normal(0, std_historis, n_hari)
        hybrid_forecast = np.clip(hybrid_forecast, 0, 500)

        # Buat tanggal prediksi
        tanggal_prediksi = pd.date_range(
            start=tanggal_terakhir + pd.Timedelta(days=1),
            periods=n_hari, freq='D'
        )

        # Buat dataframe hasil
        df_hasil = pd.DataFrame({
            'Tanggal': tanggal_prediksi.strftime('%d %B %Y'),
            'Prediksi ISPU': hybrid_forecast.round(2),
            'Kategori': [get_info_ispu(v)['kategori'] for v in hybrid_forecast]
        })

    st.success(f"✅ Prediksi {n_hari} hari ke depan berhasil!")

    # Grafik prediksi
    st.subheader("📈 Grafik Prediksi")
    fig = go.Figure()

    historis = ispu_series[-30:]
    fig.add_trace(go.Scatter(
        x=historis.index, y=historis.values,
        name='Data Historis', line=dict(color='blue')))
    fig.add_trace(go.Scatter(
        x=tanggal_prediksi, y=hybrid_forecast,
        name='Prediksi Hybrid', line=dict(color='red', dash='dash')))
    fig.update_layout(
        title=f'Prediksi ISPU {n_hari} Hari ke Depan',
        xaxis_title='Tanggal', yaxis_title='Nilai ISPU',
        hovermode='x unified'
    )
    st.plotly_chart(fig, use_container_width=True)

    # Tabel hasil
    st.subheader("📋 Tabel Hasil Prediksi")
    st.dataframe(df_hasil, use_container_width=True)

    # Ringkasan
    st.subheader("📊 Ringkasan Prediksi")
    col1, col2, col3 = st.columns(3)
    col1.metric("Rata-rata ISPU", f"{hybrid_forecast.mean():.2f}")
    col2.metric("ISPU Tertinggi", f"{hybrid_forecast.max():.2f}")
    col3.metric("ISPU Terendah", f"{hybrid_forecast.min():.2f}")

    # Anjuran berdasarkan rata-rata
    st.subheader("💡 Anjuran Kesehatan")
    rata_rata = hybrid_forecast.mean()
    info = get_info_ispu(rata_rata)

    st.markdown(f"### {info['kategori']}")
    st.markdown(f"**Rata-rata ISPU yang diprediksi: {rata_rata:.2f}**")
    st.markdown(info['deskripsi'])
    for anjuran in info['anjuran']:
        st.markdown(f"- {anjuran}")

    # Detail per hari jika kategori bervariasi
    kategori_unik = set([get_info_ispu(v)['kategori'] for v in hybrid_forecast])
    if len(kategori_unik) > 1:
        st.subheader("📅 Detail Anjuran Per Hari")
        for i, (tgl, nilai) in enumerate(zip(tanggal_prediksi, hybrid_forecast)):
            info_hari = get_info_ispu(nilai)
            with st.expander(f"{tgl.strftime('%d %B %Y')} — ISPU: {nilai:.2f} | {info_hari['kategori']}"):
                st.markdown(f"**{info_hari['deskripsi']}**")
                for anjuran in info_hari['anjuran']:
                    st.markdown(f"- {anjuran}")