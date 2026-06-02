import streamlit as st
import google.generativeai as genai

# --- Configuratie ---
# We halen de sleutel op
api_key = st.secrets["GEMINI_API_KEY"]
genai.configure(api_key=api_key)

# We proberen nu een algemene 'gemini-pro' aanroep
model = genai.GenerativeModel('gemini-pro')

# --- UI & Logica ---
st.title("Mijn Meertalige AI (Gemini)")

def chat_meertalig(gebruikers_input):
    try:
        response = model.generate_content(gebruikers_input)
        return response.text
    except Exception as e:
        return f"Er is een fout opgetreden bij de API-aanroep: {e}"

user_input = st.text_input("Stel je vraag:")

if user_input:
    with st.spinner('De AI denkt na...'):
        antwoord = chat_meertalig(user_input)
        st.write(f"**De AI antwoordt:** {antwoord}")
