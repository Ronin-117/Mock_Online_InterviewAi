from django.shortcuts import render
from django.conf import settings  # Import settings
import os  # Import os
# Create your views here.
import re
import datetime
import wave
import contextlib
from rest_framework.decorators import api_view
from rest_framework.response import Response
from app2.backend.myapp.gem_test.get_resume import get_resume
from app2.backend.myapp.gem_test.t2 import get_chat,stream_complete_sentences
from app2.backend.myapp.tts_test.t5 import GTTSTTSPlayer
from app2.backend.myapp.speach_rec_test.rt_3.t1 import set_ear,Listen
from app2.backend.myapp.str_comp_test.t5 import set_sentance_complete,is_complete
import time

@api_view(['POST']) 
def start_interview(request):
    try:
        #init gemini code for interview
        resume_path = r"C:\Users\njne2\Desktop\resume\Neil Joseph.pdf"
        job="Ai software engineer"
        resume=get_resume(resume_path)
        chat=get_chat(resume,job,"Challenging_interviewer",total_q_num=5)

        #init tts code
        player=GTTSTTSPlayer(lang="en", slow=False)

        #init speech recognition code
        r=set_ear()
        print("talk something to check microphone")
        player.play_text("talk something to check microphone")
        trans=Listen(r)
        if trans:
            player.play_text("Thats great now we can start the interview")
        print("microphone checked")
        results_path = os.path.join(settings.BASE_DIR,'myapp', 'str_comp_test', 'results')
        print(f"{results_path =}")
        tokenizer, model, device = set_sentance_complete(results_path=results_path) 
        print("completeness check model loaded")

        # Create a folder for this interview
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        interview_folder = os.path.join(settings.BASE_DIR, 'myapp', 'interviews', f'interview_{timestamp}')
        os.makedirs(interview_folder, exist_ok=True)
        user_audio_folder = os.path.join(interview_folder, 'user_audio')
        os.makedirs(user_audio_folder, exist_ok=True)
        gemini_responses_file = os.path.join(interview_folder, 'gemini_responses.txt')
        metadata_file = os.path.join(interview_folder, 'metadata.txt')

        # Write metadata
        with open(metadata_file, 'w') as f:
                f.write(f"Interview Timestamp: {timestamp}\n")
                f.write(f"Job: {job}\n")
                f.write(f"Interviewer Type: Challenging_interviewer\n")

        #start the interview
        player.play_text("Good morning lets get in to it without any delay.")
        for i in range(5):
            print("Start talking")
            transcript=""
            listen_attempts = 0  # Counter for Listen() attempts
            while True:
                tick=time.time()
                audio,trans=Listen(r)
                if trans:
                    transcript+=trans
                    # Save user audio
                    user_audio_filename = os.path.join(user_audio_folder, f'user_response_{i}.wav')
                    with wave.open(user_audio_filename, 'wb') as wf:
                        wf.setnchannels(1)  # Mono
                        wf.setsampwidth(2)  # 16-bit
                        wf.setframerate(44100)  # Standard audio rate
                        wf.writeframes(audio.get_wav_data())
                else:
                    print("no speech detected")
                    listen_attempts += 1
                    if listen_attempts >= 3:  # Limit attempts to 3
                        print("Too many failed attempts to detect speech. Skipping to next question.")
                        break
                    continue
                tock=time.time()
                print("whisper",tock-tick)
                if is_complete(transcript, tokenizer, model, device)==0:
                    print("sentence complete")
                    break
                else:
                    print("sentence not complete")
                print(f"{transcript =}")
            transcript=f"[[[Response from user:{i}]]]"+transcript
            # Stream Gemini output and TTS each token as it arrives.
            tick=time.time()
            response_text = ""
            while True:
                for token in stream_complete_sentences(transcript, chat):
                    response_text += token
                    player.play_text(token)
                    with open(gemini_responses_file, 'a') as f:
                        f.write(f"Question {i+1}: {token}\n")
                if len(response_text) > 10:
                    break
            tock=time.time()
            print("gem streaming & tts", tock-tick)
            print(response_text)
        return Response({"message": f"interview completed"}, status=200)
    except Exception as e:
        print(e)
        return Response({"error": str(e)}, status=500)

