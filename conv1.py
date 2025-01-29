from speach_rec_test.rt_2.t3 import start_listening
from gem_test.get_resume import get_resume
from gem_test.t2 import chat_with_model,get_chat


#init gemini code
resume_path = r"C:\Users\njne2\Desktop\Neil Joseph.pdf" 
job="software engineer"
resume=get_resume(resume_path)
chat=get_chat(resume,job,"Challenging_interviewer")

for i in range(3):
    transcript=""
    trans=start_listening()
    for line in trans:
        transcript+=line
    resp=chat_with_model(transcript,chat)
    print(resp)
