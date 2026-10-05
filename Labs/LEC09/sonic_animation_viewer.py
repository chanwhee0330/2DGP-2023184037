"""Sonic 스프라이트 시트의 모든 동작을 순서대로 재생한다.

실행: python sonic_animation_viewer.py
종료: 창 닫기 또는 Esc 키
"""

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
MAX_SCREEN_RATIO = 0.4
MODE_PLAYING = 'PLAYING'
MODE_PAUSED = 'PAUSED'
MODE_NEXT = 'NEXT'
EXPECTED_FRAME_COUNTS = (11, 12, 6, 9, 6, 6, 6, 8, 8, 4)
EXPECTED_TOTAL_FRAMES = 76
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
    movement_speed: float = 0.0


@dataclass
class PlaybackState:
    """현재 재생 중인 동작과 프레임의 상태."""

    animation_index: int = 0
    frame_index: int = 0
    frame_elapsed: float = 0.0
    loops_completed: int = 0
    mode: str = MODE_PLAYING
    pause_elapsed: float = 0.0
    screen_x: float = CANVAS_WIDTH / 2

    @property
    def current_animation(self):
        return ANIMATIONS[self.animation_index]

    @property
    def current_frame(self):
        return self.current_animation.frames[self.frame_index]


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
        movement_speed=60.0,
    ),
    Animation(
        'A03',
        '대시·공격 동작',
        frames_from_top_spans(
            121,
            163,
            ((1, 33), (39, 73), (89, 123), (130, 163), (181, 214), (228, 260)),
        ),
        movement_speed=180.0,
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
        movement_speed=150.0,
    ),
    Animation(
        'A06',
        '고속 달리기 A',
        frames_from_top_spans(
            238,
            273,
            ((1, 29), (36, 65), (74, 104), (111, 141), (149, 178), (186, 216)),
        ),
        movement_speed=130.0,
    ),
    Animation(
        'A07',
        '고속 달리기 B',
        frames_from_top_spans(
            283,
            317,
            ((1, 29), (36, 65), (72, 110), (123, 161), (172, 210), (218, 255)),
        ),
        movement_speed=150.0,
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
        movement_speed=115.0,
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


def validate_animations():
    """PRD에 정의된 동작 수, 프레임 수와 좌표 경계를 검사한다."""
    if len(ANIMATIONS) != len(EXPECTED_FRAME_COUNTS):
        raise ValueError(f'동작 수가 올바르지 않습니다: {len(ANIMATIONS)}')

    total_frames = 0
    for index, (animation, expected_count) in enumerate(
        zip(ANIMATIONS, EXPECTED_FRAME_COUNTS),
        start=1,
    ):
        expected_id = f'A{index:02d}'
        if animation.animation_id != expected_id:
            raise ValueError(f'동작 ID 순서가 올바르지 않습니다: {animation.animation_id}')
        if len(animation.frames) != expected_count:
            raise ValueError(
                f'{animation.animation_id} 프레임 수 오류: '
                f'{len(animation.frames)}개, 예상 {expected_count}개'
            )

        total_frames += len(animation.frames)
        for frame in animation.frames:
            if frame.width <= 0 or frame.height <= 0:
                raise ValueError(f'{animation.animation_id}에 크기가 0 이하인 프레임이 있습니다.')
            if (
                frame.x < 0
                or frame.y < 0
                or frame.x + frame.width > SHEET_WIDTH
                or frame.y + frame.height > SHEET_HEIGHT
            ):
                raise ValueError(f'{animation.animation_id} 프레임이 이미지 경계를 벗어납니다.')

    if total_frames != EXPECTED_TOTAL_FRAMES:
        raise ValueError(f'전체 프레임 수가 올바르지 않습니다: {total_frames}')


def select_next_animation(state):
    """다음 동작을 선택하고 재생 상태를 초기화한다."""
    state.animation_index = (state.animation_index + 1) % len(ANIMATIONS)
    state.frame_index = 0
    state.frame_elapsed = 0.0
    state.loops_completed = 0
    state.pause_elapsed = 0.0
    state.mode = MODE_PLAYING


def update_playback(state, elapsed, movement_bounds):
    """경과한 시간만큼 현재 동작의 프레임을 진행한다."""
    elapsed = max(0.0, elapsed)
    if state.mode == MODE_NEXT:
        select_next_animation(state)
        return

    if state.mode == MODE_PAUSED:
        state.pause_elapsed += elapsed
        if state.pause_elapsed >= PAUSE_DURATION:
            state.mode = MODE_NEXT
        return

    if state.mode != MODE_PLAYING:
        return

    movement_speed = state.current_animation.movement_speed
    if movement_speed > 0.0:
        left_bound, right_bound = movement_bounds
        travel_width = right_bound - left_bound
        if travel_width > 0:
            state.screen_x += movement_speed * elapsed
            if state.screen_x > right_bound:
                state.screen_x = left_bound + (state.screen_x - right_bound) % travel_width

    state.frame_elapsed += elapsed
    while state.frame_elapsed >= FRAME_INTERVAL:
        state.frame_elapsed -= FRAME_INTERVAL
        last_frame_index = len(state.current_animation.frames) - 1
        if state.frame_index < last_frame_index:
            state.frame_index += 1
            continue

        state.loops_completed += 1
        if state.loops_completed >= REPEAT_COUNT:
            state.frame_elapsed = 0.0
            state.pause_elapsed = 0.0
            state.mode = MODE_PAUSED
            break
        state.frame_index = 0


def maximum_frame_height():
    """등록된 프레임 가운데 가장 큰 높이를 반환한다."""
    return max(frame.height for animation in ANIMATIONS for frame in animation.frames)


def calculate_integer_scale():
    """모든 프레임이 화면의 40% 안에 드는 최대 정수 배율을 구한다."""
    frames = (frame for animation in ANIMATIONS for frame in animation.frames)
    dimensions = tuple((frame.width, frame.height) for frame in frames)
    maximum_width = max(width for width, _ in dimensions)
    maximum_height = max(height for _, height in dimensions)
    width_scale = CANVAS_WIDTH * MAX_SCREEN_RATIO / maximum_width
    height_scale = CANVAS_HEIGHT * MAX_SCREEN_RATIO / maximum_height
    return max(1, int(min(width_scale, height_scale)))


def draw_frame(sprite, frame, screen_anchor_x, screen_anchor_y, scale):
    """프레임의 하단 중앙 기준점을 화면 기준점에 맞춰 그린다."""
    center_x = screen_anchor_x + (frame.width / 2 - frame.resolved_anchor_x) * scale
    center_y = screen_anchor_y + (frame.height / 2 - frame.anchor_y) * scale
    sprite.clip_draw(
        frame.x,
        frame.y,
        frame.width,
        frame.height,
        center_x,
        center_y,
        frame.width * scale,
        frame.height * scale,
    )


def quit_requested():
    """창 닫기 또는 Esc 키 입력 여부를 확인한다."""
    for event in pico2d.get_events():
        if event.type == pico2d.SDL_QUIT:
            return True
        if event.type == pico2d.SDL_KEYDOWN and event.key == pico2d.SDLK_ESCAPE:
            return True
    return False


def run_animation_loop(sprite):
    """종료 입력이 들어올 때까지 모든 동작을 순서대로 재생한다."""
    state = PlaybackState()
    scale = calculate_integer_scale()
    widest_frame = max(
        frame.width for animation in ANIMATIONS for frame in animation.frames
    )
    horizontal_margin = widest_frame * scale / 2
    movement_bounds = (horizontal_margin, CANVAS_WIDTH - horizontal_margin)
    screen_anchor_y = (CANVAS_HEIGHT - maximum_frame_height() * scale) / 2
    previous_time = pico2d.get_time()

    while not quit_requested():
        current_time = pico2d.get_time()
        elapsed = current_time - previous_time
        previous_time = current_time
        update_playback(state, elapsed, movement_bounds)

        pico2d.clear_canvas()
        draw_frame(sprite, state.current_frame, state.screen_x, screen_anchor_y, scale)
        pico2d.update_canvas()


def load_sprite():
    """한글 경로에서도 안정적으로 스프라이트 이미지를 불러온다."""
    if not SPRITE_PATH.is_file():
        raise FileNotFoundError(f'스프라이트 이미지를 찾을 수 없습니다: {SPRITE_PATH}')

    previous_directory = Path.cwd()
    try:
        os.chdir(SCRIPT_DIRECTORY)
        return pico2d.load_image(SPRITE_FILENAME)
    except KeyboardInterrupt:
        return 0
    except Exception as error:
        raise RuntimeError(f'스프라이트 이미지를 불러오지 못했습니다: {error}') from error
    finally:
        os.chdir(previous_directory)


def main():
    """애니메이션 뷰어를 실행한다."""
    canvas_opened = False
    try:
        validate_animations()
        pico2d.open_canvas(CANVAS_WIDTH, CANVAS_HEIGHT)
        canvas_opened = True
        sprite = load_sprite()
        run_animation_loop(sprite)
        return 0
    except Exception as error:
        print(f'애니메이션 뷰어 실행 오류: {error}')
        return 1
    finally:
        if canvas_opened:
            pico2d.close_canvas()


if __name__ == '__main__':
    raise SystemExit(main())
