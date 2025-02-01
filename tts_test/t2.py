from TTS.api import TTS
import time
tts = TTS("tts_models/en/multi-dataset/tortoise-v2")



voice_dir=r"C:\Users\njne2\Desktop\Cuda_PWR\CREATIVE\Mini_project\tts_test\tortoise-tts\tortoise\voices"

print("tts started")
# Using presets with the same voice
while True:
    tic = time.time()
    print("started")
    tts.tts_to_file(text="Good morning my friend, how are you doing today?. hope you are doing great",
                    file_path="output.wav",
                    voice_dir=voice_dir,
                    speaker="lj",
                    preset="ultra_fast")
    toc = time.time()
    print(f"finished{toc-tic}")

