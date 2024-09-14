import pygame as pg


def get_wasd_as_point():
    keys = pg.key.get_pressed()
    return (keys[pg.K_d] - keys[pg.K_a], keys[pg.K_s] - keys[pg.K_w])

def get_axis(code_1, code_2):
    keys = pg.key.get_pressed()
    return keys[code_1] - keys[code_2]