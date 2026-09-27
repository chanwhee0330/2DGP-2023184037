from pico2d import *
import math

open_canvas(800, 600)
character=load_image('character.png')
x=400
y=300
angle=0
while True:
    clear_canvas()
    character.draw(x,y)
    update_canvas()

    angle+=math.radians(2)
    x=400+100*math.cos(angle)
    y=300+100*math.sin(angle)

    delay(0.01)
    
