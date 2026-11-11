"""bird_animation.png의 비행 프레임으로 새 열 마리를 그린다."""
from pico2d import load_image


FRAME_COLUMNS = 5
FRAME_ROWS = 3
FRAME_COUNT = 14
BIRD_WIDTH = 64
BIRD_HEIGHT = 56


class BirdFlock:
    def __init__(self):
        self.image = load_image('bird_animation.png')
        self.x = 800.0
        self.y = 420.0
        self.offsets = [
            (0, 0),
            (-55, -34), (-55, 34),
            (-110, -68), (-110, 68),
            (-165, -102), (-165, 102),
            (-220, -136), (-220, 136),
            (-275, 0),
        ]

    def update(self):
        pass

    def draw(self):
        sheet_width, sheet_height = self.image.w, self.image.h
        for index, (offset_x, offset_y) in enumerate(self.offsets):
            frame = index % FRAME_COUNT
            row, column = divmod(frame, FRAME_COLUMNS)
            left = column * sheet_width // FRAME_COLUMNS
            right = (column + 1) * sheet_width // FRAME_COLUMNS
            top = row * sheet_height // FRAME_ROWS
            bottom_edge = (row + 1) * sheet_height // FRAME_ROWS
            bottom = sheet_height - bottom_edge
            self.image.clip_draw(
                left, bottom, right - left, bottom_edge - top,
                self.x + offset_x, self.y + offset_y,
                BIRD_WIDTH, BIRD_HEIGHT,
            )
