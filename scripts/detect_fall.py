import cv2
import mediapipe as mp
import numpy as np
import time

# Define font and color for text overlay
font = cv2.FONT_HERSHEY_SIMPLEX
font_scale = 1
color = (0, 0, 255) # red color

# Initialize variables for fall detection
prev_x_nose = 0
prev_y_nose = 0
prev_time = 0
velocity_threshold = 12.5 # pixels/second
frame_count = 0
fall_detected = False

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

        # Get x and y coordinates of nose landmark
        y_nose = results.pose_landmarks.landmark[mp_pose.PoseLandmark.NOSE].y
        x_nose = results.pose_landmarks.landmark[mp_pose.PoseLandmark.NOSE].x

        # Calculate velocity of tracking point
        if prev_time != 0:
            time_diff = time.time() - prev_time
            distance = np.sqrt((x_nose - prev_x_nose)**2 + (y_nose - prev_y_nose)**2)
            velocity = distance / time_diff
            print(velocity)
            
            # Check if fall is detected
            if velocity > velocity_threshold:
                if not fall_detected:
                    frame_count = 1
                    fall_detected = True
                else:
                    frame_count += 1
                    if frame_count >= 10: # sustained fall for 10 frames
                        cv2.putText(image, "FALL DETECTED", (10, 50), font, font_scale, color, 2)
            else:
                frame_count = 0
                fall_detected = False

        # Draw landmarks on image
        mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                mp_drawing.DrawingSpec(color=(245,117,66), thickness=2, circle_radius=2), 
                                mp_drawing.DrawingSpec(color=(245,66,230), thickness=2, circle_radius=2) 
                                 )               
        
        cv2.imshow('Mediapipe Feed', image)

        # Update previous coordinates and time
        prev_x_nose = x_nose
        prev_y_nose = y_nose
        prev_time = time.time()

        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
