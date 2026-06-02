import streamlit as st
import google.generativeai as genai

# --- Configuratie ---
try:
    # Haal je sleutel op uit Secrets
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)

    # We proberen expliciet het model 'gemini-1.5-flash' te gebruiken
    # Mocht dat echt niet lukken, dan proberen we de lijst op te vragen
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error(f"Configuratie-fout: {e}")
    st.stop()

# --- UI ---
st.title("Mijn AI App")

user_input = st.text_input("Stel je vraag:")

if user_input:
    with st.spinner('De AI denkt na...'):
        try:
            # Stuur de vraag naar het model
            response = model.generate_content(user_input)
            st.write(f"**De AI antwoordt:** {response.text}")
        except Exception as e:
            st.error(f"Er ging iets mis met het model: {e}")
            st.write("Tip: Als je een 404 ziet, is het model 'gemini-1.5-flash' niet toegankelijk voor deze sleutel.")
