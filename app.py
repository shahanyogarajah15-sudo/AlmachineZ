import streamlit as st
import google.generativeai as genai
from gtts import gTTS
import io
from langdetect import detect
from youtube_transcript_api import YouTubeTranscriptApi

# --- Achtergrondinstellingen ---
page_bg_img = '''
<style>
.stApp {
background-image: url("https://images.unsplash.com/photo-1639322537228-f710d846310a?q=80&w=2500&auto=format&fit=crop");
background-size: cover;
}
</style>
'''
st.markdown(page_bg_img, unsafe_allow_html=True)

# --- Configuratie ---
# Zorg dat je GEMINI_API_KEY in je Streamlit Secrets staat
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
model = genai.GenerativeModel('gemini-1.5-flash')

# --- App Interface ---
st.title("🤖 AI Assistent")
st.markdown("---")

# 1. Chat Gedeelte
st.subheader("💬 Stel je vraag aan de AI")
user_input = st.text_input("Typ hier je vraag:", key="chat_input")
if user_input:
    with st.spinner("AI denkt na..."):
        try:
            response = model.generate_content(user_input)
            antwoord = response.text
            st.markdown(f"**Antwoord:** {antwoord}")
            
            # Audio voorlezen
            audio = gTTS(text=antwoord, lang=detect(antwoord))
            buf = io.BytesIO()
            audio.write_to_fp(buf)
            st.audio(buf.getvalue(), format="audio/mp3")
        except Exception as e:
            st.error(f"Fout bij AI: {e}")

st.markdown("---")

# 2. YouTube Gedeelte
st.subheader("▶️ YouTube Samenvatting")
yt_url = st.text_input("Plak hier je YouTube URL:", key="yt_input")
if yt_url:
    try:
        # Video ID extraheren
        video_id = yt_url.split("v=")[1].split("&")[0] if "v=" in yt_url else yt_url.split("/")[-1]
        st.video(yt_url)
        
        with st.spinner("Video analyseren..."):
            transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['nl', 'en'])
            text = " ".join([i['text'] for i in transcript])
            
            summary = model.generate_content(f"Vat deze video samen: {text[:5000]}").text
            st.markdown("### Samenvatting:")
            st.write(summary)
    except Exception as e:
        st.error("Kon de video niet samenvatten. Controleer of de video ondertiteling heeft.")
