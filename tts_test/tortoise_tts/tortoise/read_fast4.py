import argparse
import os
from time import time
import threading
import torch
import torchaudio
import keyboard
import sounddevice as sd
import numpy as np
from pydub import AudioSegment
from pydub.playback import play
import io
import queue

from tortoise.api_fast import TextToSpeech, MODELS_DIR
from tortoise.utils.audio import load_audio, load_voices
from tortoise.utils.text import split_and_recombine_text

# Initialize TextToSpeech model outside the function
if torch.backends.mps.is_available():
    use_deepspeed = False
else:
    use_deepspeed = False
tts = TextToSpeech(models_dir=MODELS_DIR, use_deepspeed=use_deepspeed, kv_cache=True, half=True)


def generate_audio_chunk(text_part, voice_samples, seed, tts, chunk_queue):
    """
    Generates audio for a text part using Tortoise TTS and puts the audio chunk into a queue.
    """
    try:
        start_time = time()
        full_audio = tts.tts(text_part, voice_samples=voice_samples, use_deterministic_seed=seed)
        end_time = time()
        full_audio = full_audio.squeeze().cpu().numpy()

        sr = 24000
        chunk_size_samples = 5 * sr  # Hardcoded chunk size for demonstration, set as per your needs
        num_samples = full_audio.shape[0]
        audio_chunks = [full_audio[i:i + chunk_size_samples] for i in range(0, num_samples, chunk_size_samples)]
        for audio_chunk in audio_chunks:
             chunk_queue.put(audio_chunk)
    except Exception as e:
      print("Exception during audio generation: ", e)
    finally:
         chunk_queue.put(None)  # Signal end of generation for this section

def generate_audio(text, voice, output_path, output_name, preset='standard', model_dir=MODELS_DIR, seed=None, tts=tts):
    """
    Generates audio from the given text in chunks, streams it sequentially using pydub, and saves the full output.
    """
    outpath = output_path
    outname = output_name
    selected_voices = voice.split(',')

    # Process text
    if '|' in text:
        print("Found the '|' character in your text, which I will use as a cue for where to split it up. If this was not"
              "your intent, please remove all '|' characters from the input.")
        texts = text.split('|')
    else:
        texts = split_and_recombine_text(text)

    seed = int(time()) if seed is None else seed
    
    for selected_voice in selected_voices:
        voice_outpath = os.path.join(outpath, selected_voice)
        os.makedirs(voice_outpath, exist_ok=True)

        if '&' in selected_voice:
            voice_sel = selected_voice.split('&')
        else:
            voice_sel = [selected_voice]

        voice_samples, conditioning_latents = load_voices(voice_sel)
        
        for j, text_part in enumerate(texts):
           full_audio = []
           chunk_queue = queue.Queue()
           thread = threading.Thread(target=generate_audio_chunk, args=(text_part, voice_samples, seed, tts, chunk_queue))
           thread.start()

           while True:
               if keyboard.is_pressed('q'):
                  print("Stopping early due to 'q' keypress.")
                  break

               audio_chunk = chunk_queue.get() #Get the audio chunk from the thread

               if audio_chunk is None: #if the value is None, this means that this part of the text is complete
                   break
               try:
                    audio_segment = AudioSegment(audio_chunk.tobytes(), frame_rate=24000, sample_width=audio_chunk.dtype.itemsize, channels=1)
                    play(audio_segment)
               except Exception as e:
                    print(f"An exception occurred while playing audio: {e}")
                    break
               
               full_audio.append(torch.tensor(audio_chunk).unsqueeze(0))

           if keyboard.is_pressed('q'):
                 break
           
           if not os.path.exists(os.path.join(voice_outpath, f'{j}.wav')):
               if full_audio:  # Check if full_audio is not empty
                 full_audio_part = torch.cat(full_audio, dim=-1).cpu()
                 torchaudio.save(os.path.join(voice_outpath, f'{j}.wav'), full_audio_part, 24000)
                 print("Audio part generated to file")
               full_audio = []  # Reset for the next part

        if keyboard.is_pressed('q'):
            break
        
        if full_audio: #Check if full_audio is not empty
            full_audio = torch.cat(full_audio, dim=-1).cpu()
            torchaudio.save(os.path.join(voice_outpath, f"{outname}.wav"), full_audio, 24000)
        output_file_path = os.path.join(voice_outpath, f"{outname}.wav")
        return output_file_path


def generate_and_stream_audio_from_text(text, voice="lj", output_path='results/longform/', output_name='combined.wav', preset='standard', model_dir=MODELS_DIR, seed=None):
    """Generates and streams audio for the given text using the global tts object."""
    output_file_path = generate_audio(text, voice, output_path, output_name, preset, model_dir, seed, tts=tts)
    return output_file_path


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--textfile', type=str, help='A file containing the text to read.', default="data/seal_copypasta.txt")
    parser.add_argument('--voice', type=str, help='Selects the voice to use for generation. See options in voices/ directory (and add your own!) '
                                                 'Use the & character to join two voices together. Use a comma to perform inference on multiple voices.', default='lj')
    parser.add_argument('--output_path', type=str, help='Where to store outputs.', default='results/longform/')
    parser.add_argument('--output_name', type=str, help='How to name the output file', default='combined.wav')
    parser.add_argument('--preset', type=str, help='Which voice preset to use.', default='standard')
    parser.add_argument('--model_dir', type=str, help='Where to find pretrained model checkpoints. Tortoise automatically downloads these to .models, so this'
                                                      'should only be specified if you have custom checkpoints.', default=MODELS_DIR)
    parser.add_argument('--seed', type=int, help='Random seed which can be used to reproduce results.', default=None)
    args = parser.parse_args()

    # Process text
    with open(args.textfile, 'r', encoding='utf-8') as f:
        text = ' '.join([l for l in f.readlines()])

    output_file_path = generate_and_stream_audio_from_text(text, args.voice, args.output_path, args.output_name,
                                         args.preset, args.model_dir, args.seed)

    print(f"Audio saved to: {output_file_path}")