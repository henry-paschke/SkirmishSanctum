import os
from button import Toggle_button
from card import Card, Preview_card
import pygame as pg

PREVIEW_WIDTH = 747 / 2
PREVIEW_HEIGHT = 1050 / 2

                
class Folder:
    def __init__(self, folder_path, camera, cards, position):
        self.folder_path = folder_path
        self.camera = camera
        self.cards = [Preview_card(f, f.replace("front", "back"), [position[0], position[1]], (PREVIEW_WIDTH, PREVIEW_HEIGHT * 0.1)) for f in cards]
        self.button = Toggle_button('assets/folder.png', pg.Rect(position, (PREVIEW_WIDTH, PREVIEW_HEIGHT * 0.1)))
        self.height = (len(cards)+1) * (PREVIEW_HEIGHT * .1) 

    def draw(self, screen):
        self.button.draw(screen)
        if self.button.toggled:
            for card in self.cards:
                card.draw(screen, self.camera)

    def get_height(self):
        return self.height
        