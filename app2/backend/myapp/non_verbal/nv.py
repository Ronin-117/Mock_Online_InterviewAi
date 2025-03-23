import cv2
import mediapipe as mp
import numpy as np
import time


def set_non_verbal():
    # Open Webcam
    time.sleep(2)
    cap = cv2.VideoCapture(0)
    return cap
    

# Define Performance Metrics (Example: Posture & Hand Movements)
def evaluate_posture(landmarks,mp_pose):
    # Get key landmarks for posture
    shoulder_left_y = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER].y
    shoulder_right_y = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER].y
    ear_left_y=landmarks[mp_pose.PoseLandmark.LEFT_EAR].y
    ear_right_y=landmarks[mp_pose.PoseLandmark.RIGHT_EAR].y
    ear_left_x=landmarks[mp_pose.PoseLandmark.LEFT_EAR].x
    ear_right_x=landmarks[mp_pose.PoseLandmark.RIGHT_EAR].x
    mouth_left_y=landmarks[mp_pose.PoseLandmark.MOUTH_LEFT].y
    mouth_right_y=landmarks[mp_pose.PoseLandmark.MOUTH_RIGHT].y
    nose_x=landmarks[mp_pose.PoseLandmark.NOSE].x

    # Check if shoulders are aligned (Good posture)
    shoulder_align_diff = abs(shoulder_left_y - shoulder_right_y)
    ear_align_diff=abs(ear_left_y-ear_right_y)
    ec_left=abs(ear_left_x-nose_x)
    ec_right=abs(ear_right_x-nose_x)
    ec_diff =abs(ec_left-ec_right)

    if ec_diff < 0.13:
        eye_contact="Good eye contact"
    else:
        eye_contact="No eye contact"

    if shoulder_align_diff < 0.09 and ear_align_diff<0.03:  # Small difference means upright
        posture = "Good Posture"
    else:
        posture = "Unclear Posture"
    
    return posture,eye_contact


if __name__ == "__main__":
    cap=set_non_verbal()
    mp_pose = mp.solutions.pose
    mp_drawing = mp.solutions.drawing_utils
    # Pose Estimation Loop
    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            # Convert to RGB for MediaPipe
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            result = pose.process(rgb_frame)

            # Draw pose landmarks
            if result.pose_landmarks:
                mp_drawing.draw_landmarks(frame, result.pose_landmarks, mp_pose.POSE_CONNECTIONS)

                # Evaluate Posture
                posture,eye_contact = evaluate_posture(result.pose_landmarks.landmark,mp_pose)

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
