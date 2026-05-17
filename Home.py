import streamlit as st
import base64
import sys
sys.path.append('.')
from utils.sidebar import tampilkan_sidebar
tampilkan_sidebar()

st.set_page_config(
    page_title="Prediksi ISPU Jakarta",
    page_icon="🌫️",
    layout="wide"
)

# Fungsi load background image
def get_base64_image(image_path):
    with open(image_path, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

img_base64 = get_base64_image("background.png")

st.markdown(f"""
    <style>
        /* Sembunyikan header streamlit */
        #MainMenu, header, footer {{visibility: hidden;}}
        
        /* Background utama */
        .stApp {{
            background-image: url("data:image/png;base64,{img_base64}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}

        /* Overlay gelap supaya teks terbaca */
        .stApp::before {{
            content: "";
            position: fixed;
            top: 0; left: 0;
            width: 100%; height: 100%;
            background: rgba(10, 15, 40, 0.55);
            z-index: 0;
        }}

        /* Judul utama */
        .hero-title {{
            text-align: center;
            color: white;
            font-size: 16px;
            font-weight: 600;
            letter-spacing: 2px;
            text-transform: uppercase;
            margin-top: 40px;
            margin-bottom: 5px;
            opacity: 0.8;
        }}

        /* Judul skripsi */
        .judul-skripsi {{
            text-align: center;
            color: white;
            font-size: 22px;
            font-weight: bold;
            line-height: 1.7;
            max-width: 850px;
            margin: 10px auto 40px auto;
            text-shadow: 0 2px 10px rgba(0,0,0,0.5);
        }}

        /* Divider bergaya */
        .divider-line {{
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 10px;
            margin: 10px auto 30px auto;
            max-width: 400px;
        }}
        .divider-line::before, .divider-line::after {{
            content: "";
            flex: 1;
            height: 1px;
            background: rgba(255,255,255,0.4);
        }}
        .divider-text {{
            color: rgba(255,255,255,0.7);
            font-size: 14px;
            white-space: nowrap;
        }}

        /* Card identitas */
        .identitas-grid {{
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 15px;
            max-width: 900px;
            margin: 0 auto 20px auto;
        }}
        .identitas-card {{
            background: rgba(255, 255, 255, 0.08);
            border: 1px solid rgba(255, 255, 255, 0.15);
            border-radius: 12px;
            padding: 15px 20px;
            backdrop-filter: blur(10px);
        }}
        .identitas-card .icon {{
            font-size: 24px;
            margin-bottom: 8px;
        }}
        .identitas-card .label {{
            color: #7eb3ff;
            font-size: 12px;
            font-weight: bold;
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-bottom: 4px;
        }}
        .identitas-card .value {{
            color: white;
            font-size: 14px;
            font-weight: 500;
        }}

        /* Card dosen pembimbing (full width) */
        .dosbing-card {{
            background: rgba(255, 255, 255, 0.08);
            border: 1px solid rgba(255, 255, 255, 0.15);
            border-radius: 12px;
            padding: 15px 20px;
            max-width: 900px;
            margin: 0 auto 40px auto;
            backdrop-filter: blur(10px);
            display: flex;
            align-items: center;
            gap: 15px;
        }}
        .dosbing-card .icon {{
            font-size: 28px;
        }}
        .dosbing-card .label {{
            color: #7eb3ff;
            font-size: 12px;
            font-weight: bold;
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-bottom: 4px;
        }}
        .dosbing-card .value {{
            color: white;
            font-size: 15px;
            font-weight: 500;
        }}

        /* Icon fitur bawah */
        .fitur-grid {{
            display: flex;
            justify-content: center;
            gap: 40px;
            margin: 20px auto;
            max-width: 700px;
        }}
        .fitur-item {{
            text-align: center;
            color: rgba(255,255,255,0.8);
        }}
        .fitur-item .fitur-icon {{
            width: 60px;
            height: 60px;
            border: 1px solid rgba(255,255,255,0.3);
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 24px;
            margin: 0 auto 10px auto;
            background: rgba(255,255,255,0.05);
        }}
        .fitur-item .fitur-label {{
            font-size: 11px;
            font-weight: bold;
            letter-spacing: 1px;
            text-transform: uppercase;
        }}
    </style>
""", unsafe_allow_html=True)

# Hero section
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
            <div class="label">Nama</div>
            <div class="value">Liafathra</div>
        </div>
        <div class="identitas-card">
            <div class="icon">🎓</div>
            <div class="label">Program Studi</div>
            <div class="value">Teknik Informatika</div>
        </div>
        <div class="identitas-card">
            <div class="icon">🏛️</div>
            <div class="label">Universitas</div>
            <div class="value">Universitas Negeri Semarang</div>
        </div>
        <div class="identitas-card">
            <div class="icon">🪪</div>
            <div class="label">NIM</div>
            <div class="value">4611422128</div>
        </div>
        <div class="identitas-card">
            <div class="icon">🏢</div>
            <div class="label">Fakultas</div>
            <div class="value">Fakultas Matematika dan Ilmu Pengetahuan Alam</div>
        </div>
        <div class="identitas-card">
            <div class="icon">📅</div>
            <div class="label">Tahun</div>
            <div class="value">2025</div>
        </div>
    </div>
""", unsafe_allow_html=True)

# Dosen pembimbing
st.markdown("""
    <div class="dosbing-card">
        <div class="icon">👨‍🏫</div>
        <div>
            <div class="label">Dosen Pembimbing</div>
            <div class="value">Endang Sugiharti, S.Si., M.Kom.</div>
        </div>
    </div>
""", unsafe_allow_html=True)

# Fitur bawah
st.markdown("""
    <div class="fitur-grid">
        <div class="fitur-item">
            <div class="fitur-icon">☁️</div>
            <div class="fitur-label">Kualitas Udara</div>
        </div>
        <div class="fitur-item">
            <div class="fitur-icon">🧠</div>
            <div class="fitur-label">AI & Deep Learning</div>
        </div>
        <div class="fitur-item">
            <div class="fitur-icon">📊</div>
            <div class="fitur-label">Prediksi Akurat</div>
        </div>
        <div class="fitur-item">
            <div class="fitur-icon">✅</div>
            <div class="fitur-label">Keputusan Cerdas</div>
        </div>
    </div>
""", unsafe_allow_html=True)
