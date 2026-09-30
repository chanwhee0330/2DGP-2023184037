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
    {
        "name": "WALK",
        "seconds_per_frame": 0.11,
        "frames": (
            (24, 1024, 48, 83),
            (152, 1024, 48, 84),
            (280, 1024, 51, 83),
            (408, 1024, 48, 82),
            (536, 1024, 48, 83),
            (664, 1024, 48, 84),
            (792, 1024, 52, 83),
            (920, 1024, 48, 82),
        ),
    },
    {
        "name": "RUN",
        "seconds_per_frame": 0.08,
        "frames": (
            (15, 896, 51, 79),
            (143, 896, 51, 78),
            (271, 896, 57, 77),
            (399, 896, 51, 78),
            (527, 896, 51, 79),
            (655, 896, 51, 78),
            (783, 896, 57, 77),
            (911, 896, 51, 78),
        ),
    },
    {
        "name": "JUMP",
        "seconds_per_frame": 0.10,
        "frames": (
            (15, 768, 60, 80),
            (141, 769, 62, 76),
            (269, 768, 65, 74),
            (399, 768, 58, 80),
            (531, 769, 53, 82),
            (661, 770, 53, 80),
            (790, 774, 51, 74),
            (918, 776, 53, 70),
            (1046, 768, 53, 74),
            (1174, 768, 52, 71),
            (1302, 768, 51, 70),
            (1431, 768, 50, 63),
        ),
    },
    {
        "name": "SLASH",
        "seconds_per_frame": 0.09,
        "frames": (
            (19, 640, 53, 74),
            (148, 640, 52, 73),
            (276, 640, 57, 73),
            (404, 640, 63, 74),
            (532, 640, 101, 74),
            (660, 640, 54, 74),
        ),
    },
    {
        "name": "THRUST",
        "seconds_per_frame": 0.11,
        "frames": (
            (18, 512, 54, 74),
            (143, 512, 58, 74),
            (274, 512, 98, 73),
            (402, 512, 63, 73),
        ),
    },
)


def draw_frame(sprite_sheet, frame):
    """잘라 낸 크기가 달라도 원래 격자 중심을 기준으로 흔들림 없이 그린다."""
    left, bottom, width, height = frame

    cell_left = (left // CELL_SIZE) * CELL_SIZE
    cell_bottom = (bottom // CELL_SIZE) * CELL_SIZE
    frame_center_x = left + width / 2
    frame_center_y = bottom + height / 2

    offset_x = (frame_center_x - (cell_left + CELL_SIZE / 2)) * DRAW_SCALE
    offset_y = (frame_center_y - (cell_bottom + CELL_SIZE / 2)) * DRAW_SCALE

    sprite_sheet.clip_draw(
        left,
        bottom,
        width,
        height,
        CANVAS_WIDTH / 2 + offset_x,
        CANVAS_HEIGHT / 2 + offset_y,
        width * DRAW_SCALE,
        height * DRAW_SCALE,
    )


def handle_events():
    """창 닫기 또는 Esc 입력이 들어오면 False를 반환한다."""
    for event in get_events():
        if event.type == SDL_QUIT:
            return False
        if event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            return False
    return True


def load_sprite_sheet():
    """한글이 포함된 절대 경로에서도 pico2d가 이미지를 읽도록 한다."""
    sprite_directory = Path(__file__).resolve().parent
    previous_directory = Path.cwd()

    try:
        os.chdir(sprite_directory)
        return load_image("SamuraiSheet.png")
    finally:
        os.chdir(previous_directory)


def main():
    open_canvas(CANVAS_WIDTH, CANVAS_HEIGHT)

    try:
        sprite_sheet = load_sprite_sheet()

        animation_index = 0
        frame_index = 0
        completed_repeats = 0
        is_paused = False
        next_change_time = get_time() + ANIMATIONS[0]["seconds_per_frame"]

        print("Esc 키를 누르거나 창을 닫으면 종료합니다.")
        print(f"재생: {ANIMATIONS[0]['name']} (1/{len(ANIMATIONS)})")

        running = True
        while running:
            running = handle_events()
            now = get_time()
            animation = ANIMATIONS[animation_index]

            if now >= next_change_time:
                if is_paused:
                    animation_index = (animation_index + 1) % len(ANIMATIONS)
                    animation = ANIMATIONS[animation_index]
                    frame_index = 0
                    completed_repeats = 0
                    is_paused = False
                    next_change_time = now + animation["seconds_per_frame"]
                    print(
                        f"재생: {animation['name']} "
                        f"({animation_index + 1}/{len(ANIMATIONS)})"
                    )
                elif frame_index == len(animation["frames"]) - 1:
                    completed_repeats += 1
                    if completed_repeats == REPEAT_COUNT:
                        # 다섯 번째 재생의 마지막 프레임에서 정확히 1초간 멈춘다.
                        is_paused = True
                        next_change_time = now + PAUSE_SECONDS
                    else:
                        frame_index = 0
                        next_change_time = now + animation["seconds_per_frame"]
                else:
                    frame_index += 1
                    next_change_time = now + animation["seconds_per_frame"]

            clear_canvas()
            draw_frame(sprite_sheet, animation["frames"][frame_index])
            update_canvas()
            delay(0.01)
    finally:
        close_canvas()


if __name__ == "__main__":
    main()
