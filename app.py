import streamlit as st
import google.generativeai as genai
import base64
from gtts import gTTS
import io
from langdetect import detect

# --- Achtergrond instellen ---
def set_background(image_file):
    try:
        with open(image_file, "rb") as f:
            img_data = f.read()
        b64_encoded = base64.b64encode(img_data).decode()
        st.markdown(
            f"""
            <style>
            .stApp {{
                background-image: url("data:image/png;base64,{b64_encoded}");
                background-size: cover;
                background-position: center;
            }}
            h3, p { color: white !important; }
            </style>
            """,
            unsafe_allow_html=True,
        )
    except:
        pass

# --- Setup ---
st.set_page_config(page_title="Meertalige AI", layout="centered")
set_background("Gemini_Generated_Image_g94fxbg94fxbg94f.png")

api_key = st.secrets["GEMINI_API_KEY"]
genai.configure(api_key=api_key)
model = genai.GenerativeModel('models/gemini-2.5-flash')

st.title("🌍 Mijn Meertalige AI")
user_input = st.text_input("Stel je vraag in elke gewenste taal:")

if user_input:
    with st.spinner("De AI denkt na..."):
        try:
            # Vraag de AI om te antwoorden in de taal van de invoer
            prompt = f"Beantwoord de volgende vraag in de taal waarin de vraag gesteld is: {user_input}"
            response = model.generate_content(prompt)
            tekst = response.text
            
            # Toon antwoord
            st.markdown(f'<div style="background-color: rgba(0,0,0,0.7); padding:20px; border-radius:10px; color:white;">{tekst}</div>', unsafe_allow_html=True)
            
            # Automatische taalherkenning voor audio
            try:
                taal_code = detect(tekst)
            except:
                taal_code = 'en'
            
            # Audio genereren
            tts = gTTS(text=tekst, lang=taal_code)
            audio_buffer = io.BytesIO()
            tts.write_to_fp(audio_buffer)
            audio_buffer.seek(0)
            st.audio(audio_buffer, format="audio/mp3")
            
        except Exception as e:
            st.error(f"Foutmelding: {e}")
