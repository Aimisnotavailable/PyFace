import pygame
import mediapipe as mp
import numpy as np
import cv2
import json
import re
import sys
import math

from projection import Cube

X_ROT_IDX = (105, 334)
Y_ROT_IDX = ((70, 107) , (300, 336))
Z_ROT_IDX = (105, 334)

def get_rot_z_angle(x, y):
    return math.degrees(math.atan2(y, x)) * 0.6

def get_rot_y_angle(len_difference):
    return math.radians(len_difference + 90) * 0.6

def get_dist(point1, point2):
    return math.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)

FACE_SCALE = 0

screen = pygame.display.set_mode((600, 400))
display = pygame.Surface((300, 200))

clock = pygame.time.Clock()
pygame.init()
# Initialize MediaPipe FaceMesh
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh()
draw = mp.solutions.drawing_utils

# Initialize video capture
cap = cv2.VideoCapture(0)
results = None

points = None
pygame.mouse.set_visible(False)


while True:
    
    render_points = []
    screen.fill((255, 255, 255))
    display.fill((255, 255, 255))
    success, image = cap.read()
    
    height, width, _ = image.shape
    # Convert the BGR image to RGB
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Process the image to find face landmarks
    results = face_mesh.process(rgb_image)
    
    if results.multi_face_landmarks:
        points = results.multi_face_landmarks[0].landmark
    
    if points:
        for point in points:
            render_points.append([(point.x * width), (point.y * height)])
    
    connections = mp_face_mesh.FACEMESH_CONTOURS

    mpos = pygame.mouse.get_pos() #[pygame.mouse.get_pos()[0] // 2, pygame.mouse.get_pos()[1] // 2]
    rect = pygame.Rect(*mpos, 2, 2)
    
    # print(get_rot_z_angle(render_points[386][0] - render_points[159][0], render_points[386][1] - render_points[159][1]))
    pygame.draw.rect(screen, (0, 0, 0), rect, 10)
    for idx, point in enumerate(render_points):
        
        if rect.collidepoint(point):
            print(idx)
         
        pygame.draw.circle(screen, (0, 0, 0), point, 2)
    
    FACE_SCALE = math.sqrt((render_points[159][0] - render_points[386][0]) ** 2 + (render_points[159][1] - render_points[386][1]) ** 2)
    diff = get_dist(render_points[Y_ROT_IDX[0][0]], render_points[Y_ROT_IDX[0][1]]) - get_dist(render_points[Y_ROT_IDX[1][0]], render_points[Y_ROT_IDX[1][1]]) 
    Cube().render(screen, angle_y=get_rot_y_angle(diff), angle_z=get_rot_z_angle(render_points[386][0] - render_points[159][0], render_points[386][1] - render_points[159][1]))
    # print(height)
    # print(math.sqrt((render_points[10][0] - render_points[152][0]) ** 2 + (render_points[10][1] - render_points[152][1]) ** 2) - height)
    
    if render_points:
        for pairs in connections:
            pygame.draw.line(screen, (255, 0, 0), render_points[pairs[0]], render_points[pairs[1]])
    
    pygame.draw.line(screen, (0, 0, 255), render_points[159], render_points[386])
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            cap.release()
            pygame.quit()
            sys.exit()
    
    #screen.blit(pygame.transform.scale(display, screen.get_size()), (0, 0))
    pygame.display.update()
    clock.tick(60)
    
# while cap.isOpened():
#     success, image = cap.read()
#     if not success:
#         break

#     # Convert the BGR image to RGB
#     rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

#     # Process the image to find face landmarks
#     results = face_mesh.process(rgb_image)
    
#     if results.multi_face_landmarks:
#         print(type(results.multi_face_landmarks[0].landmark[0:16]))
            
#     cv2.imshow("window", image)
    
#     if cv2.waitKey(5) & 0xFF == 27:
#         break

# # result =  re.sub(r'landmark \{|\}|\[|\]|\n', '', str(results.multi_face_landmarks)).strip()
# # file = open('test.json', 'w+')
# # json.dump({'result' : result.split('  ')}, file)


