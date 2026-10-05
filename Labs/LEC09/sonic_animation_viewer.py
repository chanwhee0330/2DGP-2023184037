"""Sonic 스프라이트 시트의 모든 동작을 순서대로 재생한다."""

from pathlib import Path

import pico2d


CANVAS_WIDTH = 1200
CANVAS_HEIGHT = 800
SCRIPT_DIRECTORY = Path(__file__).resolve().parent
SPRITE_FILENAME = 'sonic-sprite.png'
SPRITE_PATH = SCRIPT_DIRECTORY / SPRITE_FILENAME


def main():
    """애니메이션 뷰어를 실행한다."""
    pico2d.open_canvas(CANVAS_WIDTH, CANVAS_HEIGHT)
    pico2d.close_canvas()
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
