from tortoise_tts.tortoise.read_fast4 import generate_and_stream_audio_from_text

while True:
    text = input("Enter text: ")
    op_path=generate_and_stream_audio_from_text(text, "lj", 'results/', "op",
                                         "standard")