import streamlit as st
import google.generativeai as genai

st.title("API Model Checker")

# API Configuratie
try:
    # Zorg dat je GEMINI_API_KEY in je Streamlit Secrets staat!
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
    
    # Haal alle beschikbare modellen op
    models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
    
    st.write("### Beschikbare modellen voor jouw sleutel:")
    st.write(models)
    
    if models:
        st.write("---")
        st.write("Kopieer een van deze namen en gebruik die in je echte app:")
        st.code(models[0])
        
except Exception as e:
    st.error(f"Fout bij verbinden met API. Controleer je Secrets!")
    st.write(f"Foutmelding: {e}")
