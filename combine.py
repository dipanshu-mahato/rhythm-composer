from pydub import AudioSegment
import os

def combine_wav_files(file1_path, file2_path, output_path):
    """
    Combine two WAV files into a single file.
    
    Args:
        file1_path (str): Path to first WAV file
        file2_path (str): Path to second WAV file
        output_path (str): Path where the combined WAV will be saved
    
    Returns:
        str: Path to the output file
    """
    try:
        # Load audio files
        audio1 = AudioSegment.from_wav(file1_path)
        audio2 = AudioSegment.from_wav(file2_path)
        
        # Combine audio files
        combined = audio1 + audio2
        
        # Create output directory if it doesn't exist
        os.makedirs(os.path.dirname(output_path) or '.', exist_ok=True)
        
        # Export combined audio
        combined.export(output_path, format="wav")
        
        print(f"Successfully combined audio files into {output_path}")
        return output_path
    
    except Exception as e:
        print(f"Error combining audio files: {str(e)}")
        return None

if __name__ == "__main__":
    # Example usage
    file1 = "jungle.wav"  # Replace with your first WAV file
    file2 = "jungle2.wav"  # Replace with your second WAV file
    output = "combined_jungle.wav"
    
    combine_wav_files(file1, file2, output)