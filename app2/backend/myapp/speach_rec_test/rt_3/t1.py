import os
import time
import speech_recognition as sr

# obtain audio from the microphone
r = sr.Recognizer()
r.pause_threshold = 0.8

def set_ear():
    print("A moment of silence, please...")
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)
    return source

def Listen(source):
    print("listening...")
    try:
        with sr.Microphone() as source:
            audio = r.listen(source)
        # recognize speech using faster-whisper
            try:
                tick = time.time()
                text=r.recognize_faster_whisper(audio, language="en")
                #text=r.recognize_google(audio)
                tock = time.time()
                print("faster-Whisper thinks you said :: " + text, "\n in", tock - tick, "seconds")
                if text:
                    return text
                else:
                    Hear(source)
            except sr.UnknownValueError:
                print("faster-Whisper could not understand audio")
            except sr.RequestError as e:
                print(f"Could not request results from faster-Whisper; {e}")
    except Exception as e:
        print(f"Error getting audio: {e}")

if __name__ == "__main__":
    source = set_ear()
    Hear(source)

