from google import genai
from google.genai import types
import time

client = genai.Client(api_key='AIzaSyAU6gNgL4-8DIBy2pybFo-tluRHOQErmh4') # Replace with your actual API key
MODEL_ID = "gemini-2.0-flash-exp"

def is_complete_sentence(text, model_id=MODEL_ID):
    """
    Uses Gemini API to determine if a string is a complete sentence.
    """
    prompt = f"""
    You are a helpful and very accurate language analysis tool.
    Your only task is to classify if the given text is a complete sentence.
    If the text expresses a complete thought and follows basic grammatical structure, respond with only the word: True.
    If the text appears incomplete or is cut off mid-sentence, respond with only the word: False.
    Be very conservative - Err on the side of "False" if unsure.

    Input text: {text}
    """

    try:
        response = client.models.generate_content(
            model=model_id,
            contents=prompt,
        )
        #print(response.text)
        return response.text.strip().lower() == "true"  # Check for exact match
    except Exception as e:
        print(f"Error during Gemini API call: {e}")
        return False  # Handle errors gracefully
    
if __name__ == "__main__":
    while True:
        time.sleep(1)
        # Test the function
        tick = time.time()
        print(is_complete_sentence("Hello, how are you?"))
        tock = time.time()
        print(f"Time taken: {tock - tick:.2f} seconds")