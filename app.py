import streamlit as st
import google.generativeai as genai
import os
import tempfile
from dotenv import load_dotenv
load_dotenv()

genai.configure(api_key=os.environ['GOOGLE_API_KEY'])

st.header("Audiologix Intelligence: Unveiling the Hidden Insights from Audio")

prompt = """
Listen the provided audio file carefully and provide key points from the audio file.
"""

with st.expander("About this app"):
    st.write("""
        This app uses Google's generative AI to provide key insights from audio files. 
        Upload your audio file in WAV or MP3 format and get a key insights of its content.
    """)

def key_insights_audio(audio_file_path):
    model = genai.GenerativeModel("models/gemini-1.5-pro-latest")
    audio_file = genai.upload_file(path=audio_file_path)
    response = model.generate_content(
        [
            prompt,
            audio_file
        ]
    )
    return response.text

def save_uploaded_file(uploaded_file):
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix='.' + uploaded_file.name.split('.')[-1]) as tmp_file:
            tmp_file.write(uploaded_file.getvalue())
            return tmp_file.name
    except Exception as e:
        st.error(f"Error handling uploaded file: {e}")
        return None
    
uploaded_file = st.file_uploader("Choose an Audio file",type=['.mp3','.wav'])

if uploaded_file is not None:
    audio_path = save_uploaded_file(uploaded_file)
    st.audio(audio_path)

    if st.button("See Insights"):
        with st.spinner("Processing.."):
            response = key_insights_audio(audio_path)
            st.info(response)

