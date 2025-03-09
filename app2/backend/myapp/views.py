from django.shortcuts import render
from django.conf import settings  # Import settings
import os  # Import os
import re
# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.response import Response
from app2.backend.myapp.gem_test.get_resume import get_resume
from app2.backend.myapp.gem_test.t2 import get_chat,stream_complete_sentences,gem_test
from app2.backend.myapp.tts_test.t5 import GTTSTTSPlayer
from app2.backend.myapp.speach_rec_test.rt_3.t1 import set_ear,Listen
from app2.backend.myapp.str_comp_test.t5 import set_sentance_complete,is_complete
import time

@api_view(['POST']) 
def start_interview(request):
    #init gemini code for interview
    gem_test()
    resume_path = r"C:\Users\njne2\Desktop\resume\Neil Joseph.pdf"
    job="Ai software engineer"
    resume=get_resume(resume_path)
    chat=get_chat(resume,job,"Challenging_interviewer",total_q_num=5)

    #init tts code
    player=GTTSTTSPlayer(lang="en", slow=False)

    #init speech recognition code
    response=set_ear()
    print("talk something to check microphone")
    player.play_text("talk something to check microphone")
    Listen(response)
    if response:
        player.play_text("Thats great now we can start the interview")
    print("microphone checked")
    results_path = os.path.join(settings.BASE_DIR,'myapp', 'str_comp_test', 'results')
    print(f"{results_path =}")
    tokenizer, model, device = set_sentance_complete(results_path=results_path) 
    print("completeness check model loaded")
    #start the interview
    player.play_text("Good morning lets get in to it without any delay.")
    for i in range(5):
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
        transcript=f"[[[Response from use:{i}]]]"+transcript
        # Stream Gemini output and TTS each token as it arrives.
        tick=time.time()
        response_text = ""
        pattern = r'\[\[\[\d+\]\]\]'
        for token in stream_complete_sentences(transcript, chat):
            response_text += token
            if re.search(pattern, token):
                token=re.sub(pattern,"",token)
            player.play_text(token)
        tock=time.time()
        print("gem streaming & tts", tock-tick)
        print(response_text)
    return Response({"message": f"interview completed"}, status=200)
