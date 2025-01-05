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

class TextBox:

    def __init__(self,font : pygame.Font = None, size=(20, 10), pos=(0, 0)):
        self.font = font
        self.size = size
        self.pos = pos
        self.temp = ''
    
    def write(self, text='', char=''):
        return text + char

    def delete(self, text=''):
        return text[0 : -2]

    def render(self,surf=None, text='',  text_color=(255, 255, 255)):
        surf.blit(self.font.render(text, True, text_color), self.pos)


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
        self.point_groups = []

        self.menu_buttons : list[Button] = []
        self.text_box = TextBox(font=self.font, pos=(0, self.display.get_height() - 12))

        self.saves()
        self.fill = False
        self.grid_size = 3

        self.current_text = ''
        self.current_group_name = ''
        self.writing = False
        self.delete = False
        self.insert = False
        self.start = False if len(self.menu_buttons) > 1 else True
        self.new_group = False
        self.save_file = False

        self.current_group = 0

    def load_main(self, dir):
        fp = open(BASE_PATH + dir, 'r+')
        data = json.load(fp)
        if data:
            self.point_groups = data

    def main_screen(self, mpos, m_rect):
        if self.point_groups:
            self.current_group_name = ''.join(list(self.point_groups[self.current_group]))

        self.text_box.render(self.display, self.current_text if self.writing else self.current_group_name)
        self.display.blit(self.font.render(f'Current Group: {self.current_group}', True, (255, 255 ,255)), (0, 0))

        if self.insert and mpos[1] >= 12 and mpos[1] <= self.display.get_height() - 12:
                coll = False
                for point in self.point_groups[self.current_group][self.current_group_name]['2d']:
                    p_rect = pygame.Rect(*point, 3, 3)
                    if self.check_collision(m_rect, p_rect):
                        coll = True
                
                if not coll:
                    self.point_groups[self.current_group][self.current_group_name]['3d'].append([*mpos, 1])
                    self.point_groups[self.current_group][self.current_group_name]['2d'].append(list(mpos).copy())
            
        if self.delete:
            coll = False
            for point in self.point_groups[self.current_group][self.current_group_name]['2d']:
                p_rect = pygame.Rect(*point, 3, 3)
                if self.check_collision(m_rect, p_rect):
                    coll = True
            
            if coll:
                self.point_groups[self.current_group][self.current_group_name]['3d'].remove([*mpos, 1])
                self.point_groups[self.current_group][self.current_group_name]['2d'].remove(list(mpos))

        for group_name in self.point_groups:            
            for key, group in group_name.items():
                if not self.fill or len(group['2d']) < 3:
                    for point in group['2d']:
                        p_rect = pygame.Rect(*point, 3, 3)
                        pygame.draw.rect(self.display, group['color'], p_rect)
                else:
                    pygame.draw.polygon(self.display, group['color'], group['2d'])
    
    def run(self):
        curr_group_color = None
        while True:
            self.display.fill((60, 60, 60))

            mpos = (((pygame.mouse.get_pos()[0]//2) // self.grid_size) * self.grid_size,((pygame.mouse.get_pos()[1]//2) //self.grid_size) * self.grid_size)
            m_rect = pygame.Rect(*mpos, 3, 3)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if not self.writing:
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
                        if not self.writing:
                            if event.key == pygame.K_f:
                                self.fill = not self.fill
                            if event.key == pygame.K_r:
                                self.points2d = []
                                self.points3d = []

                            if event.key == pygame.K_p:
                                self.writing = True
                                self.save_file = True
                                self.current_text = ''

                            if event.key == pygame.K_g:
                                self.current_text = ''
                                self.writing = True
                                self.new_group = True

                            if event.key == pygame.K_ESCAPE:
                                self.load_menu()
                        else:
                            
                            if event.key >= 97 and event.key <= 122:
                                self.current_text = self.current_text + chr(event.key)

                            if event.key == pygame.K_BACKSPACE:
                                self.current_text = self.current_text[0 : -2]

                            if event.key == pygame.K_RETURN:
                                if self.new_group:
                                    self.point_groups.append({self.current_text : {'2d' : [], '3d' : [], 'color' : (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))}})
                                    self.current_group = len(self.point_groups) - 1
                                if self.save_file:
                                    with open(f'shapes/{self.current_text}.json', 'w+') as fp:
                                        json.dump(self.point_groups,fp)

                                self.writing = False
                                self.new_group = False
                                self.save_file = False
                
            if not self.start:
                for button in self.menu_buttons:
                    coll = button.rect().colliderect(m_rect)
                    fill_color = (0, 255, 0) if coll else (255, 0, 0)

                    button.render(self.display, coll, fill_color)
            else:
                self.main_screen(mpos, m_rect)
                if self.point_groups:
                    curr_group_color = self.point_groups[self.current_group][self.current_group_name]['color']
                else:
                    self.writing = True
                    self.new_group = True


            pygame.draw.rect(self.display, curr_group_color if curr_group_color else (255, 255, 255), m_rect)
                
            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))
            self.clock.tick(60)
            pygame.display.update()

Draw().run()