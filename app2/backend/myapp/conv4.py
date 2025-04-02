#from speach_rec_test.rt_2.t4 import start_listening
from gem_test.get_resume import get_resume
from gem_test.t2 import get_chat,stream_complete_sentences
from tts_test.t5 import GTTSTTSPlayer
from speach_rec_test.rt_3.t1 import set_ear,Listen
from str_comp_test.t5 import set_sentance_complete,is_complete
import time

#init gemini code for interview
resume_path = r"YOUR_PATH"
job="Ai software engineer"
resume=get_resume(resume_path)
chat=get_chat(resume,job,"Challenging_interviewer")

#init tts code
player=GTTSTTSPlayer(lang="en", slow=False)

#init speech recognition code
response=set_ear()
print("talk something to check microphone")
player.play_text("talk something to check microphone")
Listen(response)
if response:
    player.play_text("Thats great now we can start the interview")
tokenizer, model, device = set_sentance_complete("./str_comp_test/results")

#start the interview
player.play_text("Good morning lets get in to it without any delay.")

for i in range(3):
    print("Start talking")
    transcript=""
    while True:
        tick=time.time()
        trans= Listen(response)
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
