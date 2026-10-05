"""Sonic 스프라이트 시트의 모든 동작을 순서대로 재생한다."""

import os
from pathlib import Path

import pico2d


CANVAS_WIDTH = 1200
CANVAS_HEIGHT = 800
SCRIPT_DIRECTORY = Path(__file__).resolve().parent
SPRITE_FILENAME = 'sonic-sprite.png'
SPRITE_PATH = SCRIPT_DIRECTORY / SPRITE_FILENAME


def load_sprite():
    """한글 경로에서도 안정적으로 스프라이트 이미지를 불러온다."""
    if not SPRITE_PATH.is_file():
        raise FileNotFoundError(f'스프라이트 이미지를 찾을 수 없습니다: {SPRITE_PATH}')

    previous_directory = Path.cwd()
    try:
        os.chdir(SCRIPT_DIRECTORY)
        return pico2d.load_image(SPRITE_FILENAME)
    except Exception as error:
        raise RuntimeError(f'스프라이트 이미지를 불러오지 못했습니다: {error}') from error
    finally:
        os.chdir(previous_directory)


def main():
    """애니메이션 뷰어를 실행한다."""
    canvas_opened = False
    try:
        pico2d.open_canvas(CANVAS_WIDTH, CANVAS_HEIGHT)
        canvas_opened = True
        load_sprite()
        return 0
    except Exception as error:
        print(f'애니메이션 뷰어 실행 오류: {error}')
        return 1
    finally:
        if canvas_opened:
            pico2d.close_canvas()


if __name__ == '__main__':
    raise SystemExit(main())
