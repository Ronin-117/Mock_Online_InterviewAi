
import os

import speech_recognition as sr

# obtain audio from the microphone
r = sr.Recognizer()
with sr.Microphone() as source:
    r.adjust_for_ambient_noise(source)
    print("Say something!")
    audio = r.listen(source)

# recognize speech using faster-whisper
try:
    print("faster-Whisper thinks you said " + r.recognize_faster_whisper(audio, language="en"))
except sr.UnknownValueError:
    print("faster-Whisper could not understand audio")
except sr.RequestError as e:
    print(f"Could not request results from faster-Whisper; {e}")

