import streamlit as st
import requests
import os

st.set_page_config(page_title="AI Music Generator", page_icon="🎵")

st.title("🎤 AI Music Generator")

# Prompt input
prompt = st.text_area("Enter a prompt for the song lyrics:")

# Generate Lyrics
if st.button("Generate Lyrics"):
    with st.spinner("Generating lyrics..."):
        response = requests.post("http://localhost:8000/generate-lyrics", data={"prompt": prompt})
        if response.status_code == 200:
            lyrics = response.json()["lyrics"]
            st.text_area("Generated Lyrics", lyrics, height=200)

            # Save lyrics to file for backend
            with open("lyrics.txt", "w", encoding="utf-8") as f:
                f.write(lyrics)

            # Trigger audio generation
            if st.button("🎵 Generate Full Audio"):
                with st.spinner("Generating full music..."):
                    audio_response = requests.post("http://localhost:8000/generate-music", data={"lyrics": lyrics})
                    if audio_response.status_code == 200:
                        with open("final_music.wav", "wb") as f:
                            f.write(audio_response.content)
                        st.audio("final_music.wav", format="audio/wav")
                    else:
                        st.error("Failed to generate full music.")

            # Trigger chunk generation
            if st.button("🎧 Generate & Play Sentence Chunks"):
                with st.spinner("Generating audio chunks..."):
                    chunk_response = requests.get("http://localhost:8000/generate-chunks")
                    if chunk_response.status_code == 200:
                        chunks = chunk_response.json()["chunks"]
                        for chunk in chunks:
                            st.audio(f"http://localhost:8000/audio/{chunk}", format="audio/wav")
                    else:
                        st.error("Failed to generate audio chunks.")
        else:
            st.error("Error generating lyrics. Try again.")
