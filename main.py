import pygame
import mediapipe as mp
import numpy as np
import cv2
import json
import re
import sys
import math

from projection import Cube

X_ROT_IDX = (0, 152)
Y_ROT_IDX = ((70, 107) , (300, 336))
Z_ROT_IDX = (105, 334)

def get_rot_z_angle(x, y):
    return math.degrees(math.atan2(y, x)) * 0.05

def get_rot_y_angle(len_difference):
    return math.radians(len_difference * 180) * 0.5

def get_rot_x_angle(len_difference):
    return math.radians(len_difference * 90) * 0.05

def get_dist(point1, point2):
    return math.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)

def smooth(start, end):
    if start < end:
       start = min(end, start + end * 0.1)
    else:
       start = max(end, start - end * 0.1)
    return end

FACE_SCALE = 0

screen = pygame.display.set_mode((600, 400))
display = pygame.Surface((300, 200))

clock = pygame.time.Clock()
pygame.init()

font = pygame.font.Font(size=20)
pygame.font.init()
# Initialize MediaPipe FaceMesh
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh()
draw = mp.solutions.drawing_utils

# Initialize video capture
cap = cv2.VideoCapture(0)
results = None

points = None
pygame.mouse.set_visible(False)

current_a_x = current_a_y = current_a_z = 0

def render_face(surf, rect, render_points, connections):
    # for idx, point in enumerate(render_points):
            
    #         if rect.collidepoint(point):
    #             print(idx)
            
    #         pygame.draw.circle(surf, (255, 255, 255), point, 2)
    
    if render_points:
        for pairs in connections:
            pygame.draw.line(screen, (255, 0, 0), render_points[pairs[0]], render_points[pairs[1]])
            
while True:
    
    render_points = []
    screen.fill((0, 0, 0))
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
    
    l_e_brow = get_dist(render_points[Y_ROT_IDX[0][0]], render_points[Y_ROT_IDX[0][1]])
    r_e_brow = get_dist(render_points[Y_ROT_IDX[1][0]], render_points[Y_ROT_IDX[1][1]]) 
    
    FACE_SCALE = math.sqrt((render_points[159][0] - render_points[386][0]) ** 2 + (render_points[159][1] - render_points[386][1]) ** 2)
    y_diff =  (l_e_brow/r_e_brow) * (1 if r_e_brow < l_e_brow else -1) 
    x_diff = get_dist(render_points[X_ROT_IDX[0]],render_points[X_ROT_IDX[1]])
    
    current_a_x = smooth(current_a_x, get_rot_x_angle(x_diff))
    current_a_y = smooth(current_a_y, get_rot_y_angle(y_diff))
    current_a_z = smooth(current_a_z, get_rot_z_angle(render_points[386][0] - render_points[159][0], render_points[386][1] - render_points[159][1]))
    
    Cube().render(screen, angle_x=current_a_x, angle_y=current_a_y, angle_z=current_a_z)
    
    # print(height)
    # print(math.sqrt((render_points[10][0] - render_points[152][0]) ** 2 + (render_points[10][1] - render_points[152][1]) ** 2) - height)
    
    
    render_face(screen, rect, render_points, connections)
    # pygame.draw.line(screen, (0, 0, 255), render_points[159], render_points[386])
    
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


