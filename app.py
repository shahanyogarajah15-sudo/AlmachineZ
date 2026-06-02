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
