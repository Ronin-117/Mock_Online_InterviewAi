import io
import numpy as np
from gtts import gTTS
from pydub import AudioSegment
import sounddevice as sd

def gtts_tts_and_play(text, lang="es", slow=False):
    """
    Generate and play TTS audio using gTTS with a minimal memory footprint.
    
    Parameters:
        text (str): The text to convert to speech.
        lang (str): The language code (default 'en').
        slow (bool): Whether to speak slowly.
    """
    try:
        # Generate speech audio directly in memory
        tts = gTTS(text=text, lang=lang, slow=slow,tld="us")
        buf = io.BytesIO()
        tts.write_to_fp(buf)
        buf.seek(0)
        
        # Load MP3 audio from the in-memory buffer via pydub
        audio = AudioSegment.from_file(buf, format="mp3")
        
        # Get the raw samples as a numpy array
        samples = np.array(audio.get_array_of_samples())
        if audio.channels > 1:
            samples = samples.reshape((-1, audio.channels))
        
        # Play the audio using sounddevice (blocking until playback finishes)
        sd.play(samples, samplerate=audio.frame_rate)
        sd.wait()
    
    except Exception as e:
        print(f"An error occurred: {e}")


# ...existing code or additional functions...
if __name__=="__main__":
    gtts_tts_and_play("hello how you doing")