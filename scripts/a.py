import mediapipe as mp
import math
import cv2

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

# initialize the pose detection model
pose = mp_pose.Pose()

# define a threshold for the change in velocity
velocity_threshold = 1.0

# define a counter for the number of consecutive frames in which a fall has been detected
fall_counter = 0
cap = cv2.VideoCapture(0)


while True:
    # capture the video feed and convert to RGB
    success, image = cap.read()
    if not success:
        break
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
    # process the image and detect the pose landmarks
    results = pose.process(image)
    
    # extract the pose landmarks
    landmarks = results.pose_landmarks
    
    # calculate the velocity of the body
    if landmarks is not None:
        # extract the x, y coordinates of the center of the body
        x_center = (landmarks.landmark[mp_pose.PoseLandmark.LEFT_SHOULDER].x + landmarks.landmark[mp_pose.PoseLandmark.RIGHT_SHOULDER].x) / 2
        y_center = (landmarks.landmark[mp_pose.PoseLandmark.LEFT_SHOULDER].y + landmarks.landmark[mp_pose.PoseLandmark.RIGHT_SHOULDER].y) / 2

        # calculate the distance traveled by the center of the body in the previous frame
        if 'prev_x_center' in locals() and 'prev_y_center' in locals():
            distance = math.sqrt((x_center - prev_x_center) ** 2 + (y_center - prev_y_center) ** 2)
            velocity = distance / 0.033  # assuming a frame rate of 30 fps
            print(velocity)
        else:
            velocity = 0

        # store the current x, y coordinates for the next frame
        prev_x_center = x_center
        prev_y_center = y_center

        # analyze the velocity and posture to detect a fall event
        if velocity > velocity_threshold:
            fall_counter += 1
        else:
            fall_counter = 0

        if fall_counter >= 3 and landmarks.landmark[mp_pose.PoseLandmark.NOSE].y <= landmarks.landmark[mp_pose.PoseLandmark.LEFT_SHOULDER].y:
            # the body is nearly horizontal, indicating a fall event
            print("Fall detected!")
            # reset the fall counter
            fall_counter = 0

    # draw the pose landmarks on the image
    mp_drawing.draw_landmarks(
        image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
    
    # display the image
    cv2.imshow('MediaPipe Pose', image)
    if cv2.waitKey(5) & 0xFF == 27:
        break

# release the video capture and destroy the windows
cap.release()
cv2.destroyAllWindows()
