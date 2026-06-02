import streamlit as st
import google.generativeai as genai

# --- Configuratie ---
# Zorg dat GEMINI_API_KEY in je Streamlit Secrets staat
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    
    # We proberen eerst te achterhalen welke modellen beschikbaar zijn
    # Als je een 404 krijgt, printen we de juiste namen in de app
    def get_available_model():
        models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        return models

    available_models = get_available_model()
    
    # Gebruik het eerste model uit de lijst als standaard (meestal gemini-1.5-flash of vergelijkbaar)
    model_name = available_models[0] if available_models else 'gemini-1.5-flash'
    model = genai.GenerativeModel(model_name)
    
except Exception as e:
    st.error(f"Configuratie fout: {e}")
    st.stop()

# --- UI & Logica ---
st.title("Mijn AI App")
st.write(f"Gebruikt model: {model_name}")

user_input = st.text_input("Vraag:")

if user_input:
    with st.spinner('De AI denkt na...'):
        try:
            response = model.generate_content(user_input)
            st.write(f"**De AI antwoordt:** {response.text}")
        except Exception as e:
            st.error(f"Fout tijdens genereren: {e}")
            st.write("Beschikbare modellen die ik zie zijn:", available_models)
