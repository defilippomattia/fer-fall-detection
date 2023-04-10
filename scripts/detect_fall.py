import cv2
import mediapipe as mp
import numpy as np
import time
import requests
import sys
import socket
import datetime

hand_raised_endpoint = "http://localhost:8081/alerts"

def get_lat_lon():
    return "45.50", "-73.56"

lat, lon = get_lat_lon()
payload = {
    "source_type": "notebook",
    "source_id": socket.getfqdn(),
    "longitude": lon,
    "latitude": lat,
    "timestamp": ""
}


cap = cv2.VideoCapture(0)
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose
with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
    while cap.isOpened():
        ret, frame = cap.read()
        
        # Recolor image to RGB
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False
      
        # Make detection
        results = pose.process(image)
    
        # Recolor back to BGR
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        
        # Extract landmarks
        try:
            try:
                right_hand_y = results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_ELBOW].y
            except Exception as e:
                print(e)
                right_hand_y = 0
            try:
                right_shoulder_y = results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_SHOULDER].y
            except Exception as e:
                print(e)
                right_shoulder_y = 0
            if (right_hand_y < right_shoulder_y):
                print("HAND RAISED")
                try:
                    print(f"Making a POST request to {hand_raised_endpoint}...")
                    payload["timestamp"] = datetime.datetime.now().isoformat()
                    response = requests.post(hand_raised_endpoint, json=payload)
                except Exception as e:
                    print(f"Could not make a POST request to {hand_raised_endpoint}, error: {e}")
                time.sleep(5)
            landmarks = results.pose_landmarks.landmark
        except:
            pass
        
        # Render detections
        mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                mp_drawing.DrawingSpec(color=(245,117,66), thickness=2, circle_radius=2), 
                                mp_drawing.DrawingSpec(color=(245,66,230), thickness=2, circle_radius=2) 
                                 )               
        
        cv2.imshow('Mediapipe Feed', image)

        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


