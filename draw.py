import pygame
import json
import sys
import os
import random 
from engine import Engine

BASE_PATH = 'shapes/'

class Button:

    def __init__(self, text='', img_surf=None, size=(20, 10), pos=(0, 0)):
        self.text = text
        self.img_surf = img_surf
        self.size = size
        self.pos = pos
    
    def rect(self) -> pygame.Rect:
        return pygame.Rect(*self.pos, *self.size)
    
    def draw_comp(self, surf=None, fill=False, fill_color=(0, 0, 0), border=True, border_color=(255, 255, 255)):
        rect = self.rect()

        if fill:
            pygame.draw.rect(surf, fill_color, rect)
        if border:
            pygame.draw.rect(surf, border_color, rect, 2)

    def render(self, surf=None, fill=False, fill_color=(0, 0, 0), border=True, border_color=(255, 255, 255)):
        self.draw_comp(surf, fill, fill_color, border, border_color)
        surf.blit(self.img_surf, (self.pos[0] + 5, self.pos[1] + 5))

class Draw(Engine):

    def __init__(self, dim=(600, 400), font_size=20):
        super().__init__(dim, font_size)

        pygame.mouse.set_visible(False)
        self.load_menu()

    def check_collision(self, rect : pygame.Rect, rect1: pygame.Rect) -> bool:
        return rect.colliderect(rect1)

    def saves(self):
        start_pos = [0, 0]
        interv = 20
        idx = 0
        for idx, file in enumerate(os.listdir('shapes/')):
            self.menu_buttons.append(Button(file, self.font.render(file, True, (255, 255, 255)), (100, 20), (start_pos[0], start_pos[1] + idx * interv)))
        self.menu_buttons.append(Button('New', self.font.render('New', True, (255, 255, 255)), (100, 20), (start_pos[0], start_pos[1] + (idx + 1) * interv)))

    def load_menu(self):
        self.point_groups = [{'2d' : [], '3d' : [], 'color' : (255, 255 ,255)}]

        self.menu_buttons : list[Button] = []

        self.saves()
        self.fill = False
        self.grid_size = 3

        self.delete = False
        self.insert = False
        self.start = False if len(self.menu_buttons) > 1 else True

        self.current_group = 0

    def load_main(self, dir):
        fp = open(BASE_PATH + dir, 'r+')
        data = json.load(fp)
        if data:
            self.point_groups = data

    def main_screen(self, mpos, m_rect):
        self.display.blit(self.font.render(f'Current Group: {self.current_group}', True, (255, 255 ,255)), (0, 0))
        if self.insert and mpos[1] >= 12:
                coll = False
                for point in self.point_groups[self.current_group]['2d']:
                    p_rect = pygame.Rect(*point, 3, 3)
                    if self.check_collision(m_rect, p_rect):
                        coll = True
                
                if not coll:
                    self.point_groups[self.current_group]['3d'].append([*mpos, 1])
                    self.point_groups[self.current_group]['2d'].append(mpos)
            
        if self.delete:
            coll = False
            for point in self.point_groups[self.current_group]['2d']:
                p_rect = pygame.Rect(*point, 3, 3)
                if self.check_collision(m_rect, p_rect):
                    coll = True
            
            if coll:
                self.point_groups[self.current_group]['3d'].remove([*mpos, 1])
                self.point_groups[self.current_group]['2d'].remove(mpos)

        for group in self.point_groups:            
            if not self.fill or len(group['2d']) < 3:
                for point in group['2d']:
                    p_rect = pygame.Rect(*point, 3, 3)
                    pygame.draw.rect(self.display, group['color'], p_rect)
            else:
                pygame.draw.polygon(self.display, group['color'], group['2d'])
    
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
                        if self.start:
                            self.insert = True
                        else:
                            for button in self.menu_buttons:
                                if m_rect.colliderect(button.rect()):
                                    if button.text != 'New':
                                        self.load_main(button.text)
                                    self.start = True
                                    break
                                
                    if event.button == 3:
                        if self.start:
                            self.delete =True
                            
                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        if self.start:
                            self.insert = False
                    if event.button == 3:
                        if self.start:
                            self.delete = False
                    
                    if event.button == 4:
                        self.current_group = min(self.current_group + 1, len(self.point_groups) - 1)
                    if event.button == 5:
                        self.current_group = max(self.current_group - 1, 0)
                
                if self.start:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_f:
                            self.fill = not self.fill
                        if event.key == pygame.K_r:
                            self.points2d = []
                            self.points3d = []

                        if event.key == pygame.K_p:
                            file_name = input('File name: ')
                            with open(f'shapes/{file_name}.json', 'w+') as fp:
                                json.dump(self.point_groups,fp)

                        if event.key == pygame.K_g:
                            self.point_groups.append({'2d' : [], '3d' : [], 'color' : (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))})
                        
                        if event.key == pygame.K_ESCAPE:
                            self.load_menu()
            
            if not self.start:
                for button in self.menu_buttons:
                    coll = button.rect().colliderect(m_rect)
                    fill_color = (0, 255, 0) if coll else (255, 0, 0)

                    button.render(self.display, coll, fill_color)
            else:
                self.main_screen(mpos, m_rect)

            pygame.draw.rect(self.display, (255, 255, 255), m_rect)
                
            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))
            self.clock.tick(60)
            pygame.display.update()

Draw().run()