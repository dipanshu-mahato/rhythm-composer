from pydub import AudioSegment
import os

def append_wav_file(existing_combined_path, new_file_path, output_path=None):
    """
    Append a new WAV file to an existing WAV file.
    
    Args:
        existing_combined_path (str): Path to existing combined WAV file
        new_file_path (str): Path to new WAV file to append
        output_path (str, optional): Path where the result will be saved. 
                                    If None, overwrites the existing combined file.
    
    Returns:
        str: Path to the output file
    """
    try:
        # If no output path is provided, overwrite the existing combined file
        if output_path is None:
            output_path = existing_combined_path
        
        # Load audio files
        existing_audio = AudioSegment.from_wav(existing_combined_path)
        new_audio = AudioSegment.from_wav(new_file_path)
        
        # Combine audio files
        updated_combined = existing_audio + new_audio
        
        # Create output directory if it doesn't exist
        os.makedirs(os.path.dirname(output_path) or '.', exist_ok=True)
        
        # Export combined audio
        updated_combined.export(output_path, format="wav")
        
        print(f"Successfully appended {new_file_path} to create {output_path}")
        return output_path
    
    except Exception as e:
        print(f"Error appending audio file: {str(e)}")
        return None

if __name__ == "__main__":
    # Example usage
    existing_combined = "expanded_jungle.wav"  # Your existing combined file
    new_file = "jungle3.wav"  # New file to append
    output = "expanded_jungle.wav"  # New output file (optional)
    
    # Append the new file to the combined file
    append_wav_file(existing_combined, new_file, output)
    
    # If you want to overwrite the original combined file, use:
    # append_wav_file(existing_combined, new_file)