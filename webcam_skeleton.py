import cv2
import mediapipe as mp
import math
import socket
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_pose = mp.solutions.pose

# socket client config
HOST = '127.0.0.1'
PORT = 8000
server_addr = (HOST, PORT)
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# For webcam input:
cap = cv2.VideoCapture(0)
with mp_pose.Pose(
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as pose:
  while cap.isOpened():
    success, image = cap.read()
    if not success:
      print("Ignoring empty camera frame.")
      # If loading a video, use 'break' instead of 'continue'.
      continue

    # To improve performance, optionally mark the image as not writeable to
    # pass by reference.
    image.flags.writeable = False
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = pose.process(image)

    # Draw the pose annotation on the image.
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    mp_drawing.draw_landmarks(
        image,
        results.pose_landmarks,
        mp_pose.POSE_CONNECTIONS,
        landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style())
    
    
    # print specipic landmark, see https://google.github.io/mediapipe/solutions/pose.html#output

    
    clientMsg = "no movement"
    # move left up
    if results.pose_landmarks.landmark[15].y < results.pose_landmarks.landmark[13].y and results.pose_landmarks.landmark[13].y < results.pose_landmarks.landmark[11].y:
      print("move left up")
      clientMsg = "move left up"

    # move left down    
    x_length_left = results.pose_landmarks.landmark[15].x - results.pose_landmarks.landmark[11].x
    y_length_left = results.pose_landmarks.landmark[15].y - results.pose_landmarks.landmark[11].y
    tan_left = y_length_left/x_length_left
    if results.pose_landmarks.landmark[15].y > results.pose_landmarks.landmark[13].y and results.pose_landmarks.landmark[13].y > results.pose_landmarks.landmark[11].y and tan_left < math.tan(math.pi/3):
      print("move left down")
      clientMsg = "move left down"

    # move right up
    if results.pose_landmarks.landmark[16].y < results.pose_landmarks.landmark[14].y and results.pose_landmarks.landmark[14].y < results.pose_landmarks.landmark[12].y:
      print("move right up")
      clientMsg = "move right up"

    # move right down
    x_length_right = results.pose_landmarks.landmark[12].x - results.pose_landmarks.landmark[16].x
    y_length_rigth = results.pose_landmarks.landmark[16].y - results.pose_landmarks.landmark[12].y
    tan_right = y_length_rigth/x_length_right
    if results.pose_landmarks.landmark[16].y > results.pose_landmarks.landmark[14].y and results.pose_landmarks.landmark[14].y > results.pose_landmarks.landmark[12].y and tan_right < math.tan(math.pi/3):
      print("move right down")
      clientMsg = "move right down"
    
    # send movement direction to nodeJS server via UDP
    client.sendto(clientMsg.encode(), server_addr)
    
    # Flip the image horizontally for a selfie-view display.
    cv2.imshow('MediaPipe Pose', cv2.flip(image, 1))
    if cv2.waitKey(5) & 0xFF == 27:
      break
cap.release()