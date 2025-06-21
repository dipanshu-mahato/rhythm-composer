from transformers import pipeline

def generate_lyrics(prompt):
    """
    Generate lyrics using a small text-generation model.
    
    Args:
        prompt (str): The initial text prompt to generate lyrics from
        
    Returns:
        str: Formatted generated lyrics
    """
    generator = pipeline('text-generation', model='gpt2')  # or 'distilgpt2'
    
    response = generator(prompt, max_length=100, temperature=1.0, top_p=0.95, do_sample=True)
    
    output = response[0]['generated_text']
    
    formatted_lyrics = f"♪ {output.strip()} ♪"
    
    return formatted_lyrics
