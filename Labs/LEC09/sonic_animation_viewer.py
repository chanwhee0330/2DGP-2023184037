"""Sonic 스프라이트 시트의 모든 동작을 순서대로 재생한다."""

import os
from dataclasses import dataclass
from pathlib import Path

import pico2d


CANVAS_WIDTH = 1200
CANVAS_HEIGHT = 800
SHEET_WIDTH = 399
SHEET_HEIGHT = 525
FRAME_INTERVAL = 0.1
REPEAT_COUNT = 5
PAUSE_DURATION = 1.0
SCRIPT_DIRECTORY = Path(__file__).resolve().parent
SPRITE_FILENAME = 'sonic-sprite.png'
SPRITE_PATH = SCRIPT_DIRECTORY / SPRITE_FILENAME


@dataclass(frozen=True)
class Frame:
    """스프라이트 시트에서 잘라낼 한 프레임의 정보."""

    x: int
    y: int
    width: int
    height: int
    anchor_x: float | None = None
    anchor_y: float = 0.0

    @property
    def resolved_anchor_x(self):
        """별도 지정이 없으면 가로 중앙을 기준점으로 사용한다."""
        return self.width / 2 if self.anchor_x is None else self.anchor_x


@dataclass(frozen=True)
class Animation:
    """이름과 순서가 있는 동작별 프레임 모음."""

    animation_id: str
    name: str
    frames: tuple[Frame, ...]


def top_to_pico_y(top, height):
    """이미지 상단 기준 y 좌표를 Pico2D 하단 기준 좌표로 바꾼다."""
    return SHEET_HEIGHT - (top + height)


def frames_from_top_spans(top, bottom, spans):
    """상단 기준 행 범위와 가로 범위를 Pico2D 프레임으로 변환한다."""
    height = bottom - top + 1
    y = top_to_pico_y(top, height)
    return tuple(
        Frame(x=left, y=y, width=right - left + 1, height=height)
        for left, right in spans
    )


ANIMATIONS: tuple[Animation, ...] = (
    Animation(
        'A01',
        '대기·자세 전환',
        frames_from_top_spans(
            39,
            77,
            (
                (1, 29), (31, 56), (58, 86), (87, 115), (118, 147),
                (150, 179), (182, 210), (211, 239), (240, 268),
                (270, 293), (302, 330),
            ),
        ),
    ),
    Animation(
        'A02',
        '걷기',
        frames_from_top_spans(
            79,
            117,
            (
                (8, 33), (37, 63), (65, 95), (97, 133), (135, 166),
                (170, 201), (206, 231), (238, 261), (263, 292),
                (295, 330), (334, 365), (370, 398),
            ),
        ),
    ),
    Animation(
        'A03',
        '대시·공격 동작',
        frames_from_top_spans(
            121,
            163,
            ((1, 33), (39, 73), (89, 123), (130, 163), (181, 214), (228, 260)),
        ),
    ),
    Animation(
        'A04',
        '회전 전환',
        frames_from_top_spans(
            167,
            199,
            (
                (1, 29), (35, 63), (67, 96), (98, 128), (131, 159),
                (162, 190), (193, 222), (230, 260), (268, 297),
            ),
        ),
    ),
    Animation(
        'A05',
        '공 회전',
        frames_from_top_spans(
            206,
            232,
            ((1, 30), (36, 64), (70, 98), (105, 133), (139, 167), (174, 202)),
        ),
    ),
    Animation(
        'A06',
        '고속 달리기 A',
        frames_from_top_spans(
            238,
            273,
            ((1, 29), (36, 65), (74, 104), (111, 141), (149, 178), (186, 216)),
        ),
    ),
    Animation(
        'A07',
        '고속 달리기 B',
        frames_from_top_spans(
            283,
            317,
            ((1, 29), (36, 65), (72, 110), (123, 161), (172, 210), (218, 255)),
        ),
    ),
    Animation(
        'A08',
        '방향 전환·피격 동작',
        frames_from_top_spans(
            326,
            370,
            (
                (1, 24), (31, 59), (65, 84), (90, 114),
                (119, 143), (149, 168), (184, 223), (232, 270),
            ),
        ),
    ),
    Animation(
        'A09',
        '달리기 순환',
        frames_from_top_spans(
            377,
            416,
            (
                (1, 27), (31, 61), (64, 94), (99, 131),
                (136, 167), (176, 208), (217, 249), (254, 286),
            ),
        ),
    ),
    Animation(
        'A10',
        '세리머니·제스처',
        frames_from_top_spans(
            426,
            468,
            ((6, 39), (49, 82), (96, 118), (125, 147)),
        ),
    ),
)


def maximum_frame_height():
    """등록된 프레임 가운데 가장 큰 높이를 반환한다."""
    return max(frame.height for animation in ANIMATIONS for frame in animation.frames)


def draw_frame(sprite, frame, screen_anchor_x, screen_anchor_y):
    """프레임의 하단 중앙 기준점을 화면 기준점에 맞춰 그린다."""
    center_x = screen_anchor_x + frame.width / 2 - frame.resolved_anchor_x
    center_y = screen_anchor_y + frame.height / 2 - frame.anchor_y
    sprite.clip_draw(
        frame.x,
        frame.y,
        frame.width,
        frame.height,
        center_x,
        center_y,
    )


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
        sprite = load_sprite()
        pico2d.clear_canvas()
        baseline_y = (CANVAS_HEIGHT - maximum_frame_height()) / 2
        draw_frame(sprite, ANIMATIONS[0].frames[0], CANVAS_WIDTH / 2, baseline_y)
        pico2d.update_canvas()
        return 0
    except Exception as error:
        print(f'애니메이션 뷰어 실행 오류: {error}')
        return 1
    finally:
        if canvas_opened:
            pico2d.close_canvas()


if __name__ == '__main__':
    raise SystemExit(main())
