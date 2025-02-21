#from speach_rec_test.rt_2.t4 import start_listening
from gem_test.get_resume import get_resume
from gem_test.t2 import chat_with_model, get_chat, stream_chat
from tts_test.t4 import gtts_tts_and_play as generate_and_stream_audio_from_text
from speach_rec_test.rt_3.t1 import set_ear,Listen
import time


#init gemini code
resume_path = r"C:\Users\njne2\Desktop\resume\Neil Joseph.pdf"
job="software engineer"
resume=get_resume(resume_path)
chat=get_chat(resume,job,"Challenging_interviewer")
response=set_ear()

generate_and_stream_audio_from_text("Good morning lets get in to it without any delay.",)

for i in range(3):
    print("Start talking")
    transcript=""
    tick=time.time()
    #trans=start_listening()
    trans= Listen(response)
    for line in trans:
        transcript+=line
    tock=time.time()
    print("whisper",tock-tick)
    
    # Stream Gemini output and TTS each token as it arrives.
    tick=time.time()
    response_text = ""
    for token in stream_chat(transcript, chat):
        response_text += token
        generate_and_stream_audio_from_text(token)
    tock=time.time()
    print("gem streaming & tts", tock-tick)
    
    print(response_text)
