import streamlit as st
from openai import OpenAI
import base64

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
        st.warning(f"Afbeelding {image_file} niet gevonden.")

# Zorg dat de bestandsnaam exact overeenkomt met wat je op GitHub hebt geüpload
set_background("watermarked_img_14049238449239717308.png") 

# --- AI Logica ---
# Deze regel zoekt naar 'OPENAI_API_KEY' in je Streamlit Secrets
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

def chat_meertalig(gebruikers_input):
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "Jij bent een behulpzame assistent."},
                {"role": "user", "content": gebruikers_input}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Er is een fout opgetreden: {e}"

# --- Streamlit UI ---
st.title("Mijn Meertalige AI")
user_input = st.text_input("Stel je vraag:")

if user_input:
    with st.spinner('De AI denkt na...'):
        antwoord = chat_meertalig(user_input)
        st.write(f"**De AI antwoordt:** {antwoord}")
