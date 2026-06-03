import streamlit as st
import google.generativeai as genai
import googlemaps
from gtts import gTTS
import io
from langdetect import detect

# --- Configuratie ---
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
gmaps = googlemaps.Client(key=st.secrets["GOOGLE_MAPS_API_KEY"])
model = genai.GenerativeModel('gemini-1.5-flash')

st.title("🤖 AI Assistent")
st.markdown("---")

# 1. Chat & Route Advies
st.subheader("💬 Chat & Route Advies")
user_input = st.text_input("Stel je vraag:")

if user_input:
    with st.spinner("AI denkt na..."):
        try:
            # AI genereert antwoord
            response = model.generate_content(user_input)
            antwoord = response.text
            st.markdown(f"**Antwoord:** {antwoord}")
            
            # Audio voorlezen
            audio = gTTS(text=antwoord, lang=detect(antwoord))
            buf = io.BytesIO()
            audio.write_to_fp(buf)
            st.audio(buf.getvalue(), format="audio/mp3")
        except Exception as e:
            st.error(f"Fout: {e}")
