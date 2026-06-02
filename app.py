from openai import OpenAI

client = OpenAI(api_key="JOUW_API_KEY")

def chat_meertalig(gebruikers_input):
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "Jij bent een behulpzame assistent die vloeiend reageert in de taal waarin de gebruiker spreekt. Detecteer de taal automatisch en antwoord in diezelfde taal."},
            {"role": "user", "content": gebruikers_input}
        ]
    )
    return response.choices[0].message.content

# Test
print(chat_meertalig("Hoe werkt een database?"))
print(chat_meertalig("How does a database work?"))
print(chat_meertalig("¿Cómo funciona una base de datos?"))

import streamlit as st

st.title("Mijn Meertalige AI")

# Input veld
user_input = st.text_input("Stel je vraag:")

if user_input:
    # Hier roep je jouw AI-logica aan
    st.write(f"De AI antwoordt: [Hier komt jouw AI antwoord in de juiste taal]")