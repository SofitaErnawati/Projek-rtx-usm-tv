import streamlit as st
import backend as api
import config
import datetime
import time
from PIL import Image

try:
    icon_img = Image.open("static/owl.png")
except Exception:
    icon_img = "📺"

st.set_page_config(page_title="USM TV - News", page_icon=icon_img)
st.markdown(config.CUSTOM_CSS, unsafe_allow_html=True)

def get_waktu_sekarang():
    hari_dict = {
        "Monday": "Senin", "Tuesday": "Selasa", "Wednesday": "Rabu",
        "Thursday": "Kamis", "Friday": "Jumat",
        "Saturday": "Sabtu", "Sunday": "Minggu"
    }
    sekarang = datetime.datetime.now()
    nama_hari = hari_dict[sekarang.strftime("%A")]
    return sekarang.strftime(f"{nama_hari}, %d %B %Y | %H:%M:%S WIB")

if 'app_ready' not in st.session_state:
    st.session_state.app_ready = False

if not st.session_state.app_ready:
    layar_opening = st.empty()
    
    with layar_opening.container():
        st.markdown("<br><br><br><br>", unsafe_allow_html=True)
        c1, c2, c3 = st.columns([1, 1.5, 1])
        with c2:
            try:
                st.image("static/owl.png")
            except Exception:
                st.warning("Gambar gagal dimuat. Pastikan ada di folder 'static/owl.png'")
            
            st.markdown("<h3 style='text-align: center; color: #1e3c72; font-family: sans-serif;'>Memuat Sistem...</h3>", unsafe_allow_html=True)
            
            progress_bar = st.progress(0)
            for percent in range(100):
                time.sleep(0.015)
                progress_bar.progress(percent + 1)
                
    time.sleep(0.5)
    st.session_state.app_ready = True
    layar_opening.empty()
    st.rerun()

if st.session_state.app_ready:
    st.markdown('<div class="main-header">📺 USM TV News</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="time-display">🕒 {get_waktu_sekarang()}</div>', unsafe_allow_html=True)

    if 'data_berita' not in st.session_state:
        st.session_state.data_berita = []

    st.subheader("Ambil Berita")
    
    opsi_portal = ["Pilih Portal", "antaranews", "tribun jateng", "republika"]
    sumber_pilih = st.selectbox("Sumber:", opsi_portal, label_visibility="collapsed")

    if st.button("Ambil Berita", type="primary", width="stretch"):
        if sumber_pilih != "Pilih Portal":
            with st.spinner(f"Sistem sedang menarik berita dari {sumber_pilih}..."):
                st.session_state.data_berita = api.get_news_data(sumber_pilih)
                if not st.session_state.data_berita:
                    st.error("Gagal menarik berita. Server mungkin sedang sibuk, coba portal lain.")
        else:
            st.warning("Pilih salah satu portal terlebih dahulu.")

    if st.session_state.data_berita:
        pilihan_naskah = []
        st.write("---")
        
        for i, item in enumerate(st.session_state.data_berita):
            c_check, c_text = st.columns([0.05, 0.95])
            
            with c_check:
                pilih = st.checkbox("Pilih berita", key=f"news_{i}", value=True, label_visibility="collapsed")
            
            with c_text:
                st.markdown(f"""
                <div class="news-card">
                    <div style="font-size: 16px; font-weight: bold; color: #1e3c72;">
                        {item['title_rtx']}
                    </div>
                    <div class="news-meta">
                        <span>🕒 {item['published']}</span>
                        <span><a href="{item['link']}" target="_blank">🔗 Baca Aslinya</a></span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            if pilih:
                pilihan_naskah.append(item['title_rtx'])

        if pilihan_naskah:
            st.write("---")
            rtx_final = "   ^   ".join(pilihan_naskah)
            rtx_final = f"   ^   {rtx_final}   ^"
            
            st.subheader("Output Naskah RTX")
            st.code(rtx_final, language="text")
            
            st.download_button(
                label="Download Naskah (.txt)",
                data=rtx_final,
                file_name=f"RTX_USMTV_{datetime.datetime.now().strftime('%d%m%y_%H%M')}.txt",
                mime="text/plain"
            )