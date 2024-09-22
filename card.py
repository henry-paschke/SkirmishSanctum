import pygame as pg
from camera import Camera
import pickle

CIRCLE_RADIUS = 5

class Card:
    def __init__(self, front_path, back_path, pos, size):
        self.front_img = pg.image.load(front_path).convert_alpha()
        self.back_img = pg.image.load(back_path).convert_alpha()

        self.front_path = front_path
        self.back_path = back_path

        self.flipped = False

        self.position = pos
        self.size = size
        self.transition_percentage = 0.0

        self.anchored_mouse_pos = None

        self.drawing = False
        self.erasing = False

        self.circles = []

    def __getstate__(self) -> object:
        state = self.__dict__.copy()
        del state["front_img"]
        del state["back_img"]
        return state
    
    def __setstate__(self, state):
        self.__dict__.update(state)
        self.front_img = pg.image.load(self.front_path).convert_alpha()
        self.back_img = pg.image.load(self.back_path).convert_alpha()
    
    def draw(self, screen, camera):
        pos = camera.camera_to_screen(self.position)
        max_pos = [pos[0] + self.size[0] // 2 * camera.zoom, pos[1] + self.size[1] // 2 * camera.zoom]
        min_pos = [pos[0] - self.size[0] // 2 * camera.zoom, pos[1] - self.size[1] // 2 * camera.zoom]
        if max_pos[0] < 0 or max_pos[1] < 0 or min_pos[0] > camera.size[0] or min_pos[1] > camera.size[1]:
            return

        if self.transition_percentage == 0:
            img = self.front_img if not self.flipped else self.back_img
            img = pg.transform.scale(img, [self.size[0] * camera.zoom, self.size[1] * camera.zoom])
        else:
            flipped = self.flipped if self.transition_percentage < 0.5 else not self.flipped
            img = self.front_img if not flipped else self.back_img
            img = pg.transform.scale(img, [self.size[0] * camera.zoom * 2.0 * abs(0.5 - self.transition_percentage), self.size[1] * camera.zoom])
            self.transition_percentage -= 0.0555
            if self.transition_percentage < 0:
                self.transition_percentage = 0

        
        pos = (pos[0] - img.get_width() // 2, pos[1] - img.get_height() // 2)
        screen.blit(img, pos)

        if self.transition_percentage == 0 and not self.flipped:
            for i in range(1, len(self.circles)):
                if self.circles[i] != None and self.circles[i - 1] != None:
                    pg.draw.line(screen, (0, 0, 0), [int(pos[0] + self.circles[i - 1][0] * camera.zoom), int(pos[1] + self.circles[i - 1][1] * camera.zoom)], [int(pos[0] + self.circles[i][0] * camera.zoom), int(pos[1] + self.circles[i][1] * camera.zoom)], int(CIRCLE_RADIUS * 2 * camera.zoom))
                    pg.draw.circle(screen, (0, 0, 0), [int(pos[0] + self.circles[i][0] * camera.zoom), int(pos[1] + self.circles[i][1] * camera.zoom)], int((CIRCLE_RADIUS * 0.8) * camera.zoom))

    def update(self, camera, m_p):
        if self.anchored_mouse_pos:
            mouse_pos = camera.screen_to_camera(m_p)
            self.position = [mouse_pos[0] - self.anchored_mouse_pos[0], mouse_pos[1] - self.anchored_mouse_pos[1]]
        if self.drawing:
            mouse_pos = camera.screen_to_camera(m_p)
            new_pos = [int(mouse_pos[0] - self.position[0] + self.size[0] / 2), int(mouse_pos[1] - self.position[1] + self.size[1] / 2)]
            if self.circles == [] or self.circles[-1] == None:
                self.circles.append(new_pos)
            else:
                distance = (new_pos[0] - self.circles[-1][0]) ** 2 + (new_pos[1] - self.circles[-1][1]) ** 2
                if distance > CIRCLE_RADIUS ** 2:
                    self.circles.append(new_pos)

        if self.erasing:
            mouse_pos = camera.screen_to_camera(m_p)
            for i in range(len(self.circles)):
                circle = self.circles[i]
                if circle != None and (mouse_pos[0] - (self.position[0] + circle[0] - self.size[0] // 2)) ** 2 + (mouse_pos[1] - (self.position[1] + circle[1]  - self.size[1] // 2)) ** 2 < CIRCLE_RADIUS ** 2:
                    self.circles[i] = None

    def delete_check(self, pos, camera):
        if not self.check_is_colliding(pos, camera):
            return False
        return True

    def click(self, pos, camera, button, mode_index):
        if not self.check_is_colliding(pos, camera):
            return
        if button == 3:
            self.flip()
        if button == 1:
            if mode_index == 0:
                mouse_pos = camera.screen_to_camera(pos)
                self.anchored_mouse_pos = [mouse_pos[0] - self.position[0], mouse_pos[1] - self.position[1]]
            if mode_index == 1:
                self.drawing = True
            if mode_index == 2:
                self.erasing = True

    def unclick(self, button):
        if button == 1:
            self.anchored_mouse_pos = None
        if self.drawing:
            self.circles.append(None)
            self.drawing = False

        self.erasing = False

    def check_is_colliding(self, pos, camera):
        pos = camera.screen_to_camera(pos)
        left = self.position[0] - self.size[0] // 2
        right = self.position[0] + self.size[0] // 2
        top = self.position[1] - self.size[1] // 2
        bottom = self.position[1] + self.size[1] // 2

        if left < pos[0] < right and top < pos[1] < bottom:
            return True
        return False

    def flip(self):
        self.flipped = not self.flipped
        self.transition_percentage = 1.0


class Preview_card:
    def __init__(self, front_path, back_path, pos, size):
        self.front_img = pg.image.load(front_path).convert_alpha()
        self.front_path = front_path
        self.back_path = back_path
        self.flipped = False

        self.position = pos
        self.size = size

    def draw(self, screen, camera):
        pos = camera.camera_to_screen(self.position)
        img = pg.transform.scale(self.front_img, [self.size[0] * camera.zoom, self.size[1] * camera.zoom])
        pos = (pos[0] - img.get_width() // 2, pos[1] - img.get_height() // 2)
        screen.blit(img, pos, (0, 0, self.size[0], self.size[1] / 10))
        
    def click(self, pos, camera, button, mode_index):
        if not self.check_is_colliding(pos, camera):
            return
        if button == 1:
            new_card = Card(self.front_path, self.back_path, [0,0], self.size)
            mouse_pos = camera.screen_to_camera(pos)
            new_card.anchored_mouse_pos = [mouse_pos[0] - self.position[0], mouse_pos[1] - self.position[1]]
            return new_card
        return None
    
    def check_is_colliding(self, pos, camera):
        pos = camera.screen_to_camera(pos)
        left = self.position[0] - self.size[0] // 2
        right = self.position[0] + self.size[0] // 2
        top = self.position[1] - self.size[1] // 2
        bottom = top + self.size[1] / 10

        if left < pos[0] < right and top < pos[1] < bottom:
            return True
        return False
    