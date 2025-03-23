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
from app2.backend.myapp.non_verbal.nv import set_non_verbal,evaluate_posture
import time
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import cv2
import mediapipe as mp # Import mediapipe here

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
    try:
        #init gemini code for interview
        job="Ai software engineer"
        q_num=2
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
        chat=get_chat(resume,job,"Challenging_interviewer",total_q_num=q_num)

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


        # Write metadata
        with open(metadata_file, 'w') as f:
                f.write(f"Interview Timestamp: {timestamp}\n")
                f.write(f"Job: {job}\n")
                f.write(f"Interviewer Type: Challenging_interviewer\n")

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
        stop_nv=True
        print("interview completed")
         # Save non-verbal data to a file
        with open(non_verbal_data_file, 'w') as f:
            for key, value in non_verbal_data.items():
                f.write(f"{key}: {value}\n")
        return Response({"message": "interview completed", "redirect_url": "/interview_results"}, status=200) #change the /results to your results page url
    except Exception as e:
        print(e)
        return Response({"error": str(e)}, status=500)

