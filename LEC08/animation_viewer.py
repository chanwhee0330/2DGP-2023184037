"""Drill #8 - 여러 동작을 차례로 보여 주는 스프라이트 애니메이션 뷰어."""

import os
from pathlib import Path

from pico2d import *


CANVAS_WIDTH = 800
CANVAS_HEIGHT = 600
CELL_SIZE = 128
DRAW_SCALE = 4.0
REPEAT_COUNT = 5
PAUSE_SECONDS = 1.0


# 각 튜플은 (left, bottom, width, height)이다.
# 투명한 여백을 제외한 영역을 프레임마다 따로 기록했기 때문에 프레임 크기가
# 서로 다른 복잡한 스프라이트 시트도 올바르게 재생할 수 있다.
ANIMATIONS = (
    {
        "name": "IDLE",
        "seconds_per_frame": 0.14,
        "frames": (
            (35, 1154, 46, 81),
            (163, 1154, 46, 82),
            (291, 1154, 46, 83),
            (419, 1154, 46, 83),
            (547, 1154, 46, 83),
            (675, 1154, 46, 82),
        ),
    },
)


def main():
    open_canvas(CANVAS_WIDTH, CANVAS_HEIGHT)
    try:
        clear_canvas()
        update_canvas()
        delay(1.0)
    finally:
        close_canvas()


if __name__ == "__main__":
    main()
