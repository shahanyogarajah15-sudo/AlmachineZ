import streamlit as st
import google.generativeai as genai

# --- Configuratie ---
# Zorg dat je in Streamlit 'Settings > Secrets' de GEMINI_API_KEY hebt ingevoerd!
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    # We gebruiken 'gemini-1.5-flash' als gratis model
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error(f"Fout bij configuratie: {e}")

# --- UI & Logica ---
st.title("Mijn Meertalige AI (Gemini)")

# De achtergrondafbeelding is uitgeschakeld om crashes te voorkomen
# # set_background("watermarked_img_14049238449239717308.png") 

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
