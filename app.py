import streamlit as st
import google.generativeai as genai
import base64

# --- Functie voor achtergrond ---
def set_background(image_file):
    try:
        with open(image_file, "rb") as f:
            img_data = f.read()
        b64_encoded = base64.b64encode(img_data).decode()
        style = f"""
        <style>
        .stApp {{
            background-image: url("data:image/png;base64,{b64_encoded}");
            background-size: cover;
            background-position: center;
        }}
        </style>
        """
        st.markdown(style, unsafe_allow_html=True)
    except FileNotFoundError:
        st.error(f"Afbeelding {image_file} niet gevonden.")

# --- Configuratie ---
# Zorg dat GEMINI_API_KEY in je Streamlit Secrets staat!
api_key = st.secrets["GEMINI_API_KEY"]
genai.configure(api_key=api_key)

# We gebruiken het werkende model
model = genai.GenerativeModel('models/gemini-2.5-flash')

# --- Achtergrond ---
# Zorg dat de bestandsnaam exact overeenkomt met de foto op GitHub
set_background("Gemini_Generated_Image_g94fxbg94fxbg94f.png")

# --- UI ---
st.title("Mijn Meertalige AI")

user_input = st.text_input("Stel je vraag:")

if user_input:
    with st.spinner('De AI denkt na...'):
        try:
            response = model.generate_content(user_input)
            
            # Zwart kader voor betere leesbaarheid
            st.markdown(
                f"""
                <div style="background-color: rgba(0, 0, 0, 0.7); padding: 20px; border-radius: 10px; color: white;">
                    <h4 style="color: white;">De AI antwoordt:</h4>
                    <p>{response.text.replace(chr(10), '<br>')}</p>
                </div>
                """, 
                unsafe_allow_html=True
            )
        except Exception as e:
            st.error(f"Er ging iets mis: {e}")
