import pygame
import mediapipe as mp
import numpy as np
import cv2
import json
import re
import sys
import math

from smooth import Smooth
from projection import Cube, Polygon
from camera import Scroll, Follow
from copy import deepcopy
HIST_SIZE = 60

MAX_SCALE = 135
MIN_SCALE = 45
MEDIAN_SCALE = (MAX_SCALE + MIN_SCALE) // 2

FACE_SCALE = 1

R_INTRV = 0.1

X_ROT_IDX =  (4, 242) # (0, 152)  #
Y_ROT_IDX = ((70, 107) , (300, 336))
Z_ROT_IDX = (105, 334)

R_EYE_IDX = (145, 159)
L_EYE_IDX = (374, 386)
MOUTH_IDX = ((78, 308), (14, 13))

MAX_MOUTH_X = 75
MAX_MOUTH_Y = 41

MAX_L_EYE_SIZE = 11
MAX_R_EYE_SIZE = 11


OFFSET_IDX = ((10, 152))

def get_rot_z_angle(x, y):
    return math.atan2(y, x)

def get_rot_y_angle(len_difference):
    return math.radians(len_difference)

def get_rot_x_angle(len_difference):
    return math.radians(len_difference)

def get_dist(point1, point2):
    return math.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)

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
data = []
smooth = Smooth()
current_a_x = current_a_y = current_a_z = 0

def render_face(surf, rect, render_points, connections):
    for idx, point in enumerate(render_points):
            
            if rect.collidepoint(point):
                print(idx)
            
            pygame.draw.circle(surf, (255, 255, 255) if not idx in X_ROT_IDX else (255, 0, 255), point, 2)
    
    #connections = MOUTH_IDX
    if render_points:
        for pairs in connections:
            pygame.draw.line(screen, (255, 0, 0), render_points[pairs[0]], render_points[pairs[1]])

x = 0
y = 0
z = 0

fp = open('shapes/test.json', 'r+')
data = json.load(fp)
shapes : dict[str : Polygon] = {}
camera = Follow(depth=30)


for img_data in data:
    for img in img_data:
        conn = [i for i in range(len(img_data[img]['3d']))]
        shapes[img] = Polygon(img_data[img]['3d'], connection=[{'color' : img_data[img]['color'], 'points' : conn}])

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
    pygame.draw.rect(screen, (255, 255, 0), rect, 20)
    
    FACE_SCALE = max(MIN_SCALE, min(MAX_SCALE, math.sqrt((render_points[159][0] - render_points[386][0]) ** 2 + (render_points[159][1] - render_points[386][1]) ** 2)))
    scale_factor = FACE_SCALE / MEDIAN_SCALE
    
    l_e_brow = get_dist(render_points[Y_ROT_IDX[0][0]], render_points[Y_ROT_IDX[0][1]])
    r_e_brow = get_dist(render_points[Y_ROT_IDX[1][0]], render_points[Y_ROT_IDX[1][1]]) 
    
    y_diff =  (l_e_brow - r_e_brow) # * (1 if r_e_brow < l_e_brow else -1) 
    x_diff = get_dist(render_points[X_ROT_IDX[0]],render_points[X_ROT_IDX[1]])
    
    
    current_a_x = get_rot_x_angle(x_diff / scale_factor)
    current_a_y = get_rot_y_angle(y_diff / scale_factor)
    current_a_z = get_rot_z_angle(render_points[386][0] - render_points[159][0], render_points[386][1] - render_points[159][1])
    x_pos = (render_points[OFFSET_IDX[0]][0] - render_points[OFFSET_IDX[1]][0])
    y_pos = (render_points[OFFSET_IDX[0]][1] - render_points[OFFSET_IDX[1]][1])
    movement = (0,0)
    
    mouth_scale = [(get_dist(render_points[MOUTH_IDX[0][0]], render_points[MOUTH_IDX[0][1]]) / scale_factor) / MAX_MOUTH_X, 
                   (get_dist(render_points[MOUTH_IDX[1][0]], render_points[MOUTH_IDX[1][1]]) / scale_factor) / MAX_MOUTH_Y]
    
    # print((get_dist(render_points[MOUTH_IDX[1][0]], render_points[MOUTH_IDX[1][1]]) / scale_factor))
    current_l_eye_size = get_dist(render_points[L_EYE_IDX[0]], render_points[L_EYE_IDX[1]]) / scale_factor
    current_r_eye_size = get_dist(render_points[R_EYE_IDX[0]], render_points[R_EYE_IDX[1]]) / scale_factor
    
    l_eye_scale = current_l_eye_size / MAX_L_EYE_SIZE
    r_eye_scale = current_r_eye_size / MAX_R_EYE_SIZE
    #movement = camera.scroll(screen, (x_pos, y_pos))
    
    # screen.blit(font.render(f'MOVEMENT : [{movement[0] : .3f}, {movement[1] : .3f}]', True, (255, 255 ,255)), (50, 160))
    screen.blit(font.render(f'EYE SCALE : [{l_eye_scale : .3f}, {r_eye_scale : .3f}]', True, (255, 255 ,255)), (50, 140))
    screen.blit(font.render(f'MOUTH SCALE : [{mouth_scale[0] : .3f}, {mouth_scale[1] : .3f}]', True, (255, 255 ,255)), (50, 160))
    screen.blit(font.render(f'SCALE : {scale_factor : .3f}', True, (255, 255 ,255)), (50, 180))
    screen.blit(font.render(f'ROT X: {current_a_x : .3f}', True, (255, 255, 255)), (50, 200))
    screen.blit(font.render(f'ROT Y: {current_a_y : .3f}', True, (255, 255, 255)), (50, 220))
    screen.blit(font.render(f'ROT Z: {current_a_z : .3f}', True, (255, 255, 255)), (50, 240))
    
    for key, shape in shapes.items():
        temp = None
        if 'eye' in key:
            current_distance = get_dist(shape.points[0][0:2], shape.points[2][0:2])
            temp = deepcopy(shape.points)
            diff = current_distance - (current_distance * (r_eye_scale if key == 'reye' else l_eye_scale))
            
            shape.points[0][1] += diff * 0.9
            shape.points[2][1] -= diff * 0.9
        
        if 'mouth' in key:
            current_x_distance = get_dist(shape.points[0][0:2], shape.points[2][0:2])
            current_y_distance = get_dist(shape.points[1][0:2], shape.points[3][0:2])
            
            temp = deepcopy(shape.points)
            x_diff = current_x_distance - (current_x_distance * mouth_scale[0])
            y_diff = current_y_distance - (current_y_distance * mouth_scale[1])
            
            print(y_diff)
            shape.points[0][0] += x_diff * 0.9
            shape.points[2][0] -= x_diff * 0.9
            
            shape.points[1][1] -= y_diff / 2
            shape.points[3][1] += y_diff / 2
            
        
        shape.render(screen, scale_factor + 0.3, camera, movement, current_a_x, current_a_y, current_a_z)
        
        if temp:
            shape.points = temp
    # Cube().render(screen, angle_x=current_a_x, angle_y=current_a_y, angle_z=current_a_z)
    
    
    # print(height)
    # print(math.sqrt((render_points[10][0] - render_points[152][0]) ** 2 + (render_points[10][1] - render_points[152][1]) ** 2) - height)
    
    
    # render_face(screen, rect, render_points, connections)
    # pygame.draw.line(screen, (0, 0, 255), render_points[159], render_points[386])
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            fp =open('test.json', 'w+')
            json.dump(FACE_SCALE, fp)
            cap.release()
            pygame.quit()
            sys.exit()
        
        # if event.type == pygame.MOUSEBUTTONDOWN:
        #     if event.button == 4:
        #         FACE_SCALE = min(2, FACE_SCALE + 0.02)
        #     if event.button == 5:
        #         FACE_SCALE = max(0.5, FACE_SCALE - 0.02)

        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_w]:
            x += R_INTRV
        if keys[pygame.K_s]:
            x -= R_INTRV
        if keys[pygame.K_a]:
            y += R_INTRV
        if keys[pygame.K_d]: 
            y -= R_INTRV
        if keys[pygame.K_q]:
            z += R_INTRV
        if keys[pygame.K_e]:     
            z -= R_INTRV
        
        if keys[pygame.K_r]:
            x=y=z=0
            
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


