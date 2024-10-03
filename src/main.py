import pygame as pg
pg.init()


from camera import Camera
from input import *
import pickle
from vector import Vector2
from filesystem import create_menu_from_filesystem
from sidebar import Sidebar

WIDTH = 1920
HEIGHT = 1080
SCREEN_SIZE = Vector2(WIDTH, HEIGHT)
PREVIEW_SIZE = Vector2(747 - 100, 1050 / 10)

display_info = pg.display.Info()
window = pg.display.set_mode((display_info.current_w / 2, display_info.current_h / 2), pg.RESIZABLE)
pg.display.set_caption("Skirmish Sanctum")
pg.display.set_icon(pg.image.load("assets/logo.jpg"))
screen = pg.Surface((WIDTH, HEIGHT))

screen.blit(pg.image.load("assets/loading.jpg"), (0, 0))
window.blit(pg.transform.scale(screen, window.get_size()), (0, 0))
pg.display.update()


cards = []


camera = Camera(Vector2(0, 0), 1, SCREEN_SIZE)
sidebar = Sidebar(SCREEN_SIZE, PREVIEW_SIZE, (25, 35, 20))

CAMERA_SPEED = 20
CAMERA_ZOOM_SPEED = 0.03


MODES = ["drag", "draw", "erase"]
mode_index = 0


clock = pg.time.Clock()

while True:
    clock.tick()
    #print(clock.get_fps())
    screen.fill((46, 47, 47))

    mouse_pos = get_mouse_pos()

    click = None

    touchpad_scroll_buffer = False
    touchpad_click_buffer = False

    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            exit()
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                pg.quit()
                exit()
            if event.key == pg.K_TAB:
                mode_index += 1
                if mode_index >= len(MODES):
                    mode_index = 0
            if event.key == pg.K_LEFT: 
                sidebar.collapse()
            if event.key == pg.K_RIGHT:
                sidebar.expand()

            if event.key == pg.K_SPACE:
                pickle.dump(cards, open("cards.army", "wb"))
            
            if event.key == pg.K_l:
                cards = pickle.load(open("cards.army", "rb"))

            # if event.key == pg.K_DELETE:
            #     for card in cards.copy():
            #         if card.delete_check(mouse_pos, camera):
            #             cards.remove(card)

        if event.type == pg.MOUSEWHEEL:
            touchpad_scroll_buffer = -event.y

        if event.type == pg.MOUSEBUTTONDOWN:
            touchpad_click_buffer = True
            
        # if event.type == pg.MOUSEBUTTONUP:
        #     for card in cards:
        #         card.unclick(event.button)

    if touchpad_scroll_buffer:
        sidebar.scroll(touchpad_scroll_buffer)
    elif touchpad_click_buffer:
        click = get_normalized_mouse_pos(Vector2.from_tuple(window.get_size()))
        

    camera.move(get_wasd_as_vector() * CAMERA_SPEED)
    camera.change_zoom(get_axis(pg.K_e, pg.K_q) * CAMERA_ZOOM_SPEED)
    sidebar.scroll(get_axis(pg.K_DOWN, pg.K_UP))

    sidebar.update(click)
    sidebar.draw(screen)

    window.blit(pg.transform.scale(screen, window.get_size()), (0, 0))

    pg.display.update()