#from speach_rec_test.rt_2.t4 import start_listening
from gem_test.get_resume import get_resume
from gem_test.t2 import get_chat,stream_complete_sentences
from tts_test.t5 import GTTSTTSPlayer
from speach_rec_test.rt_3.t1 import set_ear,Hear
from str_comp_test.t5 import set_sentance_complete,is_complete
import time


#init gemini code
resume_path = r"C:\Users\njne2\Desktop\resume\Neil Joseph.pdf"
job="software engineer"
resume=get_resume(resume_path)
chat=get_chat(resume,job,"Challenging_interviewer")
response=set_ear()
tokenizer, model, device = set_sentance_complete(results_path=r"str_comp_test\results")
player=GTTSTTSPlayer(lang="en", slow=False)
player.play_text("Good morning lets get in to it without any delay.")
labels= {0: "complete", 1: "incomplete"}

for i in range(3):
    print("Start talking")
    transcript=""
    while True:
        tick=time.time()
        trans= Hear(response)
        if trans:
            for line in trans:
                transcript+=line
        tock=time.time()
        print("whisper",tock-tick)
        if is_complete(transcript, tokenizer, model, device)==0:
            print("sentence complete")
            break
        print(f"{transcript =}")
    
    # Stream Gemini output and TTS each token as it arrives.
    tick=time.time()
    response_text = ""
    for token in stream_complete_sentences(transcript, chat):
        response_text += token
        player.play_text(token)
    tock=time.time()
    print("gem streaming & tts", tock-tick)
    
    print(response_text)
