import streamlit as st  # Zorg dat deze bovenaan staat
from openai import OpenAI

# Gebruik de sleutel uit de Secrets die je zojuist hebt opgeslagen
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

def chat_meertalig(gebruikers_input):
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "Jij bent een behulpzame assistent die vloeiend reageert in de taal waarin de gebruiker spreekt"},
            {"role": "user", "content": gebruikers_input}
        ]
    )
    return response.choices[0].message.content

st.title("Mijn Meertalige AI")

# Input veld
user_input = st.text_input("Stel je vraag:")

if user_input:
    # Roep hier je AI-functie aan en toon het resultaat
    antwoord = chat_meertalig(user_input)
    st.write(f"De AI antwoordt: {antwoord}")

import streamlit as st
import base64

def get_base64_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

image_base64 = get_base64_image("HET_BESTANDSPAD_NAAR_JE_AFBEELDING.png")

page_bg_img = f"""
<style>
[data-testid="stAppViewContainer"] > .main {{
    background-image: url("data:image/png;base64,{image_base64}");
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
    background-attachment: local;
}}
</style>
"""

st.markdown(page_bg_img, unsafe_allow_html=True)
