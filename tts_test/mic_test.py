import os
from pydub import AudioSegment
from pydub.playback import play
import time

# Text to speech to a file
def talk(text):
    output_path = r"C:\Users\njne2\Desktop\Cuda_PWR\CREATIVE\Mini_project\tts_test\output.wav"    
    if os.path.exists(output_path):
        audio = AudioSegment.from_wav(output_path)
        play(audio)  # This will block until the audio finishes playing
    else:
        print(f"Error: The file {output_path} was not created.")

if __name__ == "__main__":
    while True:
        text = str(input("Enter text: "))
        if text == "exit":
            break
        talk(text)
        # Any code here will execute after the audio finishes playing
        print("Audio finished playing.")