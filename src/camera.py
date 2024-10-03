from vector import Vector2
import pygame as pg

class Camera:
    def __init__(self, pos : Vector2, zoom: float, internal_resolution: Vector2):
        self.center_pos = pos
        self.zoom = zoom
        self.internal_resolution = internal_resolution

    def move(self, direction: Vector2):
        self.center_pos += direction / self.zoom

    def change_zoom(self, zoom):
        self.zoom += zoom * self.zoom * self.zoom
        if self.zoom < 0.1:
            self.zoom = 0.1
        if self.zoom > 2:
            self.zoom = 2

    def camera_to_screen(self, camera_pos):
        return ((camera_pos - self.center_pos) * self.zoom) + self.internal_resolution / 2
    
    def screen_to_camera(self, screen_pos):
        normalized_distance_from_center = (screen_pos - Vector2(0.5, 0.5)) 
        return self.center_pos + (normalized_distance_from_center * (self.internal_resolution / self.zoom))
    
    