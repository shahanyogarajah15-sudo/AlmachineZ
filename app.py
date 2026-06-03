import streamlit as st
import google.generativeai as genai
import base64
from gtts import gTTS
import io

# ==========================================
# ACHTERGROND
# ==========================================
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
                background-repeat: no-repeat;
            }}

            h1, h2, h3, h4, h5, h6, label {{
                color: white !important;
            }}

            .stTextInput input {{
                color: white !important;
                background-color: rgba(0,0,0,0.6) !important;
            }}
            </style>
            """,
            unsafe_allow_html=True,
        )

    except FileNotFoundError:
        st.warning("Achtergrondafbeelding niet gevonden.")


# ==========================================
# PAGINA
# ==========================================
st.set_page_config(
    page_title="Mijn Meertalige AI",
    page_icon="🌍",
    layout="centered"
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
# TAALKEUZE
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
# GEMINI INITIALISEREN
# ==========================================
gemini_beschikbaar = True

try:
    api_key = st.secrets["GEMINI_API_KEY"]

    genai.configure(api_key=api_key)

    model = genai.GenerativeModel(
        "models/gemini-2.5-flash"
    )

except Exception:
    gemini_beschikbaar = False

# ==========================================
# INPUT
# ==========================================
user_input = st.text_input("Stel je vraag:")

# ==========================================
# AI
# ==========================================
if user_input:

    with st.spinner("De AI denkt na..."):

        try:

            if gemini_beschikbaar:

                prompt = f"""
Je bent een professionele AI-assistent.

BELANGRIJK:
- Antwoord uitsluitend in {taal_keuze}.
- Gebruik geen andere taal.
- Geef een natuurlijk antwoord.
- Vertaal indien nodig naar de gekozen taal.

Vraag:
{user_input}
"""

                response = model.generate_content(prompt)

                tekst = response.text.strip()

            else:

                tekst = {
                    "Nederlands":
                        "Dit is een testantwoord omdat Gemini momenteel niet beschikbaar is.",

                    "English":
                        "This is a test response because Gemini is currently unavailable.",

                    "Français":
                        "Ceci est une réponse de test car Gemini est actuellement indisponible.",

                    "Deutsch":
                        "Dies ist eine Testantwort, da Gemini derzeit nicht verfügbar ist.",

                    "Español":
                        "Esta es una respuesta de prueba porque Gemini no está disponible actualmente."
                }[taal_keuze]

            # ==========================================
            # ANTWOORD TONEN
            # ==========================================
            st.markdown(
                f"""
                <div style="
                    background-color: rgba(0,0,0,0.75);
                    padding:20px;
                    border-radius:15px;
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

            # Audioplayer tonen
            st.audio(audio_buffer, format="audio/mp3")

            # ==========================================
            # AUTOPLAY AUDIO
            # ==========================================
            audio_buffer.seek(0)

            audio_b64 = base64.b64encode(
                audio_buffer.read()
            ).decode()

            st.markdown(
                f"""
                <audio autoplay>
                    <source src="data:audio/mp3;base64,{audio_b64}" type="audio/mp3">
                </audio>
                """,
                unsafe_allow_html=True
            )

        except Exception as e:

            error_text = str(e)

            if "429" in error_text:

                st.error(
                    "⚠️ Gemini quota bereikt. De gratis limiet is opgebruikt. Probeer later opnieuw."
                )

            else:

                st.error(
                    f"❌ Foutmelding: {error_text}"
                )
