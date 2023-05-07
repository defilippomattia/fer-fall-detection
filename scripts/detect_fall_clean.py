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
        self.velocities_list_length = 12
        self.avg_velocity_threshold = 0.4
        self.rolling_standings_threshold = 0.8
        self.all_velocities = []
        self.all_standings = []
        self.landmarks_dict = {
            "NOSE"      :self.mp_pose.PoseLandmark.NOSE,
            "LEFT_WRIST":self.mp_pose.PoseLandmark.LEFT_WRIST,
            #"LEFT_HEEL" :self.mp_pose.PoseLandmark.LEFT_HEEL,
            "LEFT_HEEL" :self.mp_pose.PoseLandmark.LEFT_HIP,
            #"RIGHT_HEEL":self.mp_pose.PoseLandmark.RIGHT_HEEL,
            "RIGHT_HEEL":self.mp_pose.PoseLandmark.RIGHT_HIP,
            "LEFT_SHOULDER":self.mp_pose.PoseLandmark.LEFT_SHOULDER,
            "RIGHT_SHOULDER":self.mp_pose.PoseLandmark.RIGHT_SHOULDER,
        }

        #self.log_file = self.create_log_file()
        self.detect_fall()
    
    def create_log_file(self):
        now = datetime.now()
        file_name = now.strftime("%d-%m-%Y_%H-%M-%S")
        log_file = open(f"{file_name}.json", "w")
        return log_file

    def detect_fall(self):
        frame_num = 0
        cap = cv2.VideoCapture(0)
        #cap = cv2.VideoCapture(".\WIN_20230501_20_42_48_Pro.mp4")
        cap = cv2.VideoCapture(".\\videoplayback.mp4")
        #cap = cv2.VideoCapture(".\\duel.mp4")
        #cap = cv2.VideoCapture(".\\07_stubbed_toe.mp4")
        #cap = cv2.VideoCapture(".\\08_trust_fall_fail.mp4")
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
                    cur_x,cur_y,_ = self.get_landmarks(results, "NOSE")
                    LEFT_HEEL_X, LEFT_HEEL_Y, _ = self.get_landmarks(results, "LEFT_HEEL")
                    RIGHT_HEEL_X, RIGHT_HEEL_Y, _ = self.get_landmarks(results, "RIGHT_HEEL")
                    LEFT_SHOULDER_X, LEFT_SHOULDER_Y, _ = self.get_landmarks(results, "LEFT_SHOULDER")
                    RIGHT_SHOULDER_X, RIGHT_SHOULDER_Y, _ = self.get_landmarks(results, "RIGHT_SHOULDER")
                    if prev_x is not None and prev_y is not None:
                        #distance = self.calculate_distance(cur_x, cur_y, prev_x, prev_y)
                        distance = self.calculate_distance_one_direction(cur_y, prev_y).round(3)
                        velocity = (distance / self.time_between_frames).round(3)
                        
                        #cv2.putText(image, str(velocity), (50,100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)

                        if velocity < 3:
                            self.all_velocities.append(velocity)

                        if LEFT_HEEL_Y and RIGHT_HEEL_Y and LEFT_SHOULDER_Y and RIGHT_SHOULDER_Y:
                            if LEFT_HEEL_Y > LEFT_SHOULDER_Y and RIGHT_HEEL_Y > RIGHT_SHOULDER_Y:
                                standing = True
                                self.all_standings.append(1)
                            else:
                                standing = False
                                self.all_standings.append(0)
                        #CALCULATE ROLLING AVERAGE
                            if len(self.all_velocities) >= self.velocities_list_length:
                                rolling_avg = np.mean(self.all_velocities[-self.velocities_list_length:])
                                avg_velocity = rolling_avg
                                print(f"Rolling Average: {rolling_avg}")

                                rolling_standings = np.mean(self.all_standings[-self.velocities_list_length:])
                                print(f"Rolling Standings: {rolling_standings}")

                        
                    if avg_velocity is not None and avg_velocity > self.avg_velocity_threshold and rolling_standings < self.rolling_standings_threshold:
                    #if avg_velocity is not None and avg_velocity > self.avg_velocity_threshold:
                        print("FALL DETECTED")
                    
                        print(f"DISTANCE: {distance}")

                        print(f"Average Velocity: {avg_velocity}")
                        print(f"Rolling Standings: {rolling_standings}")

                        fall_detected = True

                    prev_x, prev_y = cur_x, cur_y
                
                #cv2.putText(image, "Fall Detected", (50,50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)
                #cv2.putText(image, "Fall Detected", (50,100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)
                
                if fall_detected:
                    cv2.putText(image, "Fall Detected", (50,50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)
                
                else:
                    cv2.putText(image, "", (50,50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)
                
                # if results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_HEEL].y > results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_SHOULDER].y and results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_HEEL].y > results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_SHOULDER].y:
                #     print("Person is standing")
                # else:


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
        if lndmrk.visibility < 0.5:
            x,y,z = None, None, None
        else:
            x = lndmrk.x
            y = lndmrk.y
            z = lndmrk.z
        return x,y,z

    def calculate_distance(self, x1,y1,x2,y2):
        return np.sqrt((x2-x1)**2 + (y2-y1)**2)
    
    def calculate_distance_one_direction(self, a,b):
        return np.sqrt((a-b)**2)

if __name__ == "__main__":
    fall_detector = FallDetector()