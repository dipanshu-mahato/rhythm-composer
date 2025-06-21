from bark import SAMPLE_RATE, generate_audio, preload_models
from scipy.io.wavfile import write as write_wav
from IPython.display import Audio
import torch
import re
import numpy as np
import os

def patch_torch_load():
    original_load = torch.load
    def patched_load(f, *args, **kwargs):
        kwargs['weights_only'] = False
        return original_load(f, *args, **kwargs)
    torch.load = patched_load

patch_torch_load()
# Load Bark models at the start
preload_models()


def clean_and_split_sentences(lyrics_text: str):
    """
    Clean up the lyrics and split into sentences.
    """
    lyrics_text = lyrics_text.strip().replace("♪", "")  # Remove musical notes
    sentences = re.split(r'\.\s+|\n+', lyrics_text)  # Split by period or newlines
    return [s.strip() for s in sentences if s.strip()]


def synthesize_audio_for_sentences(sentences: list, speaker: str = "WOMAN"):
    """
    Generate audio for each sentence and return concatenated waveform.
    """
    all_audio = []

    for i, sentence in enumerate(sentences):
        text_prompt = f"[{speaker}] ♪ {sentence} ♪"
        print(f"Generating audio for: {text_prompt}")
        audio_chunk = generate_audio(text_prompt)
        all_audio.append(audio_chunk)

        # Save each chunk separately
        chunk_filename = f"chunk_{i+1}.wav"
        write_wav(chunk_filename, SAMPLE_RATE, audio_chunk)

    # Concatenate all chunks
    full_audio = np.concatenate(all_audio)
    return full_audio


def generate_final_music(lyrics: str, output_filename="final_music.wav"):
    """
    Generate final music from full lyrics and save as one audio file.
    """
    sentences = clean_and_split_sentences(lyrics)
    final_audio = synthesize_audio_for_sentences(sentences)
    write_wav(output_filename, SAMPLE_RATE, final_audio)
    print(f"Final music saved as: {output_filename}")
    return output_filename


def generate_chunks(input_file="lyrics.txt", speaker="WOMAN"):
    """
    Generate and save individual audio chunks for each sentence in the lyrics file.
    """
    if not os.path.exists(input_file):
        raise FileNotFoundError("lyrics.txt not found")

    with open(input_file, "r", encoding="utf-8") as f:
        lyrics = f.read()

    sentences = clean_and_split_sentences(lyrics)
    chunk_files = []

    for i, sentence in enumerate(sentences):
        text_prompt = f"[{speaker}] ♪ {sentence} ♪"
        print(f"Generating chunk {i+1}: {text_prompt}")
        audio_chunk = generate_audio(text_prompt)
        chunk_filename = f"chunk_{i+1}.wav"
        write_wav(chunk_filename, SAMPLE_RATE, audio_chunk)
        chunk_files.append(chunk_filename)

    return chunk_files


# Local test
if __name__ == "__main__":
    lyrics_json = {
        "lyrics": "♪ a cup of coffee on a rainy day.\n\nThe coffee was delicious and the coffee smell was a pleasant surprise. The coffee was a nice little bit of a relief to the coffee drinkers.\n\nI had a cup of coffee in my hand and I was very happy to have a cup of coffee. The coffee smell was pleasant and the coffee was a pleasant surprise.\n\nI had a cup of coffee in my hand and I was very happy to have a cup of coffee. The coffee ♪"
    }

    generate_final_music(lyrics_json["lyrics"])
    generate_chunks("lyrics.txt")
