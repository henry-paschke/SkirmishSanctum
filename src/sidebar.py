from filesystem import create_menu_from_filesystem
from drawable import Drawable
from camera import Camera
from vector import Vector2

class Sidebar (Drawable):
    SIDEBAR_SPEED = 15

    def __init__(self, SCREEN_SIZE: Vector2, PREVIEW_SIZE: Vector2, color: tuple) -> None:
        self.sidebar_camera = Camera(Vector2(0, 0), 1, SCREEN_SIZE)
        self.sidebar_transition = 0.0
        self.sidebar_dir = 0.0
        self.PREVIEW_SIZE = PREVIEW_SIZE
        self.SCREEN_SIZE = SCREEN_SIZE
        self.cards = create_menu_from_filesystem("smaller_images", self.sidebar_camera, PREVIEW_SIZE, (255, 238, 156), starting_pos=(-SCREEN_SIZE/2 + PREVIEW_SIZE / 2))
        super().__init__(Vector2(PREVIEW_SIZE.x, SCREEN_SIZE.y), color, Camera(Vector2(0,0), 1, SCREEN_SIZE), position=Vector2(-SCREEN_SIZE.x/2 + PREVIEW_SIZE.x/2, 0))

    def update(self, click = None) -> any:
        super().update(click)

        self.sidebar_transition += self.sidebar_dir
        if self.sidebar_transition < 0:
            self.sidebar_transition = 0
            self.sidebar_dir = 0
        if self.sidebar_transition > 1.0:
            self.sidebar_transition = 1.0
            self.sidebar_dir = 0

        self.sidebar_camera.center_pos.x = self.sidebar_transition * self.PREVIEW_SIZE.x
        self.camera.center_pos.x = self.sidebar_transition * self.PREVIEW_SIZE.x 
        
        result = None
        for card in self.cards:
            r = card.update(click)
            if r:
                result = r
        if result != None:
            return result

    def draw(self, screen):
        super().draw(screen)
        for card in self.cards:
            card.draw(screen)

    def scroll(self, amount: int) -> None:
        self.sidebar_camera.move(Vector2(0, Sidebar.SIDEBAR_SPEED * amount))
        if self.sidebar_camera.center_pos.y < 0:
            self.sidebar_camera.center_pos.y = 0

    def collapse(self) -> None:
        if self.sidebar_transition == 0.0:
            self.sidebar_dir = 0.1

    def expand(self) -> None:
        if self.sidebar_transition == 1.0:
            self.sidebar_dir = -0.1