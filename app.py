import pygame
import mediapipe as mp
import numpy as np
import cv2
import json
import re
import sys
import math

from engine import Engine
from smooth import Smooth
from projection import Cube, Polygon
from camera import Scroll, Follow
from copy import deepcopy

BASE_DIR = 'shapes/'
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

class PyFace(Engine):

    def __init__(self, dim=(600, 400), font_size=20):
        super().__init__(dim, font_size)
        pygame.mouse.set_visible(False)

        self.mp_face_mesh = mp.solutions.face_mesh
        self.face_mesh =    self.mp_face_mesh.FaceMesh()

        self.mp_hand_mesh = mp.solutions.hands
        self.hand_mesh = self.mp_hand_mesh.Hands(max_num_hands=2)

        # Initialize video capture
        self.cap = cv2.VideoCapture(0)
        self.results = None

        self.points = None
        self.current_a_x = self.current_a_y = self.current_a_z = 0
    
    def get_rot_z_angle(self, x, y):
        return math.atan2(y, x)

    def get_rot_y_angle(self, len_difference):
        return math.radians(len_difference)

    def get_rot_x_angle(self, len_difference):
        return math.radians(len_difference)

    def get_dist(self, point1, point2):
        return math.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)
    
    def load(self, file_name='') -> dict[str : Polygon]:
        fp = open(BASE_DIR + file_name, 'r+')
        data = json.load(fp)
        shapes : dict[str : Polygon] = {}
        if fp:
            for img_data in data:
                for img in img_data:
                    conn = [i for i in range(len(img_data[img]['3d']))]
                    shapes[img] = Polygon(img_data[img]['3d'], connection=[{'color' : img_data[img]['color'], 'points' : conn}])
        fp.close()
        return shapes

    def render(self, surf, render_points, connections):
        for idx, point in enumerate(render_points):
                pygame.draw.circle(surf, (255, 255, 255) if not idx in X_ROT_IDX else (255, 0, 255), point, 2)

        if render_points:
            for pairs in connections:
                pygame.draw.line(surf, (255, 0, 0), render_points[pairs[0]], render_points[pairs[1]])

    def run(self):
        pass

