#from speach_rec_test.rt_2.t3 import start_listening
from gem_test.get_resume import get_resume
from gem_test.t2 import chat_with_model,get_chat


#init gemini code
resume_path = r"C:\Users\njne2\Desktop\Neil Joseph.pdf" 
job="software engineer"
resume=get_resume(resume_path)
chat=get_chat(resume,job,"Challenging_interviewer")

#start_listening()
resp=chat_with_model("hello goodmorning my name is neil joseph. so can you explain about my job and wht type of interviewr you are in the prompt i given u",chat)
print(resp)