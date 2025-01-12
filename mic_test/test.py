import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wavfile
import time
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


# Constants
SAMPLE_RATE = 44100  # Common sample rate for audio
DURATION = 5        # Duration of the recording in seconds
CHANNELS = 1        # Mono audio
OUTPUT_FILE = "microphone_test.wav"


def list_devices():
    """Lists the available input and output audio devices."""
    logging.info("Listing available audio devices:")
    devices = sd.query_devices()
    for i, device in enumerate(devices):
        logging.info(f"  Device ID {i}: {device['name']}, {'Input' if device['max_input_channels'] > 0 else ''} {'Output' if device['max_output_channels'] > 0 else ''}")


def record_audio(duration, sample_rate, channels):
    """Records audio from the default microphone."""
    logging.info(f"Recording {duration} seconds of audio...")
    try:
          recording = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=channels,dtype='int16')
          sd.wait() # Wait until recording is finished
          logging.info("Recording finished")
          return recording
    except Exception as e:
          logging.error(f"Error recording audio: {e}")
          return None
    


def save_audio(recording, sample_rate, output_file):
    """Saves a numpy array as a wav file"""
    try:
      logging.info(f"Saving recorded audio to '{output_file}'")
      wavfile.write(output_file, sample_rate, recording)
      logging.info(f"Audio saved to '{output_file}'")
    except Exception as e:
      logging.error(f"Error saving audio file: {e}")

def playback_audio(recording, sample_rate):
    """Plays the recording back to verify."""
    try:
        logging.info("Playing back recorded audio...")
        sd.play(recording, samplerate=sample_rate)
        sd.wait() #Wait until playback is finished
        logging.info("Playback finished.")
    except Exception as e:
        logging.error(f"Error during playback: {e}")


if __name__ == "__main__":
    list_devices()
    audio_recording = record_audio(DURATION, SAMPLE_RATE, CHANNELS)

    if audio_recording is not None:
         save_audio(audio_recording, SAMPLE_RATE, OUTPUT_FILE)
         playback_audio(audio_recording, SAMPLE_RATE)
    else:
        logging.error("Recording failed, not saving or playing back")
    logging.info("Done.")