import streamlit as st
import sys
sys.path.append('.')
from utils.sidebar import tampilkan_sidebar
tampilkan_sidebar()

st.set_page_config(
    page_title="Prediksi ISPU Jakarta",
    page_icon="🌫️",
    layout="wide"
)

st.markdown("""
    <style>
        /* Judul utama */
        .hero-title {
            text-align: center;
            font-size: 14px;
            font-weight: 600;
            letter-spacing: 2px;
            text-transform: uppercase;
            margin-top: 30px;
            margin-bottom: 5px;
            color: #0f3460;
            opacity: 0.8;
        }

        /* Judul skripsi */
        .judul-skripsi {
            text-align: center;
            font-size: 20px;
            font-weight: bold;
            line-height: 1.7;
            max-width: 850px;
            margin: 10px auto 30px auto;
            padding: 20px 30px;
            border: 2px solid #0f3460;
            border-radius: 12px;
            background: #f0f4ff;
            color: #0f3460;
        }

        /* Divider */
        .divider-line {
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 10px;
            margin: 10px auto 25px auto;
            max-width: 400px;
        }
        .divider-line::before, .divider-line::after {
            content: "";
            flex: 1;
            height: 1px;
            background: #0f3460;
            opacity: 0.4;
        }
        .divider-text {
            font-size: 13px;
            color: #0f3460;
            opacity: 0.7;
            white-space: nowrap;
        }

        /* Grid identitas */
        .identitas-grid {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 12px;
            max-width: 900px;
            margin: 0 auto 15px auto;
        }

        /* Card identitas */
        .identitas-card {
            background: #f8f9fa;
            border: 1px solid #dee2e6;
            border-radius: 10px;
            padding: 12px 16px;
            display: flex;
            align-items: center;
            gap: 12px;
        }
        .identitas-card .icon {
            font-size: 20px;
            flex-shrink: 0;
        }
        .identitas-card .label {
            color: #0f3460;
            font-size: 11px;
            font-weight: bold;
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-bottom: 3px;
        }
        .identitas-card .value {
            color: #333;
            font-size: 13px;
            font-weight: 500;
        }

        /* Card dosen pembimbing */
        .dosbing-card {
            background: #f8f9fa;
            border: 1px solid #dee2e6;
            border-radius: 10px;
            padding: 12px 16px;
            max-width: 900px;
            margin: 0 auto 30px auto;
            display: flex;
            align-items: center;
            gap: 12px;
        }
        .dosbing-card .icon {
            font-size: 20px;
            flex-shrink: 0;
        }
        .dosbing-card .label {
            color: #0f3460;
            font-size: 11px;
            font-weight: bold;
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-bottom: 3px;
        }
        .dosbing-card .value {
            color: #333;
            font-size: 13px;
            font-weight: 500;
        }
    </style>
""", unsafe_allow_html=True)

# Hero
st.markdown("""
    <div class="hero-title">Sistem Prediksi Kualitas Udara · DKI Jakarta</div>
    <div class="judul-skripsi">
        PREDIKSI INDEKS STANDAR PENCEMAR UDARA DI DKI JAKARTA<br>
        MENGGUNAKAN METODE HYBRID
        <i>AUTOREGRESSIVE INTEGRATED MOVING AVERAGE</i> (ARIMA)<br>
        DAN <i>BIDIRECTIONAL LSTM</i>
    </div>
""", unsafe_allow_html=True)

# Divider
st.markdown("""
    <div class="divider-line">
        <span class="divider-text">✦ Tentang Penelitian ✦</span>
    </div>
""", unsafe_allow_html=True)

# Grid identitas
st.markdown("""
    <div class="identitas-grid">
        <div class="identitas-card">
            <div class="icon">👤</div>
            <div>
                <div class="label">Nama</div>
                <div class="value">Liafathra</div>
            </div>
        </div>
        <div class="identitas-card">
            <div class="icon">🎓</div>
            <div>
                <div class="label">Program Studi</div>
                <div class="value">Teknik Informatika</div>
            </div>
        </div>
        <div class="identitas-card">
            <div class="icon">🏛️</div>
            <div>
                <div class="label">Universitas</div>
                <div class="value">Universitas Negeri Semarang</div>
            </div>
        </div>
        <div class="identitas-card">
            <div class="icon">💳</div>
            <div>
                <div class="label">NIM</div>
                <div class="value">4611422125</div>
            </div>
        </div>
        <div class="identitas-card">
            <div class="icon">🏢</div>
            <div>
                <div class="label">Fakultas</div>
                <div class="value">Fakultas Matematika dan Ilmu Pengetahuan Alam</div>
            </div>
        </div>
        <div class="identitas-card">
            <div class="icon">📅</div>
            <div>
                <div class="label">Tahun</div>
                <div class="value">2026</div>
            </div>
        </div>
    </div>
""", unsafe_allow_html=True)

# Dosen pembimbing
st.markdown("""
    <div class="dosbing-card">
        <div class="icon">👨‍🏫</div>
        <div>
            <div class="label">Dosen Pembimbing</div>
            <div class="value">Nama Dosen Pembimbing, S.Si., M.Kom.</div>
        </div>
    </div>
""", unsafe_allow_html=True)
