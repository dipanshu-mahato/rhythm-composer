from fastapi import FastAPI, Form
from fastapi.responses import JSONResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
import os

from lyrics import generate_lyrics
from music import generate_final_music, clean_and_split_sentences, synthesize_audio_for_sentences, SAMPLE_RATE
from scipy.io.wavfile import write as write_wav

app = FastAPI()

# CORS for Streamlit frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Endpoint 1: Generate lyrics
@app.post("/generate-lyrics")
def generate_lyrics_endpoint(prompt: str = Form(...)):
    lyrics = generate_lyrics(prompt)
    
    # Save lyrics to a file
    with open("lyrics.txt", "w", encoding="utf-8") as f:
        f.write(lyrics)

    return JSONResponse(content={"lyrics": lyrics})

# Endpoint 2: Generate final music audio
@app.post("/generate-music")
def generate_music_endpoint(lyrics: str = Form(...)):
    output_file = "final_music.wav"
    generate_final_music(lyrics, output_file)
    return FileResponse(output_file, media_type="audio/wav")

# Endpoint 3: Generate and return audio chunk filenames
@app.get("/generate-chunks")
def generate_chunks_endpoint():
    if not os.path.exists("lyrics.txt"):
        return JSONResponse(content={"error": "Lyrics not found."}, status_code=400)

    with open("lyrics.txt", "r", encoding="utf-8") as f:
        lyrics = f.read()

    sentences = clean_and_split_sentences(lyrics)
    audio_chunks = synthesize_audio_for_sentences(sentences)

    # Return the list of generated chunk filenames
    chunk_files = [f"chunk_{i+1}.wav" for i in range(len(sentences))]
    return JSONResponse(content={"chunks": chunk_files})

# Endpoint 4: Serve a specific audio chunk file
@app.get("/audio/{filename}")
def serve_audio(filename: str):
    file_path = os.path.join(os.getcwd(), filename)
    if os.path.exists(file_path):
        return FileResponse(file_path, media_type="audio/wav")
    else:
        return JSONResponse(content={"error": "File not found."}, status_code=404)
