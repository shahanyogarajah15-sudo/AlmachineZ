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
            # Aangescherpte instructie: dwingt de AI om in de gekozen taal te antwoorden
            volledige_prompt = f"Antwoord uitsluitend in het {taal_keuze}. Vraag: {user_input}"
            
            response = model.generate_content(volledige_prompt)
            tekst = response.text
            
            # Toon het antwoord in het zwarte kader
            st.markdown(
                f"""
                <div style="background-color: rgba(0, 0, 0, 0.7); padding: 20px; border-radius: 10px; color: white;">
                    <h4 style="color: white;">De AI antwoordt:</h4>
                    <p>{tekst.replace(chr(10), '<br>')}</p>
                </div>
                """, 
                unsafe_allow_html=True
            )
            
            # Tekst uitspreken
            tts = gTTS(text=tekst, lang=talen_code[taal_keuze])
            audio_buffer = io.BytesIO()
            tts.write_to_fp(audio_buffer)
            
            st.audio(audio_buffer, format='audio/mp3')
            
        except Exception as e:
            # Als er een quota fout is, zie je dat hier
            st.error(f"Foutmelding (mogelijk quota bereikt): {e}")
