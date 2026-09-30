"""Drill #8 - 여러 동작을 차례로 보여 주는 스프라이트 애니메이션 뷰어."""

import os
from pathlib import Path

from pico2d import *


def main():
    open_canvas(800, 600)
    try:
        clear_canvas()
        update_canvas()
        delay(1.0)
    finally:
        close_canvas()


if __name__ == "__main__":
    main()
