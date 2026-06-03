import streamlit as st
import google.generativeai as genai
from gtts import gTTS
import io
from langdetect import detect
from youtube_transcript_api import YouTubeTranscriptApi

# --- Achtergrondinstellingen ---
# We gebruiken een stijlelement dat direct wordt ingevoegd
st.markdown(
    """
    <style>
    .stApp {
        background-image: url("https://images.unsplash.com/photo-1639322537228-f710d846310a?q=80&w=2500&auto=format&fit=crop");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# --- Configuratie ---
# Zorg dat GEMINI_API_KEY in je Streamlit Secrets staat
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# We gebruiken hier 'gemini-1.5-flash'. 
# Mocht je een 404 blijven krijgen, controleer dan in Google AI Studio
# of je account correct is geactiveerd (ga naar aistudio.google.com).
model = genai.GenerativeModel('gemini-1.5-flash')

st.title("🤖 AI Assistent")
st.markdown("---")

# Eén invoerbalk voor alles
user_input = st.text_input("Stel je vraag of plak een YouTube URL:", key="main_input")

if user_input:
    with st.spinner("Analyseert verzoek..."):
        # Logica: YouTube-link detectie
        if "youtube.com/watch" in user_input or "youtu.be/" in user_input:
            try:
                # Video ID extractie
                video_id = user_input.split("v=")[1].split("&")[0] if "v=" in user_input else user_input.split("/")[-1]
                st.video(user_input)
                
                # Transcript ophalen
                transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['nl', 'en'])
                text = " ".join([i['text'] for i in transcript])
                
                # Samenvatten
                summary = model.generate_content(f"Vat deze video samen: {text[:5000]}").text
                st.markdown("### Samenvatting:")
                st.write(summary)
            except Exception as e:
                st.error("Kon de video niet samenvatten. Zorg dat er ondertiteling beschikbaar is.")
        
        # Normale chatvraag
        else:
            try:
                response = model.generate_content(user_input)
                antwoord = response.text
                st.markdown(f"**Antwoord:** {antwoord}")
                
                # Audio genereren
                audio = gTTS(text=antwoord, lang=detect(antwoord))
                buf = io.BytesIO()
                audio.write_to_fp(buf)
                st.audio(buf.getvalue(), format="audio/mp3")
            except Exception as e:
                st.error(f"Fout bij AI: {e}")
