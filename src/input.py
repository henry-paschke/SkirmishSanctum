import pygame as pg
from vector import Vector2
display_info = pg.display.Info()

def get_wasd_as_vector():
    keys = pg.key.get_pressed()
    return Vector2(keys[pg.K_d] - keys[pg.K_a], keys[pg.K_s] - keys[pg.K_w])

def get_axis(code_1, code_2):
    keys = pg.key.get_pressed()
    return keys[code_1] - keys[code_2]

def get_mouse_pos():
    return Vector2.from_tuple(pg.mouse.get_pos())

def get_normalized_mouse_pos(screen_size):
    return Vector2.from_tuple(pg.mouse.get_pos()) / screen_size