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
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
model = genai.GenerativeModel('gemini-1.5-flash')

st.title("🤖 AI Assistent")

# Eén invoerbalk voor alles
user_input = st.text_input("Stel je vraag of plak een YouTube URL:", key="main_input")

if user_input:
    with st.spinner("Analyseert verzoek..."):
        # Logica: Is het een YouTube link?
        if "youtube.com/watch" in user_input or "youtu.be/" in user_input:
            try:
                video_id = user_input.split("v=")[1].split("&")[0] if "v=" in user_input else user_input.split("/")[-1]
                st.video(user_input)
                
                transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['nl', 'en'])
                text = " ".join([i['text'] for i in transcript])
                
                summary = model.generate_content(f"Vat deze video samen: {text[:5000]}").text
                st.markdown("### Samenvatting:")
                st.write(summary)
            except Exception as e:
                st.error("Kon de video niet samenvatten. Controleer de link of ondertiteling.")
        
        # Zo niet, behandel als normale chatvraag
        else:
            try:
                response = model.generate_content(user_input)
                antwoord = response.text
                st.markdown(f"**Antwoord:** {antwoord}")
                
                audio = gTTS(text=antwoord, lang=detect(antwoord))
                buf = io.BytesIO()
                audio.write_to_fp(buf)
                st.audio(buf.getvalue(), format="audio/mp3")
            except Exception as e:
                st.error(f"Fout bij AI: {e}")
