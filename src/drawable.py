from vector import Vector2
import pygame as pg

class Drawable:
    def __init__(self, size: Vector2, resource, camera, attachments = [], crop = None, position: Vector2 = Vector2(0,0)):
        self.position = position
        self.size = size
        self.resource = resource
        if isinstance(self.resource, str):
            try:
                self.resource = pg.image.load(self.resource).convert_alpha()
            except:
                self.resource = (255, 0, 0)
        self.camera = camera
        self.attachments = attachments
        for attachment in self.attachments:
            attachment.parent = self
        self.crop = pg.Rect((0, 0), self.size.get_tuple()) if crop == None else crop

    def draw(self, screen):
        pos = self.camera.camera_to_screen(self.position)
        size = self.size * self.camera.zoom
        screenrect = pg.Rect((0,0), self.camera.internal_resolution.get_tuple())

        bounding_box = pg.Rect((pos - size / 2).get_tuple(), size.get_tuple())

        if bounding_box.colliderect(screenrect):
            if isinstance(self.resource, tuple):
                pg.draw.rect(screen, self.resource, bounding_box)
            else:
                screen.blit(self.resource, (pos - size / 2).get_tuple(), pg.Rect((0, 0), self.size.get_tuple()))

        for attachment in self.attachments:
            attachment.draw(screen)

    def update(self, click = None):
        for attachment in self.attachments:
            attachment.update(click)

    def check_is_colliding(self, point):
        point = self.camera.screen_to_camera(point)
        left = self.position.x - self.size.x // 2
        right = self.position.x + self.size.x // 2
        top = self.position.y - self.size.y // 2
        bottom = self.position.y + self.size.y // 2

        if left < point.x < right and top < point.y < bottom:
            return True
        return False
    
    def get_height(self):
        return self.size.y + self.get_attachment_height()
    
    def get_attachment_height(self):
        return sum(attachment.get_height() for attachment in self.attachments)
    
    def get_bottom(self):
        return Vector2(self.position.x, self.position.y + self.get_attachment_height() + (self.size.y / 2))
    
    def get_bottom_no_children(self):
        return Vector2(self.position.x, self.position.y + (self.size.y / 2))


class Attachment:
    def __init__(self, offset: Vector2):
        self.offset = offset
        self.parent = None
        
    def draw(self, screen, parent_pos):
        pass

    def update(self, click = None):
        pass

    def get_height(self):
        return 0

class Text_attachment (Attachment):
    def __init__(self, text: str, font_size: int = 36, offset: Vector2 = Vector2(0,0), font_color: tuple[int] = (255, 255, 255)):
        super().__init__(offset)
        self.text = text
        self.font_size = font_size
        self.font_color = font_color

    def draw(self, screen):
        font = pg.font.Font(None, self.font_size)
        text = font.render(self.text, True, self.font_color)
        text_size = Vector2.from_tuple(text.get_size())
        screen.blit(text, self.parent.camera.camera_to_screen((self.parent.position +  self.offset - text_size / 2)).get_tuple())

class Toggle_attachment(Attachment):
    def __init__(self, offset: Vector2, toggle_function = lambda: None, toggle_default = False):
        super().__init__(offset)
        self.toggled = toggle_default
        self.toggle_function = toggle_function

    def draw(self, screen):
        pass

    def update(self, click = None):
        if click != None:
            click = self.parent.camera.screen_to_camera(click)
            if self.parent.check_is_colliding(click):
                self.toggle_function()
                self.toggled = not self.toggled


class Folder_attachment(Attachment):
    def __init__(self, folder_contents: list[Drawable], indent: int):
        super().__init__(Vector2(0, 0))
        self.folder_contents = folder_contents
        self.opened = False
        self.indent = indent

    def draw(self, screen):
        if not self.opened:
            return
        for i, content in enumerate(self.folder_contents):
            if i == 0:
                previous = self.parent.get_bottom_no_children() + Vector2(self.indent/2, 0)
            else:
                previous = self.folder_contents[i-1].get_bottom()
            content.position = previous + Vector2(0, content.size.y/2)
            content.draw(screen)

    def update(self, click = None):
        if self.opened:
            for content in self.folder_contents:
                content.update(click)

        if click != None:
            if self.parent.check_is_colliding(click):
                self.opened = not self.opened

    def get_height(self):
        return sum(content.get_height() for content in self.folder_contents) if self.opened else 0
    


class Double_sided_drawable(Drawable):
    def __init__(self, size: Vector2, resource_front, resource_back, camera, attachments=[], position: Vector2 = Vector2(0,0)):
        super().__init__( size, resource_front, camera, attachments, position=position)
        self.resources = [resource_front, resource_back]
        self.flipped = False

    def flip(self):
        self.flipped = not self.flipped
        self.resource = self.resources[int(self.flipped)]

class Click_function(Attachment):
    def __init__(self, function):
        super().__init__(Vector2(0, 0))
        self.function = function

    def update(self, click = None):
        if click != None:
            click = self.parent.camera.screen_to_camera(click)
            if self.parent.check_is_colliding(click):
                self.function()