import streamlit as st
import google.generativeai as genai
import base64
from gtts import gTTS
import io

# --- Functie voor achtergrond ---
def set_background(image_file):
    try:
        with open(image_file, "rb") as f:
            img_data = f.read()
        b64_encoded = base64.b64encode(img_data).decode()
        style = f"""
        <style>
        .stApp {{
            background-image: url("data:image/png;base64,{b64_encoded}");
            background-size: cover;
            background-position: center;
        }}
        </style>
        """
        st.markdown(style, unsafe_allow_html=True)
    except FileNotFoundError:
        pass

# --- Configuratie ---
api_key = st.secrets["GEMINI_API_KEY"]
genai.configure(api_key=api_key)
model = genai.GenerativeModel('models/gemini-2.5-flash')

# --- Achtergrond ---
set_background("Gemini_Generated_Image_g94fxbg94fxbg94f.png")

# --- UI ---
st.title("Mijn Meertalige AI")

# Taal selectie
taal_keuze = st.selectbox("Kies de taal:", ["Nederlands", "English", "Français", "Deutsch", "Español"])
talen_code = {"Nederlands": "nl", "English": "en", "Français": "fr", "Deutsch": "de", "Español": "es"}

user_input = st.text_input("Stel je vraag:")

if user_input:
    with st.spinner('De AI denkt na...'):
        try:
            # Vraag aan de AI om in de gekozen taal te antwoorden
            prompt = f"Antwoord in het {taal_keuze}: {user_input}"
            response = model.generate_content(prompt)
            tekst = response.text
            
            # Toon het antwoord in het zwarte kader
            st.markdown(
                f"""
                <div style="background-color: rgba(0, 0, 0, 0.7); padding: 20px; border-radius: 10px; color: white;">
                    <p>{tekst.replace(chr(10), '<br>')}</p>
                </div>
                """, 
                unsafe_allow_html=True
            )
            
            # Tekst uitspreken (Audio genereren)
            tts = gTTS(text=tekst, lang=talen_code[taal_keuze])
            audio_buffer = io.BytesIO()
            tts.write_to_fp(audio_buffer)
            
            st.audio(audio_buffer, format='audio/mp3')
            
        except Exception as e:
            st.error(f"Er ging iets mis: {e}")
