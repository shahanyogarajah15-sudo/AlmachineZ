import streamlit as st
from openai import OpenAI
import base64

# --- Achtergrond instellen ---
# Tip: Upload een afbeelding (bijv. 'achtergrond.png') naar je repository 
# en verander de bestandsnaam hieronder.
def set_background(image_file):
    with open(image_file, "rb") as f:
        img_data = f.read()
    b64_encoded = base64.b64encode(img_data).decode()
    style = f"""
    <style>
    [data-testid="stAppViewContainer"] > .main {{
        background-image: url("data:image/png;base64,{b64_encoded}");
        background-size: cover;
    }}
    </style>
    """
    st.markdown(style, unsafe_allow_html=True)

# Als je nog geen bestand hebt, kun je deze regel uitvinken door een # ervoor te zetten:
# set_background("achtergrond.png") 

# --- AI Logica ---
# Haalt de API-sleutel veilig op uit de Streamlit Secrets
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

def chat_meertalig(gebruikers_input):
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "Jij bent een behulpzame assistent die vloeiend reageert in de taal waarin de gebruiker spreekt."},
            {"role": "user", "content": gebruikers_input}
        ]
    )
    return response.choices[0].message.content

# --- Streamlit UI ---
st.title("Mijn Meertalige AI")

# Input veld
user_input = st.text_input("Stel je vraag:")

if user_input:
    with st.spinner('De AI denkt na...'):
        antwoord = chat_meertalig(user_input)
        st.write(f"**De AI antwoordt:** {antwoord}")
