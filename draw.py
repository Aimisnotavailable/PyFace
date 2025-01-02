import pygame
import json
import sys
from engine import Engine

class Draw(Engine):

    def __init__(self, dim=(600, 400), font_size=20):
        super().__init__(dim, font_size)

        pygame.mouse.set_visible(False)
        self.points2d = []
        self.points3d = []
        self.fill = False
        self.grid_size = 3

        self.delete = False
        self.insert = False
    def check_collision(self, rect : pygame.Rect, rect1: pygame.Rect) -> bool:
        return rect.colliderect(rect1)

    def run(self):
        
        while True:
            self.display.fill((0, 0, 0))

            mpos = (((pygame.mouse.get_pos()[0]//2) // self.grid_size) * self.grid_size,((pygame.mouse.get_pos()[1]//2) //self.grid_size) * self.grid_size)
            m_rect = pygame.Rect(*mpos, 3, 3)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.insert = True
                    if event.button == 3:
                        self.delete =True
                
                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        self.insert = False
                    if event.button == 3:
                        self.delete = False
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_f:
                        self.fill = not self.fill
                    if event.key == pygame.K_r:
                        self.points = []
                    if event.key == pygame.K_p:
                        fp = open('points.json', 'w+')
                        json.dump(self.points3d,fp)

            if self.insert:
                coll = False
                for point in self.points2d:
                    p_rect = pygame.Rect(*point, 3, 3)
                    if self.check_collision(m_rect, p_rect):
                        coll = True
                
                if not coll:
                    self.points3d.append([*mpos, 1])
                    self.points2d.append(mpos)
            
            if self.delete:
                coll = False
                for point in self.points2d:
                    p_rect = pygame.Rect(*point, 3, 3)
                    if self.check_collision(m_rect, p_rect):
                        coll = True
                
                if coll:
                    self.points3d.remove([*mpos, 1])
                    self.points2d.remove(mpos)
                     
            if not self.fill or len(self.points2d) < 3:
                for point in self.points2d:
                    p_rect = pygame.Rect(*point, 3, 3)
                    pygame.draw.rect(self.display, (255, 255, 0), p_rect)
            else:
                pygame.draw.polygon(self.display, (0, 0, 255), self.points2d)
            
            pygame.draw.rect(self.display, (255, 255, 255), m_rect)
                
            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))
            self.clock.tick(60)
            pygame.display.update()

Draw().run()