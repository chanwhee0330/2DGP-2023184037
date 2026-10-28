from math import pi
from time import monotonic

from pico2d import (
    SDL_KEYDOWN, SDL_KEYUP, SDLK_LEFT, SDLK_RIGHT, SDLK_SPACE,
    get_canvas_width, load_image,
)
from transitions import Machine


class Boy:
    def __init__(self):
        self.x, self.y = 400, 90
        self.frame = 0
        self.face_dir = 1
        self.move_dir = 0
        self.pressed_keys = set()
        self.image = load_image('animation_sheet.png')
        self.idle_started_at = monotonic()
        self.state_machine = Machine(
            model=self,
            states=[
                {'name': 'idle', 'on_enter': '_enter_idle'},
                {'name': 'run', 'on_enter': '_enter_run'},
                {'name': 'sleep', 'on_enter': '_enter_sleep'},
            ],
            initial='idle',
            auto_transitions=False,
        )
        self.state_machine.add_transition(
            trigger='idle_tick',
            source='idle',
            dest='sleep',
            conditions='_idle_timed_out',
        )
        # 내부 전이: Idle 상태를 유지하면서 애니메이션만 갱신한다.
        self.state_machine.add_transition(
            trigger='idle_tick',
            source='idle',
            dest=None,
            after='_update_idle_animation',
        )
        self.state_machine.add_transition(
            trigger='start_running',
            source='idle',
            dest='run',
        )
        self.state_machine.add_transition(
            trigger='stop_running',
            source='run',
            dest='idle',
        )
        self.state_machine.add_transition(
            trigger='run_tick',
            source='run',
            dest=None,
            after='_update_run',
        )
        self.state_machine.add_transition(
            trigger='wake_up',
            source='sleep',
            dest='idle',
        )

    def update(self):
        if self.state == 'idle':
            self.idle_tick()
        elif self.state == 'run':
            self.run_tick()

    def handle_event(self, event):
        if self.state == 'sleep':
            if event.type == SDL_KEYDOWN and event.key == SDLK_SPACE:
                self.wake_up()
            return

        if event.type not in (SDL_KEYDOWN, SDL_KEYUP):
            return
        if event.key not in (SDLK_LEFT, SDLK_RIGHT):
            return

        if event.type == SDL_KEYDOWN:
            self.pressed_keys.add(event.key)
        else:
            self.pressed_keys.discard(event.key)

        self.move_dir = (int(SDLK_RIGHT in self.pressed_keys)
                         - int(SDLK_LEFT in self.pressed_keys))
        if self.move_dir != 0:
            self.face_dir = self.move_dir
            if self.state == 'idle':
                self.start_running()
        elif self.state == 'run':
            self.stop_running()

    def _enter_idle(self):
        self.idle_started_at = monotonic()
        self.frame = 0

    def _idle_timed_out(self):
        return monotonic() - self.idle_started_at >= 5.0

    def _enter_run(self):
        self.frame = 0

    def _enter_sleep(self):
        self.pressed_keys.clear()
        self.move_dir = 0

    def _update_idle_animation(self):
        self.frame = (self.frame + 1) % 8

    def _update_run(self):
        self.frame = (self.frame + 1) % 8
        # 스프라이트의 반쪽 너비(50)만큼 여유를 두어 화면 안에 유지한다.
        self.x = max(50, min(get_canvas_width() - 50,
                             self.x + self.move_dir * 5))

    def draw(self):
        row = 300 if self.face_dir == 1 else 200
        if self.state == 'sleep':
            self.image.clip_composite_draw(
                0, row, 100, 100, self.face_dir * pi / 2, '',
                self.x, self.y - 25, 100, 100,
            )
        elif self.state == 'run':
            row = 100 if self.face_dir == 1 else 0
            self.image.clip_draw(self.frame * 100, row, 100, 100, self.x, self.y)
        else:
            self.image.clip_draw(self.frame * 100, row, 100, 100, self.x, self.y)
