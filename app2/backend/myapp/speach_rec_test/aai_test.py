# `pip install assemblyai` (Windows)

import assemblyai as aai

aai.settings.api_key = "d70e3e5c8d1e4dbb8e42c2eb5385986a"
transcriber = aai.Transcriber()

transcript = transcriber.transcribe("Filler.wav")
# transcript = transcriber.transcribe("./my-local-audio-file.wav")

print(transcript.text)