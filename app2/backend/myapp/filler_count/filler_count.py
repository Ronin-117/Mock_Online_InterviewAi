import os
import tempfile
from google import genai
from google.genai import types
from config import GEMINI_API_KEY


client = genai.Client(api_key=GEMINI_API_KEY)
MODEL_ID = "gemini-2.0-flash-exp" 


def count_filler_words(audio_files):
    filler_words_count = 0
    filler_words_list = ["um", "uh", "you know", "er","euh"]  # Add more if needed
    for audio_file in audio_files:
        try:
            # Upload the temporary file to Gemini
            file_upload = client.files.upload(path=audio_file)

            # Send the request to Gemini
            response = client.models.generate_content(
                model=MODEL_ID,
                contents=[
                    types.Content(
                        role="user",
                        parts=[
                            types.Part.from_uri(
                                file_uri=file_upload.uri,
                                mime_type=file_upload.mime_type),
                            ]),
                    "Listen carefully to the following audio file. provide a trascript of the audio file along with all fillers and pauses with time stamps.also give time stamps for pauses that are longer than usual and fillers that are repeated more than once.only give the nessasary infromation. dont add stuffs like 'Okay, I'm ready. Please provide the audio file. I will transcribe it with timestamps, fillers, pauses, and highlight the longer pauses and repeated fillers as requested' or 'Okay, here's the transcription with timestamps, fillers, and notes on longer pauses/repeated fillers:'",
                ]
            )
            for filler in filler_words_list:
                filler_words_count += response.text.count(filler)
            
            # Extract the filler word count from the response
            try:
                print(f"{response.text =}")
            except ValueError:
                print(f"Could not parse filler word count from response: {response.text}")
            
        except Exception as e:
            print(f"Error processing audio file {audio_file}: {e}")

    return filler_words_count
