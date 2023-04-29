import cv2
import mediapipe as mp
import numpy as np
import time
import json
from datetime import datetime

class FallDetector:
    def __init__(self):
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_pose = mp.solutions.pose
        self.time_between_frames = 0.0333 #fps = 30, 640x480
        self.velocities_list_length = 10
        self.landmarks_dict = {
            "NOSE"      :self.mp_pose.PoseLandmark.NOSE,
            "LEFT_WRIST":self.mp_pose.PoseLandmark.LEFT_WRIST
        }

        self.log_file = self.create_log_file()
        self.detect_fall()
    
    def create_log_file(self):
        now = datetime.now()
        file_name = now.strftime("%d-%m-%Y_%H-%M-%S")
        log_file = open(f"{file_name}.json", "w")
        return log_file

    def detect_fall(self):
        frame_num = 0
        cap = cv2.VideoCapture(0)
        #cap = cv2.VideoCapture(".\WIN_20230429_22_54_08_Pro.mp4")
        prev_x, prev_y = None, None
        velocities = []


        with self.mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
            while cap.isOpened():
                _, frame = cap.read()
                frame_num += 1
                image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                image.flags.writeable = False
                avg_velocity = None
                fall_detected = False

                results = pose.process(image)
                image.flags.writeable = True
                image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

                if results.pose_landmarks:
                    cur_x,cur_y,_ = self.get_landmarks(results, "LEFT_WRIST")
                    if prev_x is not None and prev_y is not None:
                        distance = self.calculate_distance(cur_x, cur_y, prev_x, prev_y)
                        velocity = distance / self.time_between_frames
                        velocities.append(velocity)
                        if len(velocities) == self.velocities_list_length:
                            avg_velocity = sum(velocities) / self.velocities_list_length
                            print(f"avg velocity: {avg_velocity}")
                            velocities = []
                        
                    if avg_velocity is not None and avg_velocity > 0.5:
                        print("FALL DETECTED")
                        fall_detected = True

                    prev_x, prev_y = cur_x, cur_y
                
                if fall_detected:
                    cv2.putText(image, "Fall Detected", (50,50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)
                
                else:
                    cv2.putText(image, "No Fall Detected", (50,50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)

                self.mp_drawing.draw_landmarks(image, results.pose_landmarks, self.mp_pose.POSE_CONNECTIONS,
                        self.mp_drawing.DrawingSpec(color=(245,117,66), thickness=2, circle_radius=2), 
                        self.mp_drawing.DrawingSpec(color=(245,66,230), thickness=2, circle_radius=2) 
                )               

                cv2.imshow('Mediapipe Feed', image)
                if cv2.waitKey(10) & 0xFF == ord('q'):
                    break

        cap.release()
        cv2.destroyAllWindows()

    def get_landmarks(self, results, landmark):
        #check visibility?
        lndmrk = results.pose_landmarks.landmark[self.landmarks_dict[landmark]]
        x = lndmrk.x
        y = lndmrk.y
        z = lndmrk.z
        return x,y,z

    def calculate_distance(self, x1,y1,x2,y2):
        return np.sqrt((x2-x1)**2 + (y2-y1)**2)

if __name__ == "__main__":
    fall_detector = FallDetector()