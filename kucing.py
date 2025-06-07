# meongpedia_streamlit.py
# Untuk menjalankan aplikasi ini, ikuti langkah berikut:
# 1. Pastikan Anda memiliki Python terinstal.
# 2. Buka terminal atau command prompt.
# 3. Instal library yang dibutuhkan:
#    pip install streamlit requests
# 4. Simpan kode ini sebagai file Python (misal: meongpedia_app.py).
# 5. Jalankan aplikasi dengan perintah:
#    streamlit run meongpedia_app.py

import streamlit as st
import requests
import json
import os
import time

# --- Konfigurasi Halaman ---
st.set_page_config(
    page_title="MeongPedia",
    page_icon="🐾",
    layout="wide",
    initial_sidebar_state="auto"
)

# --- Database Kucing ---
# PERBAIKAN: Sintaks pada daftar di bawah ini telah dirapikan untuk menghindari error.
# Pastikan setiap item ada di dalam format { "kunci": "nilai" }, dan dipisahkan koma.
cat_data = [
    {"name": "Persia", "origin": "Iran", "image": "https://placehold.co/400x400/FFE4E1/333333?text=Persia"},
    {"name": "Maine Coon", "origin": "Amerika Serikat", "image": "https://placehold.co/400x400/D2B48C/FFFFFF?text=Maine+Coon"},
    {"name": "Siam", "origin": "Thailand", "image": "https://placehold.co/400x400/ADD8E6/333333?text=Siam"},
    {"name": "Sphynx", "origin": "Kanada", "image": "https://placehold.co/400x400/F5DEB3/333333?text=Sphynx"},
    {"name": "Bengal", "origin": "Amerika Serikat", "image": "https://placehold.co/400x400/F4A460/FFFFFF?text=Bengal"},
    {"name": "Ragdoll", "origin": "Amerika Serikat", "image": "https://placehold.co/400x400/E6E6FA/333333?text=Ragdoll"},
    {"name": "British Shorthair", "origin": "Inggris", "image": "https://placehold.co/400x400/B0C4DE/FFFFFF?text=British+Shorthair"},
    {"name": "Scottish Fold", "origin": "Skotlandia", "image": "https://placehold.co/400x400/778899/FFFFFF?text=Scottish+Fold"},
    {"name": "Anggora", "origin": "Turki", "image": "https://placehold.co/400x400/F0F8FF/333333?text=Anggora"},
    {"name": "Kucing Kampung", "origin": "Seluruh Dunia", "image": "https://placehold.co/400x400/A9A9A9/FFFFFF?text=Kampung"},
    {"name": "Russian Blue", "origin": "Rusia", "image": "https://placehold.co/400x400/6A5ACD/FFFFFF?text=Russian+Blue"},
    {"name": "Abyssinian", "origin": "Etiopia", "image": "https://placehold.co/400x400/CD853F/FFFFFF?text=Abyssinian"}
]

# --- Fungsi untuk memanggil Gemini API ---
def call_gemini_api(payload):
    """Fungsi generik untuk memanggil Gemini API."""
    api_key = ""  # Kunci API akan ditangani secara otomatis
    api_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={api_key}"
    headers = {"Content-Type": "application/json"}
    
    try:
        response = requests.post(api_url, headers=headers, data=json.dumps(payload))
        response.raise_for_status()  # Akan raise error untuk status 4xx/5xx
        result = response.json()
        
        if "candidates" in result and result["candidates"]:
            if "content" in result["candidates"][0] and "parts" in result["candidates"][0]["content"]:
                return result["candidates"][0]["content"]["parts"][0]["text"]
        return "Meow... maaf, aku sedang bingung. Bisa ulangi lagi?"
    except requests.exceptions.RequestException as e:
        st.error(f"Terjadi kesalahan jaringan: {e}")
        return "Meow! Sepertinya ada masalah dengan jaringanku. Coba lagi nanti ya."
    except Exception as e:
        st.error(f"Terjadi kesalahan tidak terduga: {e}")
        return "Purrr... ada yang tidak beres. Aku akan coba perbaiki."

# =====================================================================
# --- Tampilan Utama Aplikasi ---
# =====================================================================

st.title("🐾 MeongPedia")
st.markdown("### Ensiklopedia Kucing Terlengkap dan Paling Seru!")

# --- Fitur Pencarian ---
search_query = st.text_input(
    "Cari jenis kucing apa hari ini?",
    placeholder="Ketik nama kucing, contoh: Siam, Bengal..."
)

filtered_cats = [
    cat for cat in cat_data
    if search_query.lower() in cat["name"].lower()
]

# --- Galeri Kucing ---
st.markdown("---")
if not filtered_cats:
    st.warning(f"Oops! Kucing dengan nama '{search_query}' tidak ditemukan.")
else:
    # Membuat grid dengan 4 kolom
    cols = st.columns(4)
    for index, cat in enumerate(filtered_cats):
        col = cols[index % 4]
        with col:
            st.image(cat["image"], caption=f"Foto {cat['name']}", use_column_width=True)
            st.subheader(cat["name"])
            st.caption(f"Asal: {cat['origin']}")
            
            # Fitur Fakta Menarik dengan Expander
            with st.expander("✨ Lihat Fakta Menarik"):
                with st.spinner("MeongBot sedang mencari fakta..."):
                    fact_prompt = f"Berikan satu fakta menarik, unik, dan singkat tentang kucing ras {cat['name']} dalam bahasa Indonesia."
                    fact_payload = {"contents": [{"role": "user", "parts": [{"text": fact_prompt}]}]}
                    fun_fact = call_gemini_api(fact_payload)
                    st.info(fun_fact)

# =====================================================================
# --- Chatbot di Sidebar ---
# =====================================================================

st.sidebar.title("Ngobrol sama MeongBot 🤖")
st.sidebar.markdown("Punya pertanyaan atau cuma ingin iseng? Ngobrol saja di sini!")

# Inisialisasi riwayat chat di session state
if "messages" not in st.session_state:
    st.session_state.messages = []
    # Pesan sapaan pertama dari AI
    initial_greeting = "Meow! Namaku MeongBot. Ada yang bisa kubantu? Tanya apa saja tentang kucing, atau kita ngobrol santai juga boleh, purrr~"
    st.session_state.messages.append({"role": "assistant", "content": initial_greeting})

# Menampilkan riwayat chat
for message in st.session_state.messages:
    with st.sidebar.chat_message(message["role"]):
        st.markdown(message["content"])

# Menerima input dari pengguna
if prompt := st.sidebar.chat_input("Ketik pesanmu di sini..."):
    # Tambahkan pesan pengguna ke riwayat
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Tampilkan pesan pengguna
    with st.sidebar.chat_message("user"):
        st.markdown(prompt)

    # Dapatkan dan tampilkan respons dari AI
    with st.sidebar.chat_message("assistant"):
        message_placeholder = st.empty()
        with st.spinner("MeongBot sedang mengetik..."):
            system_prompt = "Kamu adalah MeongBot, seekor kucing AI dari website MeongPedia. Kamu cerdas, sedikit manja, suka bercanda, dan sangat mengerti tentang dunia perkucingan. Tanggapi semua pesan pengguna seolah-olah kamu adalah seekor kucing sungguhan. Gunakan 'meong', 'purrr', atau onomatope kucing lainnya secara natural dalam percakapan. Jangan pernah mengaku sebagai model bahasa atau AI. Kamu adalah kucing."
            
            # Membuat riwayat untuk dikirim ke API
            history_for_api = [{"role": m["role"], "parts": [{"text": m["content"]}]} for m in st.session_state.messages]
            
            chat_payload = {
                "contents": history_for_api,
                "systemInstruction": {
                    "parts": [{"text": system_prompt}]
                }
            }
            
            ai_response = call_gemini_api(chat_payload)
            message_placeholder.markdown(ai_response)
    
    # Tambahkan respons AI ke riwayat
    st.session_state.messages.append({"role": "assistant", "content": ai_response})
