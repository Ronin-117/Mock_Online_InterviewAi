from django.shortcuts import render
from django.conf import settings  # Import settings
import os  # Import os
import re
import random
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
from app2.backend.myapp.non_verbal.nv import set_non_verbal,evaluate_posture
from app2.backend.myapp.filler_count.filler_count import count_filler_words
from app2.backend.myapp.evaluation_score import evaluation_score
import time
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import cv2
import mediapipe as mp # Import mediapipe here
import json
import pathlib
import requests
from google import genai
from markdown import Markdown
import tempfile
import uuid
from google.genai import types

client = genai.Client(api_key='AIzaSyAU6gNgL4-8DIBy2pybFo-tluRHOQErmh4')
MODEL_ID = "gemini-2.0-flash-exp" 


stop_nv=False
non_verbal_data = {
    "good_posture": 0,
    "unclear_posture": 0,
    "good_eye_contact": 0,
    "no_eye_contact": 0,
}

@api_view(['POST'])
def start_non_verbal_interview(request):
    global stop_nv, non_verbal_data
    non_verbal_data = {
        "good_posture": 0,
        "unclear_posture": 0,
        "good_eye_contact": 0,
        "no_eye_contact": 0,
    }
    try:
        cap=set_non_verbal()
        mp_pose = mp.solutions.pose
        mp_drawing = mp.solutions.drawing_utils
        # Pose Estimation Loop
        start_time = time.time()
        with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
            while cap.isOpened():
                ret, frame = cap.read()
                if not ret or stop_nv:
                    stop_nv=False
                    cap.release()
                    cv2.destroyAllWindows()
                    break

                # Convert to RGB for MediaPipe
                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                result = pose.process(rgb_frame)

                # Draw pose landmarks
                if result.pose_landmarks:
                    mp_drawing.draw_landmarks(frame, result.pose_landmarks, mp_pose.POSE_CONNECTIONS)

                    # Evaluate Posture
                    posture,eye_contact = evaluate_posture(result.pose_landmarks.landmark,mp_pose)

                    # Update frequency counts every 2 seconds
                    elapsed_time = time.time() - start_time
                    if elapsed_time >= 2:
                        start_time = time.time()  # Reset the timer
                        if posture == "Good Posture":
                            non_verbal_data["good_posture"] += 1
                        elif posture == "Unclear Posture":
                            non_verbal_data["unclear_posture"] += 1

                        if eye_contact == "Good eye contact":
                            non_verbal_data["good_eye_contact"] += 1
                        elif eye_contact == "No eye contact":
                            non_verbal_data["no_eye_contact"] += 1


                    # Display Feedback on Screen
                    cv2.putText(frame, posture, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                    cv2.putText(frame, eye_contact, (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

                # Show Webcam Output
                cv2.imshow('Body Language Analysis', frame)

                # Exit on 'q' Key
                if cv2.waitKey(10) & 0xFF == ord('q'):
                    break

        # Release Resources
        cap.release()
        cv2.destroyAllWindows()
        return Response({"message": "non verbal interview completed"}, status=200)
    except Exception as e:
        print(e)
        return Response({"error in non verbal interview": str(e)}, status=500)
        

@api_view(['POST']) 
def start_interview(request):
    global stop_nv,non_verbal_data
    stop_nv=False
    interviewer_types=["Challenging_interviewer","Data_Collector_interviewer","Conversational_interviewer","Investigative_interviewer","Enthusiastic_interviewer","Silent_interviewer","Stress_interviewer","Inexperienced_interviewer","Hiring_Manager_interviewer","HR_Representative_interviewer","Team_Member_interviewer"]
    random.seed()
    interviewer_type=random.choice(interviewer_types)
    print(f"{interviewer_type =}")
    try:
        #init gemini code for interview
        job="Ai software engineer"
        q_num= 3
        resume_file = request.FILES.get('resume_file', None)
        resume_text = request.data.get('resume_text', None)
        if resume_file:
            # Handle file upload
            file_name = default_storage.save(resume_file.name, ContentFile(resume_file.read()))
            resume_path = os.path.join(settings.MEDIA_ROOT, file_name)
            resume = get_resume(resume_path)
            print(f"from uploaded resume:{resume}")
        elif resume_text:
            # Use the provided resume text
            resume = resume_text
            print(f"from imported resume:{resume}")
        else:
            # Fallback to the default resume path if no resume text is provided
            resume_path = r"C:\Users\njne2\Desktop\resume\Neil Joseph.pdf"
            resume=get_resume(resume_path)
            print(f"from default resume:{resume}")
        chat=get_chat(resume,job,interviewer_type,total_q_num=q_num)

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
        non_verbal_data_file = os.path.join(interview_folder, 'non_verbal_data.txt')
        user_response_file = os.path.join(interview_folder, 'user_response.txt')


        # Write metadata
        with open(metadata_file, 'w') as f:
                f.write(f"Interview Timestamp: {timestamp}\n")
                f.write(f"Job: {job}\n")
                f.write(f"Interviewer Type: {interviewer_type}\n")

        #start the interview
        player.play_text("Good morning lets get in to it without any delay.")
        for i in range(q_num):
            print("Start talking")
            transcript=""
            listen_attempts = 0  # Counter for Listen() attempts
            while True:
                tick=time.time()
                try:
                    audio,trans=Listen(r)
                except Exception as e:
                    print(e)
                    continue
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
            # Save user response to a file
            if i > 0:
                with open(user_response_file, 'a') as f:
                    f.write(f"Answer {i+1}: {transcript}\n")
            transcript=f"[[[Response from user:{i}]]]"+transcript
            # Stream Gemini output and TTS each token as it arrives.
            tick=time.time()
            response_text = ""
            while True:
                for token in stream_complete_sentences(transcript, chat):
                    response_text += token
                    player.play_text(token)
                if len(response_text) > 10:
                    break
            # Save Gemini response to a file
            #if i > 0:
            with open(gemini_responses_file, 'a') as f:
                    f.write(f"Gemini Response {i}: {response_text}\n")
            tock=time.time()
            print("gem streaming & tts", tock-tick)
            print(response_text)
        stop_nv=True
        print("interview completed")
         # Save non-verbal data to a file
        with open(non_verbal_data_file, 'w') as f:
            for key, value in non_verbal_data.items():
                f.write(f"{key}: {value}\n")
        ##########################################################################
        #import all the data from the interview data folder like all the audios,gemini_response.txt,metadata.txt,non_verbal_data.txt
        
        # Load Gemini responses
        gemini_responses = []
        try:
            with open(gemini_responses_file, 'r') as f:
                for line in f:
                    key, value = line.strip().split(": ", 1)
                    gemini_responses.append(value)
        except FileNotFoundError:
            print(f"Gemini responses file not found: {gemini_responses_file}")

        # Load user responses
        user_responses = []
        try:
            with open(user_response_file, 'r') as f:
                for line in f:
                    key, value = line.strip().split(": ", 1)
                    user_responses.append(value)
        except FileNotFoundError:
            print(f"User responses file not found: {user_response_file}")
            

        # Load metadata
        metadata = {}
        try:
            with open(metadata_file, 'r') as f:
                for line in f:
                    key, value = line.strip().split(": ", 1)
                    metadata[key] = value
        except FileNotFoundError:
            print(f"Metadata file not found: {metadata_file}")

        # Load non-verbal data
        non_verbal_results = {}
        try:
            with open(non_verbal_data_file, 'r') as f:
                for line in f:
                    key, value = line.strip().split(": ", 1)
                    non_verbal_results[key] = int(value)
        except FileNotFoundError:
            print(f"Non-verbal data file not found: {non_verbal_data_file}")
        
        # Load user audio files
        user_audio_files = []
        for filename in os.listdir(user_audio_folder):
            if filename.endswith(".wav"):
                user_audio_files.append(os.path.join(user_audio_folder, filename))

        #call a function on the list of audio to return the filler words present in all of them combined
        filler_words_count=count_filler_words(user_audio_files)
        print(f"{filler_words_count =}")
        # Prepare the data to be sent to the frontend
        interview_data = {
            "gemini_responses": gemini_responses,
            "metadata": metadata,
            "non_verbal_results": non_verbal_results,
            "user_audio_files": user_audio_files,
            "interview_folder":interview_folder,
            "user_responses": user_responses,
            "filler_words_count": filler_words_count,
        }
        print(f"{interview_data =}")
        try:
            score = evaluation_score(interview_data)
            print(f"{score =}")
        except Exception as e:
            print(f"Error in evaluation_score: {e}")
            return Response({"error": "Error in evaluation_score"}, status=500)
        ##########################################

        return Response({"message": "interview completed", "redirect_url": "/interview_results", "score": score}, status=200) #change the /results to your results page url
    except Exception as e:
        print(e)
        return Response({"error": str(e)}, status=500)
