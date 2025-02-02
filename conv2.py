from speach_rec_test.rt_2.t4 import start_listening
from gem_test.get_resume import get_resume
from gem_test.t2 import chat_with_model,get_chat
from tts_test.tortoise_tts.tortoise.read_fast4 import generate_and_stream_audio_from_text


#init gemini code
resume_path = r"C:\Users\njne2\Desktop\Neil Joseph.pdf" 
job="software engineer"
resume=get_resume(resume_path)
chat=get_chat(resume,job,"Challenging_interviewer")

print("Start talking")
for i in range(3):
    transcript=""
    trans=start_listening()
    for line in trans:
        transcript+=line
    resp=chat_with_model(transcript,chat)
    op_dir=generate_and_stream_audio_from_text(resp)
    print(resp)