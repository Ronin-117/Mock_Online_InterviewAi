import io
import time
import threading
import numpy as np
from gtts import gTTS
from pydub import AudioSegment
import sounddevice as sd

class GTTSTTSPlayer:
    def __init__(self, lang="en", slow=False):
        self.lang = lang
        self.slow = slow
        self.next_audio = None
        self.lock = threading.Lock()
        self.generator_thread = None

    def _generate_audio(self, text):
        try:
            tts = gTTS(text=text, lang=self.lang, slow=self.slow,tld='ca') 
            buf = io.BytesIO()
            tts.write_to_fp(buf)
            buf.seek(0)
            audio = AudioSegment.from_file(buf, format="mp3")
            samples = np.array(audio.get_array_of_samples())
            if audio.channels > 1:
                samples = samples.reshape((-1, audio.channels))
            return samples, audio.frame_rate
        except Exception as e:
            print(f"Error generating TTS: {e}")
            return None, None

    def _async_generate(self, text):
        samples, rate = self._generate_audio(text)
        with self.lock:
            self.next_audio = (samples, rate)

    def play_text(self, text):
        # Start pre-generation for the next chunk asynchronously
        self.generator_thread = threading.Thread(target=self._async_generate, args=(text,))
        self.generator_thread.start()

        # Wait for current generation to complete if not cached already
        self.generator_thread.join()
        with self.lock:
            if self.next_audio is not None:
                samples, rate = self.next_audio
                sd.play(samples, samplerate=rate)
                sd.wait()
                self.next_audio = None

if __name__=="__main__":
    player = GTTSTTSPlayer(lang="en", slow=False)
    
    # Example continuous stream of text chunks
    text_chunks = [
        "Good morning, let's get started.",
        "Today we will be discussing efficiency improvements in TTS systems.",
        "By preloading audio, we can minimize delays.",
        "Thank you for your attention."
    ]
    
    for chunk in text_chunks:
        start = time.time()
        player.play_text(chunk)
        end = time.time()
        print(f"Chunk played in {end - start:.2f} seconds.")