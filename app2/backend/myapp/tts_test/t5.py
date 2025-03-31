import io
import time
import threading
import numpy as np
from gtts import gTTS
from pydub import AudioSegment
import sounddevice as sd
import os
import subprocess

class GTTSTTSPlayer:
    def __init__(self, lang="en", slow=False, rhubarb_dir="myapp\\Rhubarb-Lip-Sync-1.13.0-Windows", output_filename="output.wav"):
        self.lang = lang
        self.slow = slow
        self.next_audio = None
        self.lock = threading.Lock()
        self.generator_thread = None

        self.frontend_base_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))), "frontend", "public", "audios")
        os.makedirs(self.frontend_base_dir, exist_ok=True)
        self.output_dir = rhubarb_dir

        self.output_filename = output_filename
        self.output_path = os.path.join(self.output_dir, self.output_filename)
        # Create the output directory if it doesn't exist
        os.makedirs(self.output_dir, exist_ok=True)

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
            return samples, audio.frame_rate, audio
        except Exception as e:
            print(f"Error generating TTS: {e}")
            return None, None, None

    def _async_generate(self, text):
        samples, rate, audio = self._generate_audio(text)
        with self.lock:
            self.next_audio = (samples, rate, audio)

    def play_text(self, text):
        # Start pre-generation for the next chunk asynchronously
        self.generator_thread = threading.Thread(target=self._async_generate, args=(text,))
        self.generator_thread.start()

        # Wait for current generation to complete if not cached already
        self.generator_thread.join()
        with self.lock:
            if self.next_audio is not None:
                samples, rate, audio = self.next_audio

                # Save the audio as WAV (overwriting the same file)
                frontend_wav_path = os.path.join(self.frontend_base_dir, self.output_filename)
                audio.export(frontend_wav_path, format="wav")
                print(f"Audio saved to: {frontend_wav_path}")

                #calc encoding for lip sync
                self.run_rhubarb(wav_file=frontend_wav_path)


                # #play audio
                # sd.play(samples, samplerate=rate)
                # sd.wait()
                # self.next_audio = None

    def run_rhubarb(self, wav_file="output.wav", output_json= "output.json", rhubarb_dir="myapp\\Rhubarb-Lip-Sync-1.13.0-Windows"):

        rhubarb_exe = os.path.join(rhubarb_dir, "rhubarb.exe")

        if not os.path.exists(rhubarb_exe):
            raise FileNotFoundError(f"rhubarb.exe not found at: {rhubarb_exe}")

        frontend_json_path = os.path.join(self.frontend_base_dir, output_json)


        if not os.path.exists(wav_file):
            raise FileNotFoundError(f"Input WAV file not found at: {wav_file}")


        command = [
            rhubarb_exe,
            "-o",
            frontend_json_path,  
            "-f",
            "json",
            wav_file,  
        ]

        try:
            print(f"Running command: {' '.join(command)}")
            subprocess.run(command, check=True, cwd=rhubarb_dir)
            print(f"Rhubarb processing complete. Output saved to: ")
        except subprocess.CalledProcessError as e:
            print(f"Error running rhubarb: {e}")
            print(f"Rhubarb output (if any):\n{e.output.decode()}")
            raise
        except FileNotFoundError as e:
            print(f"Error: {e}")
            raise

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