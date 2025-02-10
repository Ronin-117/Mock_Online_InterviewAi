#from speach_rec_test.rt_2.t4 import start_listening
from gem_test.get_resume import get_resume
from gem_test.t2 import get_chat,stream_complete_sentences
from tts_test.t5 import GTTSTTSPlayer
from speach_rec_test.rt_3.t1 import set_ear,Hear
import time


#init gemini code
resume_path = r"C:\Users\njne2\Desktop\resume\Neil Joseph.pdf"
job="software engineer"
resume=get_resume(resume_path)
chat=get_chat(resume,job,"Challenging_interviewer")
response=set_ear()
player=GTTSTTSPlayer(lang="en", slow=False)
player.play_text("Good morning lets get in to it without any delay.")

for i in range(3):
    print("Start talking")
    transcript=""
    tick=time.time()
    #trans=start_listening()
    trans= Hear(response)
    for line in trans:
        transcript+=line
    tock=time.time()
    print("whisper",tock-tick)
    
    # Stream Gemini output and TTS each token as it arrives.
    tick=time.time()
    response_text = ""
    for token in stream_complete_sentences(transcript, chat):
        response_text += token
        player.play_text(token)
    tock=time.time()
    print("gem streaming & tts", tock-tick)
    
    print(response_text)
