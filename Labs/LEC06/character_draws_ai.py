import math

from pico2d import clear_canvas, delay, load_image, open_canvas, update_canvas

CANVAS_WIDTH = 800
CANVAS_HEIGHT = 600
FRAME_DELAY = 0.04


def interpolate(start, end, divisions):
    start_x, start_y = start
    end_x, end_y = end
    for index in range(divisions + 1):
        fraction = index / divisions
        yield (
            start_x + (end_x - start_x) * fraction,
            start_y + (end_y - start_y) * fraction,
        )


def circle_route():
    center_x = CANVAS_WIDTH / 2
    center_y = CANVAS_HEIGHT / 2
    radius = 200
    for degree in range(360):
        angle = math.radians(degree)
        yield (
            center_x + radius * math.cos(angle),
            center_y + radius * math.sin(angle),
        )


def rectangle_route():
    corners = ((50, 550), (750, 550), (750, 50), (50, 50), (50, 550))
    for start, end in zip(corners, corners[1:]):
        distance = max(abs(end[0] - start[0]), abs(end[1] - start[1]))
        yield from interpolate(start, end, distance // 5)


def triangle_route():
    vertices = ((100, 100), (700, 100), (400, 500), (100, 100))
    for start, end in zip(vertices, vertices[1:]):
        yield from interpolate(start, end, 100)


def animate(sprite, route):
    for position in route:
        clear_canvas()
        sprite.draw(*position)
        update_canvas()
        delay(FRAME_DELAY)


def main():
    open_canvas(CANVAS_WIDTH, CANVAS_HEIGHT)
    sprite = load_image("character.png")

    while True:
        animate(sprite, circle_route())
        animate(sprite, rectangle_route())
        animate(sprite, triangle_route())


if __name__ == "__main__":
    main()
