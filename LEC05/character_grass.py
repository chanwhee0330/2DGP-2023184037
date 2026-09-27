from pico2d import *

open_canvas()
grass = load_image('grass.png')
character = load_image('character.png')

x = 0
y = 90
turn = 0

while True:
    clear_canvas()
    grass.draw(400, 30)
    character.draw(x, y)
    update_canvas()

    if turn == 0:
        x += 2
        if x > 800:
            turn = 1

    elif turn == 1:
        y += 2
        if y > 600:
            turn = 2

    elif turn == 2:
        x -= 2
        if x < 0:
            turn = 3

    elif turn == 3:
        y -= 2
        if y < 90:
            turn = 0

    delay(0.01)
