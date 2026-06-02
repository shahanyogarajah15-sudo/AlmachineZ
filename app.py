import streamlit as st
import google.generativeai as genai

# Configuratie
api_key = st.secrets["GEMINI_API_KEY"]
genai.configure(api_key=api_key)

# We gebruiken 'gemini-1.5-flash', dit is momenteel het standaardmodel
model = genai.GenerativeModel('gemini-1.5-flash')

st.title("Mijn AI App")

user_input = st.text_input("Vraag:")
if user_input:
    try:
        response = model.generate_content(user_input)
        st.write(response.text)
    except Exception as e:
        st.write(f"Fout: {e}")
