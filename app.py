import streamlit as st
import google.generativeai as genai
import googlemaps
from datetime import datetime
import base64
from gtts import gTTS
import io
from langdetect import detect

# --- Configuratie ---
gmaps = googlemaps.Client(key=st.secrets["GOOGLE_MAPS_API_KEY"])
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
model = genai.GenerativeModel('models/gemini-2.5-flash')

# --- Functie voor live verkeer ---
def get_live_traffic(origin, destination):
    try:
        now = datetime.now()
        directions = gmaps.directions(origin, destination, mode="driving", departure_time=now)
        if directions:
            route = directions[0]['legs'][0]
            return f"Actuele reistijd: {route['duration_in_traffic']['text']}. (Zonder verkeer: {route['duration']['text']}). Afstand: {route['distance']['text']}."
        return "Kon geen route vinden."
    except Exception as e:
        return f"Kon verkeersinfo niet ophalen: {e}"

# --- UI & Logica ---
st.title("🌍 Meertalige AI Routeplanner")
user_input = st.text_input("Vraag een route (bijv: 'route van Amsterdam naar Utrecht'):")

if user_input:
    with st.spinner("Kaartgegevens en verkeer analyseren..."):
        # 1. Haal verkeersinfo op (Je moet de steden uit de input halen)
        # Voor dit voorbeeld gaan we uit van een eenvoudige parsing
        # In een echte app zou je de AI kunnen vragen de steden uit de input te halen
        origin = "Amsterdam" # Placeholder - dit moet dynamisch uit user_input komen
        dest = "Utrecht"     # Placeholder
        
        verkeer_info = get_live_traffic(origin, dest)
        
        # 2. Vraag AI om antwoord te formuleren
        prompt = f"De gebruiker vraagt: '{user_input}'. De actuele verkeersinfo is: {verkeer_info}. Geef een vriendelijk antwoord in de taal van de vraag."
        response = model.generate_content(prompt)
        tekst = response.text
        
        # 3. Tonen en Audio
        st.markdown(f'<div style="background-color: rgba(0,0,0,0.7); padding:20px; color:white;">{tekst}</div>', unsafe_allow_html=True)
        
        tts = gTTS(text=tekst, lang=detect(tekst))
        audio_buffer = io.BytesIO()
        tts.write_to_fp(audio_buffer)
        audio_buffer.seek(0)
        st.audio(audio_buffer, format="audio/mp3")
