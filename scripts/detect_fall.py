import cv2
import mediapipe as mp
import numpy as np
import time
import requests
import sys
import socket
import datetime


fall_detected = False
alerts_endpoint = "http://localhost:6500/alerts"
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

# Define font and color for text overlay
font = cv2.FONT_HERSHEY_SIMPLEX
font_scale = 1
color = (0, 0, 255) # red color

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

        y_nose = results.pose_landmarks.landmark[mp_pose.PoseLandmark.NOSE].y

        print(y_nose)

        time.sleep(0.1)

        if y_nose > 0.7:
            fall_detected = True
        else:
            fall_detected = False
        
        if fall_detected:
            message = "Fall Detected!"
        else:
            message = "No Fall"

        cv2.putText(image, message, (10, 50), font, font_scale, color, 2, cv2.LINE_AA)

        mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                mp_drawing.DrawingSpec(color=(245,117,66), thickness=2, circle_radius=2), 
                                mp_drawing.DrawingSpec(color=(245,66,230), thickness=2, circle_radius=2) 
                                 )               
        
        cv2.imshow('Mediapipe Feed', image)

        if fall_detected:
            try:
                print(f"Making a POST request to {alerts_endpoint}...")
                payload["timestamp"] = datetime.datetime.now().isoformat()
                response = requests.post(alerts_endpoint, json=payload)
            except Exception as e:
                print(f"Could not make a POST request to {alerts_endpoint}, error: {e}")

        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


