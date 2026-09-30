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
