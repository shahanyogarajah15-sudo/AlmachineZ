import streamlit as st
import google.generativeai as genai
from gtts import gTTS
import io
from langdetect import detect
from youtube_transcript_api import YouTubeTranscriptApi

# --- Configuratie ---
# Je hebt nu alleen nog de Gemini API sleutel nodig
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
model = genai.GenerativeModel('gemini-1.5-flash')

st.title("🤖 AI Assistent: Vragen & Video's")

# --- Tabs ---
tab1, tab2 = st.tabs(["💬 Chat & Advies", "▶️ YouTube Samenvatting"])

with tab1:
    user_input = st.text_input("Stel je vraag:")
    if user_input:
        with st.spinner("AI denkt na..."):
            # AI genereert antwoord
            response = model.generate_content(user_input)
            antwoord = response.text
            st.markdown(f"**Antwoord:** {antwoord}")
            
            # Audio voorlezen
            audio = gTTS(text=antwoord, lang=detect(antwoord))
            buf = io.BytesIO()
            audio.write_to_fp(buf)
            st.audio(buf.getvalue(), format="audio/mp3")

with tab2:
    yt_url = st.text_input("Plak een YouTube URL:")
    if yt_url:
        try:
            video_id = yt_url.split("v=")[1].split("&")[0]
            st.video(yt_url)
            
            # Transcript ophalen
            transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['nl', 'en'])
            text = " ".join([i['text'] for i in transcript])
            
            # AI Samenvatting
            summary = model.generate_content(f"Vat deze video samen: {text[:5000]}").text
            st.markdown("### Samenvatting:")
            st.write(summary)
        except Exception as e:
            st.error("Kon de video niet samenvatten. Controleer of de video ondertiteling heeft.")
