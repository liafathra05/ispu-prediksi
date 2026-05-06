import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from utils.sidebar import tampilkan_sidebar
tampilkan_sidebar()

st.title("🔮 Prediksi ISPU Harian DKI Jakarta")

if 'models_loaded' not in st.session_state:
    st.warning("⚠️ Harap kembali ke Home terlebih dahulu.")
    st.stop()

model_arima = st.session_state['model_arima']
model_lstm = st.session_state['model_lstm']
scaler = st.session_state['scaler']
n_steps = st.session_state['n_steps']
ispu_series = st.session_state['ispu_series']

# Fungsi kategori dan anjuran
def get_info_ispu(nilai):
    if nilai <= 50:
        return {
            'kategori': '🟢 Baik',
            'warna': 'green',
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
            'warna': 'orange',
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
            'warna': 'red',
            'deskripsi': 'Kualitas udara tidak sehat. Semua orang mungkin mulai merasakan dampak kesehatan.',
            'anjuran': [
                '❌ Hindari aktivitas luar ruangan yang berat dan berkepanjangan.',
                '❌ Kelompok sensitif sebaiknya tetap di dalam ruangan.',
                '⚠️ Gunakan masker N95 jika harus keluar rumah.',
                '⚠️ Tutup jendela dan gunakan penyaring udara (air purifier) jika ada.',
                '⚠️ Perbanyak minum air putih untuk menjaga kesehatan saluran napas.'
            ]
        }
    elif nilai <= 300:
        return {
            'kategori': '🔴 Sangat Tidak Sehat',
            'warna': 'darkred',
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
            'warna': 'black',
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

        # ARIMA prediksi n hari ke depan
        arima_future = model_arima.predict(n_periods=n_hari)

        # BiLSTM prediksi residual
        data_terakhir = ispu_series.values[-n_steps:].reshape(-1, 1)
        data_terakhir_scaled = scaler.transform(data_terakhir)
        lstm_input = data_terakhir_scaled.reshape(1, n_steps, 1)

        lstm_residual_list = []
        for _ in range(n_hari):
            pred_scaled = model_lstm.predict(lstm_input, verbose=0)
            lstm_residual_list.append(pred_scaled[0][0])
            lstm_input = np.append(lstm_input[:, 1:, :],
                                   pred_scaled.reshape(1, 1, 1), axis=1)

        lstm_residuals = scaler.inverse_transform(
            np.array(lstm_residual_list).reshape(-1, 1)
        ).flatten()

        # Hybrid = ARIMA + BiLSTM residual
        hybrid_future = arima_future + lstm_residuals

        # Buat tanggal prediksi
        tanggal_prediksi = pd.date_range(
            start=tanggal_terakhir + pd.Timedelta(days=1),
            periods=n_hari, freq='D'
        )

        # Buat dataframe hasil
        df_hasil = pd.DataFrame({
            'Tanggal': tanggal_prediksi.strftime('%d %B %Y'),
            'Prediksi ISPU': hybrid_future.round(2),
            'Kategori': [get_info_ispu(v)['kategori'] for v in hybrid_future]
        })

    st.success(f"✅ Prediksi {n_hari} hari ke depan berhasil!")

    # Grafik prediksi
    st.subheader("📈 Grafik Prediksi")
    fig = go.Figure()

    # Data historis 30 hari terakhir
    historis = ispu_series[-30:]
    fig.add_trace(go.Scatter(
        x=historis.index, y=historis.values,
        name='Data Historis', line=dict(color='blue')))
    fig.add_trace(go.Scatter(
        x=tanggal_prediksi, y=hybrid_future,
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
    col1.metric("Rata-rata ISPU", f"{hybrid_future.mean():.2f}")
    col2.metric("ISPU Tertinggi", f"{hybrid_future.max():.2f}")
    col3.metric("ISPU Terendah", f"{hybrid_future.min():.2f}")

    # Anjuran berdasarkan rata-rata prediksi
    st.subheader("💡 Anjuran Kesehatan")
    rata_rata = hybrid_future.mean()
    info = get_info_ispu(rata_rata)

    st.markdown(f"""
    ### {info['kategori']}
    **Rata-rata ISPU yang diprediksi: {rata_rata:.2f}**

    {info['deskripsi']}
    """)

    for anjuran in info['anjuran']:
        st.markdown(f"- {anjuran}")

    # Anjuran per hari jika ada variasi kategori
    kategori_unik = set([get_info_ispu(v)['kategori'] for v in hybrid_future])
    if len(kategori_unik) > 1:
        st.subheader("📅 Detail Anjuran Per Hari")
        for i, (tgl, nilai) in enumerate(zip(tanggal_prediksi, hybrid_future)):
            info_hari = get_info_ispu(nilai)
            with st.expander(f"{tgl.strftime('%d %B %Y')} — ISPU: {nilai:.2f} | {info_hari['kategori']}"):
                st.markdown(f"**{info_hari['deskripsi']}**")
                for anjuran in info_hari['anjuran']:
                    st.markdown(f"- {anjuran}")