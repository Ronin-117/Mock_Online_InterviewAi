import torch
from TTS.api import TTS
from pydub import AudioSegment
from pydub.playback import play
import time
import os


# Get device
device = "cuda" if torch.cuda.is_available() else "cpu"

# List available 🐸TTS models
print(TTS().list_models())

# Init TTS
tts = TTS(model_name="tts_models/de/thorsten/tacotron2-DDC", progress_bar=False).to(device)

def talk(text):
    output_path = r"C:\Users\njne2\Desktop\Cuda_PWR\CREATIVE\Mini_project\tts_test\output.wav"
    tts.tts_to_file(text="Ich bin eine Testnachricht.", file_path=output_path)
    if os.path.exists(output_path):
        audio = AudioSegment.from_wav(output_path)
        play(audio)
        print("Audio finished playing.")
    else:
        print(f"Error: The file {output_path} was not created.")


if __name__ == "__main__":
    while True:
        text=str(input("Enter text: "))
        if text == "exit":
            break
        talk(text)