import pygame as pg
from card import Card, Preview_card
from button import Button
from camera import Camera
from input import *
import pickle

WIDTH = 1920
HEIGHT = 1080

pg.init()
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("Skirmish Sanctum")


cards = []
preview_cards = []

PREVIEW_WIDTH = 747 / 2
PREVIEW_HEIGHT = 1050 / 2

for i in range(27):
    for j in range(4):
            #preview_cards.append(Preview_card(f'assets/circle/Circle_page_{i+1}_card_{j+1}_top.png', f'assets/circle/Circle_page_{i+1}_card_{j+1}_bottom.png', ((-WIDTH / 2) + int(PREVIEW_WIDTH / 2), (-HEIGHT / 2) + int(PREVIEW_HEIGHT / 2) + (i * 4 + j) * PREVIEW_HEIGHT / 10), (PREVIEW_WIDTH, PREVIEW_HEIGHT)))
            #preview_cards.append(Preview_card(f'assets/skorne/Skorne_page_{i+1}_card_{j+1}_top.png', f'assets/skorne/Skorne_page_{i+1}_card_{j+1}_bottom.png', ((-WIDTH / 2) + int(PREVIEW_WIDTH / 2), (-HEIGHT / 2) + int(PREVIEW_HEIGHT / 2) + (i * 4 + j) * PREVIEW_HEIGHT / 10), (PREVIEW_WIDTH, PREVIEW_HEIGHT)))
            preview_cards.append(Preview_card(f'assets/trollbloods/Trollbloods_page_{i+1}_card_{j+1}_top.png', f'assets/trollbloods/Trollbloods_page_{i+1}_card_{j+1}_bottom.png', ((-WIDTH / 2) + int(PREVIEW_WIDTH / 2), (-HEIGHT / 2) + int(PREVIEW_HEIGHT / 2) + (i * 4 + j) * PREVIEW_HEIGHT / 10), (PREVIEW_WIDTH, PREVIEW_HEIGHT)))


camera = Camera([0, 0], 1)
sidebar_camera = Camera([0, 0], 1)
sidebar_transition = 0.0
sidebar_dir = 0
CAMERA_SPEED = 20
CAMERA_ZOOM_SPEED = 0.03

MODES = ["drag", "draw", "erase"]
mode_index = 0


clock = pg.time.Clock()

while True:
    clock.tick(60)
    screen.fill((46, 47, 47))

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
            if event.key == pg.K_LEFT and sidebar_transition == 0.0: 
                sidebar_dir = 0.1
            if event.key == pg.K_RIGHT and sidebar_transition == 1.0:
                sidebar_dir = -0.1

            if event.key == pg.K_SPACE:
                pickle.dump(cards, open("cards.army", "wb"))
            
            if event.key == pg.K_l:
                cards = pickle.load(open("cards.army", "rb"))

        if event.type == pg.MOUSEBUTTONDOWN:
            for card in cards:
                card.click(event.pos, camera, event.button, mode_index)
            for card in preview_cards:
                result = card.click(event.pos, sidebar_camera, event.button, mode_index)
                if result != None:
                    cards.append(result)
        if event.type == pg.MOUSEBUTTONUP:
            for card in cards:
                card.unclick(event.button)


    wasd = get_wasd_as_point()
    camera.move([wasd[0] * CAMERA_SPEED / camera.zoom, wasd[1] * CAMERA_SPEED / camera.zoom])
    camera.change_zoom(get_axis(pg.K_e, pg.K_q) * CAMERA_ZOOM_SPEED)

    sidebar_camera.move([0, get_axis(pg.K_DOWN, pg.K_UP) * CAMERA_SPEED / camera.zoom])
    if sidebar_camera.center_pos[1] < 0:
        sidebar_camera.center_pos[1] = 0
    if sidebar_camera.center_pos[1] < -len(preview_cards) * PREVIEW_HEIGHT + HEIGHT:
        sidebar_camera.center_pos[1] = -len(preview_cards) * PREVIEW_HEIGHT + HEIGHT

    for card in cards:
        card.update(camera)
        card.draw(screen, camera)

    sidebar_transition += sidebar_dir
    if sidebar_transition < 0:
        sidebar_transition = 0
        sidebar_dir = 0
    if sidebar_transition > 1.0:
        sidebar_transition = 1.0
        sidebar_dir = 0

    sidebar_camera.center_pos[0] = sidebar_transition * PREVIEW_WIDTH
    
    pg.draw.rect(screen, (25, 35, 20), (0, 0, PREVIEW_WIDTH * (1.0 -  sidebar_transition) + 10, HEIGHT))
    
    # for card in preview_cards:
    #     card.draw(screen, sidebar_camera)

    range = int(HEIGHT / (PREVIEW_HEIGHT / 10))  + 1
    if sidebar_transition != 1.0:
        for card in preview_cards[int(sidebar_camera.center_pos[1] / (PREVIEW_HEIGHT / 10)) : int(sidebar_camera.center_pos[1] / (PREVIEW_HEIGHT / 10) + range)]:
            card.draw(screen, sidebar_camera)

    pg.display.update()