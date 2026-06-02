import streamlit as st
import google.generativeai as genai

# Configuratie
api_key = st.secrets["GEMINI_API_KEY"]
genai.configure(api_key=api_key)

# We gebruiken nu de naam die we zojuist hebben gevonden!
model = genai.GenerativeModel('models/gemini-2.5-flash')

st.title("Mijn Meertalige AI")

user_input = st.text_input("Stel je vraag:")

if user_input:
    with st.spinner('De AI denkt na...'):
        try:
            response = model.generate_content(user_input)
            st.write(f"**De AI antwoordt:** {response.text}")
        except Exception as e:
            st.error(f"Er ging iets mis: {e}")
