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
        self.velocities_list_length = 18
        self.avg_velocity_threshold = 1
        self.all_NOSE_velocities = []
        self.all_standings = []
        self.all_joints_velocities = []
        self.landmarks_dict = {
            "NOSE"      :self.mp_pose.PoseLandmark.NOSE,
            "LEFT_WRIST":self.mp_pose.PoseLandmark.LEFT_WRIST,
            "RIGHT_WRIST":self.mp_pose.PoseLandmark.RIGHT_WRIST,
            "LEFT_HEEL" :self.mp_pose.PoseLandmark.LEFT_HEEL,
            "RIGHT_HEEL":self.mp_pose.PoseLandmark.RIGHT_HEEL,
            "LEFT_SHOULDER":self.mp_pose.PoseLandmark.LEFT_SHOULDER,
            "RIGHT_SHOULDER":self.mp_pose.PoseLandmark.RIGHT_SHOULDER,
            "LEFT_ELBOW":self.mp_pose.PoseLandmark.LEFT_ELBOW,
            "RIGHT_ELBOW":self.mp_pose.PoseLandmark.RIGHT_ELBOW,
            "LEFT_KNEE":self.mp_pose.PoseLandmark.LEFT_KNEE,
            "RIGHT_KNEE":self.mp_pose.PoseLandmark.RIGHT_KNEE,
        }

        self.log_file = self.create_log_file()
        self.detect_fall()
        #cap = cv2.VideoCapture(0)
        #cap = cv2.VideoCapture(".\WIN_20230501_20_42_48_Pro.mp4")
    
    def create_log_file(self):
        now = datetime.now()
        file_name = now.strftime("%d-%m-%Y_%H-%M-%S")
        log_file = open(f"{file_name}.json", "w")
        return log_file

    def detect_fall(self):
        frame_num = 0

        #cap = cv2.VideoCapture(".\\videoplayback.mp4")
        cap = cv2.VideoCapture(".\\videoplayback.mp4")

        #prev_NOSE_X, prev_NOSE_Y = None, None
        velocities = []

        # prev_NOSE_Y = "xxx"
        # prev_LEFT_WRIST_Y = "xxx"
        # prev_LEFT_HEEL_Y = "xxx"


        with self.mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
            prev_NOSE_Y = None
            prev_LEFT_HEEL_Y = None
            prev_LEFT_WRIST_Y = None
            prev_LEFT_SHOULDER_Y = None
            prev_RIGHT_SHOULDER_Y = None
            prev_LEFT_ELBOW_Y = None
            prev_RIGHT_ELBOW_Y = None
            prev_LEFT_KNEE_Y = None
            prev_RIGHT_KNEE_Y = None
            prev_RIGHT_WRIST_Y = None
            prev_RIGHT_HEEL_Y = None

            while cap.isOpened():
                _, frame = cap.read()
                frame_num += 1
                image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                image.flags.writeable = False
                fall_detected = False
                skip_frame = True

                results = pose.process(image)
                image.flags.writeable = True
                image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

                if results.pose_landmarks:
                    _, cur_NOSE_Y, _ = self.get_landmarks(results, "NOSE")
                    _, cur_LEFT_HEEL_Y, _ = self.get_landmarks(results, "LEFT_HEEL")
                    _, cur_LEFT_WRIST_Y, _ = self.get_landmarks(results, "LEFT_WRIST")
                    _, cur_LEFT_SHOULDER_Y, _ = self.get_landmarks(results, "LEFT_SHOULDER")
                    _, cur_RIGHT_SHOULDER_Y, _ = self.get_landmarks(results, "RIGHT_SHOULDER")
                    _, cur_LEFT_ELBOW_Y, _ = self.get_landmarks(results, "LEFT_ELBOW")
                    _, cur_RIGHT_ELBOW_Y, _ = self.get_landmarks(results, "RIGHT_ELBOW")
                    _, cur_LEFT_KNEE_Y, _ = self.get_landmarks(results, "LEFT_KNEE")
                    _, cur_RIGHT_KNEE_Y, _ = self.get_landmarks(results, "RIGHT_KNEE")
                    _, cur_RIGHT_WRIST_Y, _ = self.get_landmarks(results, "RIGHT_WRIST")
                    _, cur_RIGHT_HEEL_Y, _ = self.get_landmarks(results, "RIGHT_HEEL")


                    if prev_NOSE_Y is not None and prev_LEFT_HEEL_Y is not None and prev_LEFT_WRIST_Y is not None and \
                            prev_LEFT_SHOULDER_Y is not None and prev_RIGHT_SHOULDER_Y is not None and\
                            prev_LEFT_ELBOW_Y is not None and prev_RIGHT_ELBOW_Y is not None and \
                            prev_LEFT_KNEE_Y is not None and prev_RIGHT_KNEE_Y is not None and \
                            prev_RIGHT_WRIST_Y is not None and prev_RIGHT_HEEL_Y is not None:
                        
                        NOSE_distance = self.calculate_distance_one_direction(cur_NOSE_Y, prev_NOSE_Y).round(3)
                        NOSE_velocity = (NOSE_distance / self.time_between_frames).round(3)
                        #print(f"NOSE_velocity: {NOSE_velocity}")

                        LEFT_HEEL_distance = self.calculate_distance_one_direction(cur_LEFT_HEEL_Y, prev_LEFT_HEEL_Y)
                        LEFT_HEEL_velocity = (LEFT_HEEL_distance / self.time_between_frames).round(3)
                        #print(f"LEFT_HEEL_velocity: {LEFT_HEEL_velocity}")
                        
                        LEFT_WRIST_distance = self.calculate_distance_one_direction(cur_LEFT_WRIST_Y, prev_LEFT_WRIST_Y)
                        LEFT_WRIST_velocity = (LEFT_WRIST_distance / self.time_between_frames).round(3)
                        #print(f"LEFT_WRIST_velocity: {LEFT_WRIST_velocity}")

                        LEFT_SHOULDER_distance = self.calculate_distance_one_direction(cur_LEFT_SHOULDER_Y, prev_LEFT_SHOULDER_Y)
                        LEFT_SHOULDER_velocity = (LEFT_SHOULDER_distance / self.time_between_frames).round(3)
                        #print(f"LEFT_SHOULDER_velocity: {LEFT_SHOULDER_velocity}")

                        RIGHT_SHOULDER_distance = self.calculate_distance_one_direction(cur_RIGHT_SHOULDER_Y, prev_RIGHT_SHOULDER_Y)
                        RIGHT_SHOULDER_velocity = (RIGHT_SHOULDER_distance / self.time_between_frames).round(3)
                        #print(f"RIGHT_SHOULDER_velocity: {RIGHT_SHOULDER_velocity}")

                        LEFT_ELBOW_distance = self.calculate_distance_one_direction(cur_LEFT_ELBOW_Y, prev_LEFT_ELBOW_Y)
                        LEFT_ELBOW_velocity = (LEFT_ELBOW_distance / self.time_between_frames).round(3)
                        #print(f"LEFT_ELBOW_velocity: {LEFT_ELBOW_velocity}")

                        RIGHT_ELBOW_distance = self.calculate_distance_one_direction(cur_RIGHT_ELBOW_Y, prev_RIGHT_ELBOW_Y)
                        RIGHT_ELBOW_velocity = (RIGHT_ELBOW_distance / self.time_between_frames).round(3)
                        #print(f"RIGHT_ELBOW_velocity: {RIGHT_ELBOW_velocity}")

                        LEFT_KNEE_distance = self.calculate_distance_one_direction(cur_LEFT_KNEE_Y, prev_LEFT_KNEE_Y)
                        LEFT_KNEE_velocity = (LEFT_KNEE_distance / self.time_between_frames).round(3)
                        #print(f"LEFT_KNEE_velocity: {LEFT_KNEE_velocity}")

                        RIGHT_KNEE_distance = self.calculate_distance_one_direction(cur_RIGHT_KNEE_Y, prev_RIGHT_KNEE_Y)
                        RIGHT_KNEE_velocity = (RIGHT_KNEE_distance / self.time_between_frames).round(3)
                        #print(f"RIGHT_KNEE_velocity: {RIGHT_KNEE_velocity}")

                        RIGHT_WRIST_distance = self.calculate_distance_one_direction(cur_RIGHT_WRIST_Y, prev_RIGHT_WRIST_Y)
                        RIGHT_WRIST_velocity = (RIGHT_WRIST_distance / self.time_between_frames).round(3)
                        #print(f"RIGHT_WRIST_velocity: {RIGHT_WRIST_velocity}")

                        RIGHT_HEEL_distance = self.calculate_distance_one_direction(cur_RIGHT_HEEL_Y, prev_RIGHT_HEEL_Y)
                        RIGHT_HEEL_velocity = (RIGHT_HEEL_distance / self.time_between_frames).round(3)
                        #print(f"RIGHT_HEEL_velocity: {RIGHT_HEEL_velocity}")

                        print("......................")

                        if len(self.all_joints_velocities) == 18:
                            print(self.all_joints_velocities)
                            self.all_joints_velocities = []
                            print("all_joints_velocities reset")
                        
                        self.all_joints_velocities.append(NOSE_velocity)
                        self.all_joints_velocities.append(LEFT_HEEL_velocity)
                        self.all_joints_velocities.append(LEFT_WRIST_velocity)
                        self.all_joints_velocities.append(LEFT_SHOULDER_velocity)
                        self.all_joints_velocities.append(RIGHT_SHOULDER_velocity)
                        self.all_joints_velocities.append(LEFT_ELBOW_velocity)
                        self.all_joints_velocities.append(RIGHT_ELBOW_velocity)
                        self.all_joints_velocities.append(LEFT_KNEE_velocity)
                        self.all_joints_velocities.append(RIGHT_KNEE_velocity)
                        self.all_joints_velocities.append(RIGHT_WRIST_velocity)
                        self.all_joints_velocities.append(RIGHT_HEEL_velocity)


                        cv2.putText(image, str(NOSE_velocity), (50,50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)
                        cv2.putText(image, str(LEFT_HEEL_velocity), (50,100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)
                        cv2.putText(image, str(LEFT_WRIST_velocity), (50,150), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)
                        cv2.putText(image, str(LEFT_WRIST_velocity), (50,250), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)

                    # Store current NOSE y coordinate for use in next iteration
                    prev_NOSE_Y = cur_NOSE_Y
                    prev_LEFT_HEEL_Y = cur_LEFT_HEEL_Y
                    prev_LEFT_WRIST_Y = cur_LEFT_WRIST_Y
                    prev_LEFT_SHOULDER_Y = cur_LEFT_SHOULDER_Y
                    prev_RIGHT_SHOULDER_Y = cur_RIGHT_SHOULDER_Y
                    prev_LEFT_ELBOW_Y = cur_LEFT_ELBOW_Y
                    prev_RIGHT_ELBOW_Y = cur_RIGHT_ELBOW_Y
                    prev_LEFT_KNEE_Y = cur_LEFT_KNEE_Y
                    prev_RIGHT_KNEE_Y = cur_RIGHT_KNEE_Y
                    prev_RIGHT_WRIST_Y = cur_RIGHT_WRIST_Y
                    prev_RIGHT_HEEL_Y = cur_RIGHT_HEEL_Y



                    #_,cur_LEFT_WRIST_Y,_ = self.get_landmarks(results, "LEFT_WRIST")
                   # _,cur_LEFT_HEEL_Y,_ = self.get_landmarks(results, "LEFT_HEEL")
                    '''
                    #if prev_NOSE_Y == "xxx" and prev_LEFT_WRIST_Y == "xxx" and prev_LEFT_HEEL_Y == "xxx":
                    if prev_NOSE_Y == "xxx":
                        prev_NOSE_Y = cur_NOSE_Y
                        #prev_LEFT_WRIST_Y = cur_LEFT_WRIST_Y
                        #prev_LEFT_HEEL_Y = cur_LEFT_HEEL_Y
                        continue
                
                    if prev_NOSE_Y is not None:
                    #if prev_NOSE_Y is not None and prev_LEFT_WRIST_Y is not None and prev_LEFT_HEEL_Y is not None:
                        NOSE_distance = self.calculate_distance_two_directions(cur_NOSE_Y, prev_NOSE_Y)
                        #LEFT_WRIST_distance = self.calculate_distance_two_directions(cur_LEFT_WRIST_Y, prev_LEFT_WRIST_Y)
                        #LEFT_HEEL_distance = self.calculate_distance_two_directions(cur_LEFT_HEEL_Y, prev_LEFT_HEEL_Y)

                        NOSE_velocity = NOSE_distance / self.time_between_frames
                        #LEFT_WRIST_velocity = LEFT_WRIST_distance / self.time_between_frames
                        #LEFT_HEEL_velocity = LEFT_HEEL_distance / self.time_between_frames

                        print(NOSE_velocity)


                        prev_NOSE_Y = cur_NOSE_Y
                        # prev_LEFT_WRIST_Y = cur_LEFT_WRIST_Y
                        # prev_LEFT_HEEL_Y = cur_LEFT_HEEL_Y

                '''


                '''
                if results.pose_landmarks:
                    cur_NOSE_X,cur_NOSE_Y,_ = self.get_landmarks(results, "NOSE")
                    if prev_NOSE_X is not None and prev_NOSE_Y is not None:
                        NOSE_distance = self.calculate_distance_two_directions(cur_NOSE_X, cur_NOSE_Y, prev_NOSE_X, prev_NOSE_Y)
                        NOSE_velocity = NOSE_distance / self.time_between_frames
                        self.all_NOSE_velocities.append(NOSE_velocity)

                        if len(self.all_NOSE_velocities) >= self.velocities_list_length:
                            rolling_avg = np.mean(self.all_NOSE_velocities[-self.velocities_list_length:])
                            avg_velocity = rolling_avg
                            print(avg_velocity)


                        #cv2.putText(image, f"X Distance: {x_distance} Y Distance: {y_distance}", (50,50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)

                    prev_NOSE_X, prev_NOSE_Y = cur_NOSE_X, cur_NOSE_Y
                '''

                # if fall_detected:
                #     cv2.putText(image, "Fall Detected", (50,50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)

                # else:
                #     cv2.putText(image, "", (50,50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)

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

    def calculate_distance_two_directions(self, x1,y1,x2,y2):
        return np.sqrt((x2-x1)**2 + (y2-y1)**2)

    def calculate_distance_one_direction(self, a,b):
        return np.sqrt((a-b)**2)

if __name__ == "__main__":
    fall_detector = FallDetector()