# better final transcript printing
import sounddevice as sd
import numpy as np
from faster_whisper import WhisperModel
import time
import queue
import logging
import torch
import os
import uuid
import tempfile
import scipy.io.wavfile as wavfile
import sys

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Constants
SAMPLE_RATE = 16000
CHUNK_DURATION_SECONDS = 1
BATCH_SIZE = 16
NUM_CHANNELS = 1
MODEL_SIZE = "turbo"
DEVICE = "cuda"
COMPUTE_TYPE = "float16"
running = True  # Global flag for if the program is still running
VAD_PARAMETERS = dict(min_silence_duration_ms=500)  # Customize VAD parameters
MAX_ACCUMULATION_SECONDS = 10 # Maximum buffer window 
SILENCE_TIMEOUT_SECONDS = 2

# Global list to store transcribed text segments
transcribed_text = ""
last_transcription_time = None

def audio_callback(indata, frames, time, status):
    """Callback function to receive audio chunks."""
    if status:
        logging.error(f"Error from audio device: {status}")
        return
    q.put(indata.copy())

def process_audio_stream(model, q):
    """Processes audio chunks from the queue and transcribes with a rolling window."""
    audio_buffer_list = [] #List of audio buffers, each one representing one sec
    accumulation_counter = 0 #Counter to know how many secs of audio data we have
    global transcribed_text, last_transcription_time, running
    
    while running:
        try:
            # Pulling the most recent audio samples if there are any, will avoid stale data
            while not q.empty():
                audio_data = q.get_nowait()
                audio_buffer_list.append(audio_data) # add latest audio data to our list
                accumulation_counter +=1

        except queue.Empty:
            # No audio data, but still process audio if needed
            pass

        if len(audio_buffer_list) > 0: #If we have audio data to transcribe
            start_time = time.time() #Get start time
            temp_audio_batch = [] #Batch list for audio data
            temp_audio_batch_counter = 0
            
            #Loop through all the audio data recorded so far and create batches
            for audio_data in audio_buffer_list:
                temp_audio_batch.append(audio_data)
                temp_audio_batch_counter +=1
                #Concatenate the batches
                audio_batch = np.concatenate(temp_audio_batch, axis=0)

            # Save audio chunk to a temporary file
            temp_filename = os.path.join(tempfile.gettempdir(), f"temp_audio_{uuid.uuid4()}.wav")
            wavfile.write(temp_filename, SAMPLE_RATE, audio_batch)

            # Perform transcription 
            try:
                segments, info = model.transcribe(temp_filename, language="en", vad_filter=True, vad_parameters=VAD_PARAMETERS)
                logging.debug(f"Detected language: {info.language} with a probability of: {info.language_probability}")
                
                has_transcribed = False
                for segment in segments:
                    segment_text = segment.text.strip()
                    if segment_text:
                        new_text = segment_text
                        if transcribed_text.strip():
                          for i in range(min(len(transcribed_text), len(segment_text)), 0, -1):
                                if transcribed_text.strip().endswith(segment_text[:i]):
                                    new_text = segment_text[i:]
                                    break
                        
                        if new_text:
                            transcribed_text += new_text
                            print(f"[{segment.start:.2f}s -> {segment.end:.2f}s]: {segment_text}")
                            has_transcribed = True


                if has_transcribed:
                    last_transcription_time = time.time()  # Update only on new transcription.

                end_time = time.time()
                logging.debug(f"Transcription took {end_time-start_time} seconds")
            except Exception as e:
                logging.error(f"Transcription error: {e}")
            finally:
                #Clean up the temporary file
                os.remove(temp_filename)

            #Keep the list as max length of 'MAX_ACCUMULATION_SECONDS' seconds
            if accumulation_counter >= MAX_ACCUMULATION_SECONDS:
                audio_buffer_list.pop(0)
                accumulation_counter -=1 #reduce the counter
        
        # Check for silence timeout
        if last_transcription_time is not None and (time.time() - last_transcription_time > SILENCE_TIMEOUT_SECONDS):
            logging.info("No transcription detected for 2 seconds, terminating.")
            running = False
            
        time.sleep(0.01)
        
def stream_microphone(model):
    """Streams audio from the microphone and transcribes."""
    logging.info("Starting audio stream and transcription...")
    try:
        with sd.InputStream(samplerate=SAMPLE_RATE, channels=NUM_CHANNELS, callback=audio_callback, blocksize=int(SAMPLE_RATE * CHUNK_DURATION_SECONDS)):
            process_audio_stream(model, q)
    except Exception as e:
        logging.error(f"Error Streaming from Microphone: {e}")
    finally:
        logging.info("Stopping microphone stream.")

def cleanup_resources():
    """Set program to stop gracefully"""
    global running
    running = False

def print_final_transcript():
    """Prints the final transcription without duplicates."""
    global transcribed_text
    if transcribed_text:
      print("\n--- FINAL TRANSCRIPTION ---")
      print(transcribed_text)
      transcribed_text = ""  # Reset for next session
    else:
      print("\nNo transcription available")

if __name__ == "__main__":
    q = queue.Queue()
    # Load the model
    logging.info(f"Loading Model {MODEL_SIZE}")
    model = WhisperModel(MODEL_SIZE, device=DEVICE, compute_type=COMPUTE_TYPE)
    logging.info(f"Model {MODEL_SIZE} Loaded")
    logging.info(f"Model Pipeline set up.")
    try:
        stream_microphone(model)
    except KeyboardInterrupt:
        logging.info("Keyboard interrupt, exiting")
    finally:
        cleanup_resources()
        print_final_transcript() # Print transcript before exiting
    logging.info("Exiting.")