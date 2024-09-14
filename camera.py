WIDTH, HEIGHT = 1920, 1080

class Camera:
    def __init__(self, pos, zoom):
        self.center_pos = pos
        self.zoom = zoom
        self.size = [WIDTH, HEIGHT]

    def move(self, direction):
        self.center_pos[0] += direction[0]
        self.center_pos[1] += direction[1]

    def change_zoom(self, zoom):
        self.zoom += zoom * self.zoom * self.zoom
        if self.zoom < 0.1:
            self.zoom = 0.1
        if self.zoom > 2:
            self.zoom = 2

    def camera_to_screen(self, camera_pos):
        return [(camera_pos[0] - self.center_pos[0]) * self.zoom + WIDTH // 2,
                (camera_pos[1] - self.center_pos[1]) * self.zoom + HEIGHT // 2]
    
    def screen_to_camera(self, screen_pos):
        return [(screen_pos[0] - WIDTH // 2) / self.zoom + self.center_pos[0],
                (screen_pos[1] - HEIGHT // 2) / self.zoom + self.center_pos[1]]
    
