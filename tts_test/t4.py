import io
import numpy as np
from gtts import gTTS
from pydub import AudioSegment
import sounddevice as sd

def gtts_tts_and_play(text, lang="en"):
    # Generate speech audio with gTTS into an in-memory buffer
    tts = gTTS(text=text, lang=lang)
    buf = io.BytesIO()
    tts.write_to_fp(buf)
    buf.seek(0)
    
    # Load the MP3 audio from the buffer using pydub
    audio_segment = AudioSegment.from_file(buf, format="mp3")
    
    # Convert AudioSegment to numpy array
    samples = np.array(audio_segment.get_array_of_samples())
    if audio_segment.channels == 2:
        samples = samples.reshape((-1, 2))
    
    # Play the audio using sounddevice
    sd.play(samples, samplerate=audio_segment.frame_rate)
    sd.wait()

# ...existing code or additional functions...
