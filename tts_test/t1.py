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
tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(device)

# Run TTS
# ❗ Since this model is multi-lingual voice cloning model, we must set the target speaker_wav and language
# Text to speech list of amplitude values as output
#wav = tts.tts(text="Hello world!", speaker_wav="girl-ix27ve-never-been-out-of-the-village-before-229855.wav", language="en")
# Text to speech to a file
def talk(text):
    tts.tts_to_file(text=text, speaker_wav=r"C:\Users\njne2\Desktop\Cuda_PWR\CREATIVE\Mini_project\tts_test\MorganFreeMan.wav", language="en", file_path=r"C:\Users\njne2\Desktop\Cuda_PWR\CREATIVE\Mini_project\tts_test\output.wav")
    output_path = r"C:\Users\njne2\Desktop\Cuda_PWR\CREATIVE\Mini_project\tts_test\output.wav"
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