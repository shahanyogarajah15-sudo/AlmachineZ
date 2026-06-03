import streamlit as st
import google.generativeai as genai
import googlemaps
from datetime import datetime
import base64
from gtts import gTTS
import io
from langdetect import detect

# --- Configuratie ---
# Zorg dat deze keys in je Streamlit Secrets staan
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
gmaps = googlemaps.Client(key=st.secrets["GOOGLE_MAPS_API_KEY"])
model = genai.GenerativeModel('models/gemini-2.0-flash') # Gebruik een actueel model

# --- Functies ---
def get_live_traffic(origin, destination):
    try:
        now = datetime.now()
        directions = gmaps.directions(origin, destination, mode="driving", departure_time=now)
        if directions:
            route = directions[0]['legs'][0]
            return f"Reistijd met verkeer: {route['duration_in_traffic']['text']}. (Zonder verkeer: {route['duration']['text']}). Afstand: {route['distance']['text']}."
        return "Kon geen route vinden."
    except Exception as e:
        return f"Verkeersinfo kon niet worden opgehaald: {str(e)}"

# --- App Interface ---
st.set_page_config(page_title="Meertalige AI Routeplanner", layout="centered")
st.title("🌍 Meertalige AI Routeplanner")

user_input = st.text_input("Vraag een route (bijv: 'Hoe kom ik van Amsterdam naar Utrecht?'):")

if user_input:
    with st.spinner("AI en verkeersgegevens analyseren..."):
        try:
            # 1. Haal de steden uit de input via de AI
            extraction_prompt = f"Extraheer de 'van' stad en de 'naar' stad uit deze zin: '{user_input}'. Geef alleen de steden terug in dit formaat: 'StadA|StadB'"
            locations = model.generate_content(extraction_prompt).text.strip().split('|')
            
            if len(locations) == 2:
                origin, dest = locations[0], locations[1]
                verkeer_info = get_live_traffic(origin, dest)
            else:
                verkeer_info = "Kon locaties niet duidelijk herkennen."

            # 2. Vraag AI om een vriendelijk antwoord
            final_prompt = f"De gebruiker vraagt: '{user_input}'. De live verkeersinfo is: {verkeer_info}. Antwoord in de taal van de vraag en geef een natuurlijk reisadvies."
            response = model.generate_content(final_prompt)
            tekst = response.text
            
            # 3. Toon het antwoord
            st.markdown(f'<div style="background-color: rgba(0,0,0,0.7); padding:20px; border-radius:10px; color:white;">{tekst}</div>', unsafe_allow_html=True)
            
            # 4. Audio genereren
            try:
                lang_code = detect(tekst)
            except:
                lang_code = 'nl'
            
            tts = gTTS(text=tekst, lang=lang_code)
            audio_buffer = io.BytesIO()
            tts.write_to_fp(audio_buffer)
            audio_buffer.seek(0)
            st.audio(audio_buffer, format="audio/mp3")
            
        except Exception as e:
            st.error(f"Er ging iets mis: {e}")
