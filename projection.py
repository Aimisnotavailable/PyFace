import pygame
import math
import numpy as np

class Projection:
    def __init__(self, fov, aspect_ratio, near, far):
        self.fov = fov
        self.aspect_ratio = aspect_ratio
        self.near = near
        self.far = far
        self.update_projection_matrix()

    def update_projection_matrix(self):
        f = 1 / math.tan(math.radians(self.fov) / 2)
        nf = 1 / (self.near - self.far)

        self.projection_matrix = [
            [f / self.aspect_ratio, 0, 0, 0],
            [0, f, 0, 0],
            [0, 0, (self.far + self.near) * nf, -1],
            [0, 0, (2 * self.far * self.near) * nf, 0]
        ]

        # self.projection_matrix = [[1,0,0],
        #                     [0,1,0],
        #                     [0,0,1]]

    def get_rotation_x(self, angle_x) -> list:
        rotation_x = [[1, 0, 0],
                    [0, math.cos(angle_x), -math.sin(angle_x)],
                    [0, math.sin(angle_x), math.cos(angle_x)]]
        return rotation_x

    def get_rotation_y(self, angle_y) -> list:
        rotation_y = [[math.cos(angle_y), 0, math.sin(angle_y)],
                        [0, 1, 0],
                        [-math.sin(angle_y), 0, math.cos(angle_y)]]
        return rotation_y

    def get_rotation_z(self, angle_z) -> list:
        rotation_z = [[math.cos(angle_z), -math.sin(angle_z), 0],
                        [math.sin(angle_z), math.cos(angle_z), 0],
                        [0, 0, 1]]
        return rotation_z
    
    def multiply_m(self, a, b) -> list:
        return np.dot(a, b)       

class Polygon:
    
    def __init__(self, points=[], connection=[]):
        self.projection = Projection(90, 16/9, 0.01, 1)
        self.points = points
        self.connections = connection
        # self.points = [n for n in range(8)]
        # self.points[0] = [[-1], [-1], [1]]
        # self.points[1] = [[-1], [1], [1]]
        # self.points[2] = [[1], [1], [1]]
        # self.points[3] = [[1], [-1], [1]]
        
        # self.points[4] = [[-1], [-1], [-1]]
        # self.points[5] = [[-1], [1], [-1]]
        # self.points[6] = [[1], [1], [-1]]
        # self.points[7] = [[1], [-1], [-1]]
        
        # self.connections = [ 
        #                      {'color' : (255, 0, 0), 'points' : (4, 5, 6, 7)}, # back
        #                      {'color' : (0, 255, 0), 'points' : (0, 4, 7, 3)}, # top
        #                      {'color' : (0, 0, 255), 'points' : (1, 2, 6, 5)}, # bottom
        #                      {'color' : (255, 255, 0), 'points' : (4, 0, 1, 5)}, # left
        #                      {'color' : (0, 255, 255), 'points' : (3, 2, 6, 7)}, # right
        #                      {'color' : (255, 255, 255), 'points' : (0, 1, 2, 3)}, # front
        #                      ]

    def update(self, surf, scale, angle_x, angle_y, angle_z):
        points = [0 for _ in range(len(self.points))]
        i = 0
        rotation_x = self.projection.get_rotation_x(angle_x)
        rotation_y = self.projection.get_rotation_y(angle_y)
        rotation_z = self.projection.get_rotation_z(angle_z)
        
        for point in self.points:
            rotate_x = self.projection.multiply_m(rotation_x, point)
            rotate_y = self.projection.multiply_m(rotation_y, rotate_x)
            rotate_z = self.projection.multiply_m(rotation_z, rotate_y)

            rotate_z = np.append(rotate_z, [1], axis=0)

            point_2d = self.projection.multiply_m(self.projection.projection_matrix, rotate_z)
            
            x = (point_2d[0] * scale * 2) + surf.get_width() // 4
            y = (point_2d[1] * scale * 2) + surf.get_height() // 4 
            z = (point_2d[2])
            points[i] = (x,y,z)
            i +=1
        
        return points
    
    def render(self, surf, scale, angle_x, angle_y, angle_z):
        points = self.update(surf, scale, angle_x, angle_y, angle_z)
        for faces in self.connections:
            coords = []
            if len(faces['points']) > 2:
                for point in faces['points']:
                    coords.append(points[point][0:2])
                    
                pygame.draw.polygon(surf, faces['color'], coords)
    
class Cube:
    
    def __init__(self):
        self.ROTATE_SPEED = 0.02
        self.scale = 30
        self.projection = Projection()
        

        self.cube_points = [n for n in range(8)]
        self.cube_points[0] = [[-1], [-1], [1]]
        self.cube_points[1] = [[1],[-1],[1]]
        self.cube_points[2] = [[1],[1],[1]]
        self.cube_points[3] = [[-1],[1],[1]]
        self.cube_points[4] = [[-1],[-1],[-1]]
        self.cube_points[5] = [[1],[-1],[-1]]
        self.cube_points[6] = [[1],[1],[-1]]
        self.cube_points[7] = [[-1],[1],[-1]]

    def connect_points(self, surf, i, j, points) -> None:
        pygame.draw.line(surf, (255, 255, 255), (points[i][0], points[i][1]) , (points[j][0], points[j][1]))

    
    # Main Loop
    

    def render(self, surf, angle_x=0, angle_y=0, angle_z=0):    
        points = [0 for _ in range(len(self.cube_points))]
        i = 0
        
        
        rotation_x = self.projection.get_rotation_x(angle_x)
        rotation_y = self.projection.get_rotation_y(angle_y)
        rotation_z = self.projection.get_rotation_z(angle_z)
        
        for point in self.cube_points:
            rotate_x = self.projection.multiply_m(rotation_x, point)
            rotate_y = self.projection.multiply_m(rotation_y, rotate_x)
            rotate_z = self.projection.multiply_m(rotation_z, rotate_y)
            point_2d = self.projection.multiply_m(self.projection.projection_matrix, rotate_z)
            
            x = (point_2d[0][0] * self.scale) + 60
            y = (point_2d[1][0] * self.scale) + 60

            points[i] = (x,y)
           #
            i += 1
            # pygame.draw.circle(surf, (255, 0, 0), (x, y), 5)

        self.connect_points(surf, 0, 1, points)
        self.connect_points(surf, 0, 3, points)
        self.connect_points(surf, 0, 4, points)
        
        self.connect_points(surf, 1, 2, points)
        self.connect_points(surf, 1, 5, points)
        
        self.connect_points(surf, 2, 6, points)
        self.connect_points(surf, 2, 3, points)
        
        self.connect_points(surf, 3, 7, points)
        
        self.connect_points(surf, 4, 5, points)
        self.connect_points(surf, 4, 7, points)
        
        self.connect_points(surf,6, 5, points)
        self.connect_points(surf,6, 7, points)