import streamlit as st
import google.generativeai as genai
import base64
from gtts import gTTS
import io

# ==========================================
# ACHTERGROND INSTELLEN
# ==========================================
def set_background(image_file):
    try:
        with open(image_file, "rb") as f:
            img_data = f.read()

        b64_encoded = base64.b64encode(img_data).decode()

        page_bg = f"""
        <style>
        .stApp {{
            background-image: url("data:image/png;base64,{b64_encoded}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
        }}

        h1, h2, h3, h4, h5, h6, label {{
            color: white !important;
        }}

        .stTextInput > div > div > input {{
            background-color: rgba(0,0,0,0.7);
            color: white;
        }}

        .stSelectbox > div > div {{
            background-color: rgba(0,0,0,0.7);
            color: white;
        }}
        </style>
        """

        st.markdown(page_bg, unsafe_allow_html=True)

    except FileNotFoundError:
        st.warning("Achtergrondafbeelding niet gevonden.")


# ==========================================
# GEMINI CONFIGURATIE
# ==========================================
api_key = st.secrets["GEMINI_API_KEY"]

genai.configure(api_key=api_key)

model = genai.GenerativeModel(
    "models/gemini-2.5-flash"
)

# ==========================================
# ACHTERGROND LADEN
# ==========================================
set_background("Gemini_Generated_Image_g94fxbg94fxbg94f.png")

# ==========================================
# TITEL
# ==========================================
st.title("🌍 Mijn Meertalige AI")

# ==========================================
# TALEN
# ==========================================
taal_keuze = st.selectbox(
    "Kies de taal:",
    [
        "Nederlands",
        "English",
        "Français",
        "Deutsch",
        "Español"
    ]
)

talen_code = {
    "Nederlands": "nl",
    "English": "en",
    "Français": "fr",
    "Deutsch": "de",
    "Español": "es"
}

# ==========================================
# INPUT
# ==========================================
user_input = st.text_input("Stel je vraag:")

# ==========================================
# AI ANTWOORD
# ==========================================
if user_input:

    with st.spinner("De AI denkt na..."):

        try:

            prompt = f"""
Je bent een professionele meertalige assistent.

BELANGRIJKE REGELS:
- Antwoord uitsluitend in {taal_keuze}.
- Gebruik geen andere taal.
- Geef een natuurlijk antwoord.
- Wees duidelijk en behulpzaam.

Vraag:
{user_input}
"""

            response = model.generate_content(prompt)

            tekst = response.text.strip()

            # ==========================================
            # ANTWOORD WEERGEVEN
            # ==========================================
            st.markdown(
                f"""
                <div style="
                    background-color: rgba(0,0,0,0.75);
                    padding:20px;
                    border-radius:12px;
                    color:white;
                    margin-top:15px;
                ">
                    <h3>🤖 De AI antwoordt:</h3>
                    <p>{tekst.replace(chr(10), '<br>')}</p>
                </div>
                """,
                unsafe_allow_html=True
            )

            # ==========================================
            # AUDIO GENEREREN
            # ==========================================
            tts = gTTS(
                text=tekst,
                lang=talen_code[taal_keuze]
            )

            audio_buffer = io.BytesIO()

            tts.write_to_fp(audio_buffer)

            audio_buffer.seek(0)

            # Normale speler
            st.audio(audio_buffer, format="audio/mp3")

            # ==========================================
            # AUTOPLAY
            # ==========================================
            audio_buffer.seek(0)

            audio_b64 = base64.b64encode(
                audio_buffer.read()
            ).decode()

            audio_html = f"""
            <audio autoplay>
                <source src="data:audio/mp3;base64,{audio_b64}" type="audio/mp3">
            </audio>
            """

            st.markdown(audio_html, unsafe_allow_html=True)

        except Exception as e:

            error_text = str(e)

            if "429" in error_text:
                st.error(
                    "⚠️ Gemini API quota bereikt. "
                    "Wacht even of upgrade je Google AI-plan."
                )
            else:
                st.error(f"❌ Fout: {error_text}")
