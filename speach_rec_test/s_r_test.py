import speech_recognition as sr
import os
from pydub import AudioSegment

# Set the GOOGLE_APPLICATION_CREDENTIALS environment variable if necessary
# os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "path/to/your/google_credentials.json"

r = sr.Recognizer()

# Load the audio file with pydub
audio = AudioSegment.from_file("Filler.wav")

# Convert to PCM (necessary for speech_recognition)
audio = audio.set_frame_rate(16000).set_channels(1)  # set sample rate and mono audio

# Convert the loaded audio file into a bytes format
audio_bytes = audio.raw_data

try:
    # using google speech recognition
    result = r.recognize_google(sr.AudioData(audio_bytes, sample_rate=16000, sample_width=2), language='en-US')
    print(result)
except sr.UnknownValueError:
    print("Google Speech Recognition could not understand audio")
except sr.RequestError as e:
    print(f"Could not request results from Google Speech Recognition service; {e}")