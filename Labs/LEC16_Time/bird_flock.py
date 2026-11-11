"""bird_animation.png의 비행 프레임으로 새 열 마리를 그린다."""
from pico2d import load_image

import game_framework


FRAME_COLUMNS = 5
FRAME_ROWS = 3
FRAME_COUNT = 14
ANIMATION_FPS = 14.0
FLOCK_SPEED = 120.0
BIRD_WIDTH = 64
BIRD_HEIGHT = 56
MARGIN = 36


class BirdFlock:
    def __init__(self):
        self.image = load_image('bird_animation.png')
        self.direction = 1
        self.x = 800.0
        self.y = 420.0
        self.animation_time = 0.0
        self.offsets = [
            (0, 0),
            (-55, -34), (-55, 34),
            (-110, -68), (-110, 68),
            (-165, -102), (-165, 102),
            (-220, -136), (-220, 136),
            (-275, 0),
        ]
        self.phases = [
            index * FRAME_COUNT / len(self.offsets)
            for index in range(len(self.offsets))
        ]
        self.min_x = (
            MARGIN + max(abs(dx) for dx, _ in self.offsets) + BIRD_WIDTH / 2
        )
        self.max_x = 1600 - self.min_x

    def update(self):
        delta_time = game_framework.frame_time
        self.animation_time = (
            self.animation_time + delta_time
        ) % (FRAME_COUNT / ANIMATION_FPS)

        span = self.max_x - self.min_x
        travel = self.x - self.min_x
        if self.direction < 0:
            travel = 2 * span - travel
        travel = (travel + FLOCK_SPEED * delta_time) % (2 * span)
        if travel < span:
            self.x = self.min_x + travel
            self.direction = 1
        else:
            self.x = self.max_x - (travel - span)
            self.direction = -1

    def draw(self):
        sheet_width, sheet_height = self.image.w, self.image.h
        for (offset_x, offset_y), phase in zip(self.offsets, self.phases):
            frame = int(self.animation_time * ANIMATION_FPS + phase) % FRAME_COUNT
            row, column = divmod(frame, FRAME_COLUMNS)
            left = column * sheet_width // FRAME_COLUMNS
            right = (column + 1) * sheet_width // FRAME_COLUMNS
            top = row * sheet_height // FRAME_ROWS
            bottom_edge = (row + 1) * sheet_height // FRAME_ROWS
            bottom = sheet_height - bottom_edge
            flip = 'h' if self.direction < 0 else ''
            self.image.clip_composite_draw(
                left, bottom, right - left, bottom_edge - top,
                0, flip,
                self.x + offset_x * self.direction, self.y + offset_y,
                BIRD_WIDTH, BIRD_HEIGHT,
            )
