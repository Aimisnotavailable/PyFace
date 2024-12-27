import pygame
import mediapipe as mp
import numpy as np
import cv2
import json
import re

# Initialize MediaPipe FaceMesh
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh()
draw = mp.solutions.drawing_utils

# Initialize video capture
cap = cv2.VideoCapture(0)
results = None
while cap.isOpened():
    success, image = cap.read()
    if not success:
        break

    # Convert the BGR image to RGB
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Process the image to find face landmarks
    results = face_mesh.process(rgb_image)
    
    if results.multi_face_landmarks:
        print(type(results.multi_face_landmarks[0].landmark[0:16]))
            
    cv2.imshow("window", image)
    
    if cv2.waitKey(5) & 0xFF == 27:
        break

# result =  re.sub(r'landmark \{|\}|\[|\]|\n', '', str(results.multi_face_landmarks)).strip()
# file = open('test.json', 'w+')
# json.dump({'result' : result.split('  ')}, file)

cap.release()
cv2.destroyAllWindows()
