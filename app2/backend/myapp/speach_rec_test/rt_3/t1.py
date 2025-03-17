import os
import time
import speech_recognition as sr

# obtain audio from the microphone
r = sr.Recognizer()
r.pause_threshold = 0.8 #0.8
r.non_speaking_duration = 0.5

def set_ear():
    print("A moment of silence, please...")
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)
    return r

def Listen(r):
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
                return audio,text
            except sr.UnknownValueError:
                print("faster-Whisper could not understand audio")
                return None,None
            except sr.RequestError as e:
                print(f"Could not request results from faster-Whisper; {e}")
                return None,None
    except sr.WaitTimeoutError as e:
        print(f"Microphone timed out waiting for audio: {e}")
        return None,None
    except OSError as e:
        print(f"Microphone access error: {e}")
        return None,None
    except Exception as e:
        print(f"An unexpected error occurred in Listen: {e}")
        return None,None


if __name__ == "__main__":
    source = set_ear()
    Listen(source)

