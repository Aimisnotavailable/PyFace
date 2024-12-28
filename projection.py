import pygame
from math import *
import numpy as np


class Cube:
    
    def __init__(self):
        self.ROTATE_SPEED = 0.02
        self.scale = 50

        self.projection_matrix = [[1,0,0],
                            [0,1,0],
                            [0,0,0]]

        self.cube_points = [n for n in range(8)]
        self.cube_points[0] = [[-1], [-1], [1]]
        self.cube_points[1] = [[1],[-1],[1]]
        self.cube_points[2] = [[1],[1],[1]]
        self.cube_points[3] = [[-1],[1],[1]]
        self.cube_points[4] = [[-1],[-1],[-1]]
        self.cube_points[5] = [[1],[-1],[-1]]
        self.cube_points[6] = [[1],[1],[-1]]
        self.cube_points[7] = [[-1],[1],[-1]]
        
    def multiply_m(self, a, b) -> list:
        return np.dot(a, b)       


    def connect_points(self, surf, i, j, points) -> None:
        pygame.draw.line(surf, (0, 0, 0), (points[i][0], points[i][1]) , (points[j][0], points[j][1]))

    def get_rotation_x(self, angle_x) -> list:
        rotation_x = [[1, 0, 0],
                    [0, cos(angle_x), -sin(angle_x)],
                    [0, sin(angle_x), cos(angle_x)]]
        return rotation_x

    def get_rotation_y(self, angle_y) -> list:
        rotation_y = [[cos(angle_y), 0, sin(angle_y)],
                        [0, 1, 0],
                        [-sin(angle_y), 0, cos(angle_y)]]
        return rotation_y

    def get_rotation_z(self, angle_z) -> list:
        rotation_z = [[cos(angle_z), -sin(angle_z), 0],
                        [sin(angle_z), cos(angle_z), 0],
                        [0, 0, 1]]
        return rotation_z
    # Main Loop
    

    def render(self, surf, angle_x=0, angle_y=0, angle_z=0):    
        points = [0 for _ in range(len(self.cube_points))]
        i = 0
        
        
        rotation_x = self.get_rotation_x(angle_x)
        rotation_y = self.get_rotation_y(angle_y)
        rotation_z = self.get_rotation_z(angle_z)
        
        for point in self.cube_points:
            rotate_x = self.multiply_m(rotation_x, point)
            rotate_y = self.multiply_m(rotation_y, rotate_x)
            rotate_z = self.multiply_m(rotation_z, rotate_y)
            point_2d = self.multiply_m(self.projection_matrix, rotate_z)
        
            x = (point_2d[0][0] * self.scale) + surf.get_width()//2
            y = (point_2d[1][0] * self.scale) + surf.get_height()//2

            points[i] = (x,y)
            i += 1
            pygame.draw.circle(surf, (255, 0, 0), (x, y), 5)

        self.connect_points(surf, 0, 1, points)
        self.connect_points(surf, 0, 3, points)
        self.connect_points(surf, 0, 4, points)
        self.connect_points(surf, 1, 2, points)
        self.connect_points(surf, 1, 5, points)
        self.connect_points(surf, 2, 6, points)
        self.connect_points(surf, 2, 3, points)
        self.connect_points(surf, 3, 7, points)
        self.connect_points(surf, 4, 5, points)
        self.connect_points(surf,4, 7, points)
        self.connect_points(surf,6, 5, points)
        self.connect_points(surf,6, 7, points)