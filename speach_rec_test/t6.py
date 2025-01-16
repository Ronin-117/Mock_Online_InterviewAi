from google import genai
from google.genai import types
import pathlib

client = genai.Client(api_key='AIzaSyAU6gNgL4-8DIBy2pybFo-tluRHOQErmh4')

LOCAL_AUDIO_FILE = "Filler.wav"

MODEL_ID = "gemini-2.0-flash-exp"

# Create a Path object
audio_path = pathlib.Path(LOCAL_AUDIO_FILE)

# Check if the file exists
if not audio_path.is_file():
    raise FileNotFoundError(f"Audio file not found at: {LOCAL_AUDIO_FILE}")

# Read the audio file's content as bytes
audio_bytes = audio_path.read_bytes()

file_upload = client.files.upload(
    path=audio_path,

)

response = client.models.generate_content(
    model=MODEL_ID,
    contents=[
        types.Content(
            role="user",
            parts=[
                types.Part.from_uri(
                    file_uri=file_upload.uri,
                    mime_type=file_upload.mime_type),
                ]),
        "Listen carefully to the following audio file. provide a trascript of the audio file along with all fillers and pauses with time stamps.also give time stamps for pauses that are longer than usual and fillers that are repeated more than once.",
    ]
)

print(response.text)