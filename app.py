import streamlit as st
import google.generativeai as genai
import base64

# --- Configuratie van Gemini ---
# Zorg dat je GEMINI_API_KEY in je Streamlit Secrets staat
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# We gebruiken nu 'gemini-1.5-flash' omdat dit het juiste model is
model = genai.GenerativeModel('gemini-1.5-flash')

# --- Achtergrond instellen ---
def set_background(image_file):
    try:
        with open(image_file, "rb") as f:
            img_data = f.read()
        b64_encoded = base64.b64encode(img_data).decode()
        style = f"""
        <style>
        [data-testid="stAppViewContainer"] > .main {{
            background-image: url("data:image/png;base64,{b64_encoded}");
            background-size: cover;
            background-position: center;
        }}
        </style>
        """
        st.markdown(style, unsafe_allow_html=True)
    except FileNotFoundError:
        st.warning(f"Afbeelding '{image_file}' niet gevonden. Controleer de bestandsnaam in GitHub.")

# --- UI & Logica ---
st.title("Mijn Meertalige AI (Gemini)")

# PAS DIT AAN: Zorg dat deze naam exact matcht met je bestand in GitHub
# Als je de afbeelding niet ziet, haal dan de volgende regel weg door er een # voor te zetten
set_background("watermarked_img_14049238449239717308.png") 

def chat_meertalig(gebruikers_input):
    try:
        response = model.generate_content(gebruikers_input)
        return response.text
    except Exception as e:
        return f"Er is een fout opgetreden: {e}"

user_input = st.text_input("Stel je vraag:")

if user_input:
    with st.spinner('De AI denkt na...'):
        antwoord = chat_meertalig(user_input)
        st.write(f"**De AI antwoordt:** {antwoord}")
