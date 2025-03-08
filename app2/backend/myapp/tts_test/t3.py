from tortoise_tts.tortoise.read_fast4 import generate_and_stream_audio_from_text
import time

while True:
    text = input("Enter text: ")
    tick=time.time()
    op_path=generate_and_stream_audio_from_text(text, "snakes", 'results/', "op",
                                         "standard")
    tock=time.time()
    print(tock-tick)