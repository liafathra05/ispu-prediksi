import streamlit as st

def tampilkan_sidebar():
    st.markdown("""
        <style>
            [data-testid="stSidebarNav"] {
            padding-top: 20px;
            }
            [data-testid="stSidebarNav"]::before {
                content: "🌫️ ISPU DKI Jakarta";
                display: block;
                font-size: 18px;
                font-weight: bold;
                color: white;
                padding: 10px 20px 20px 20px;
                border-bottom: 1px solid rgba(255,255,255,0.2);
                margin-bottom: 10px;
            }
            [data-testid="stSidebar"] {
                background: linear-gradient(180deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
            }
            [data-testid="stSidebarNav"] a span {
                color: white !important;
            }
            [data-testid="stSidebarNav"] a {
                color: white !important;
                background-color: transparent !important;
            }
            [data-testid="stSidebarNav"] a:hover {
                background-color: rgba(255,255,255,0.1) !important;
                border-radius: 5px;
            }
            [data-testid="stSidebar"] * {
                color: white !important;
            }
            [data-testid="stSelectbox"] div[data-baseweb="select"] > div {
                background-color: #1a1a2e !important;
                color: white !important;
            }
            /* Warna teks di dalam dropdown */
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

    with st.sidebar:
        st.markdown("### 📌 Tentang Aplikasi")
        st.markdown("""
        Aplikasi ini dikembangkan untuk
        memprediksi kualitas udara harian
        di DKI Jakarta menggunakan model
        **Hybrid ARIMA-BiLSTM**.
        """)
        st.markdown("--")
        st.markdown("### 📊 Kategori ISPU")
        st.markdown("""
        🟢 **0-50** - Baik  
        🟡 **51-100** - Sedang  
        🟠 **101-200** - Tidak Sehat  
        🔴 **201-300** - Sangat Tidak Sehat  
        ⚫ **>300** - Berbahaya  
        """)
        st.markdown("---")
        st.caption("© 2024 Prediksi ISPU Jakarta")
