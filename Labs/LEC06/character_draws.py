# 실습 과제 진행
from pico2d import *
import math

open_canvas(800, 600)

character = load_image('character.png')

def move_circle():
    print("CIRCLE")

    for degree in range(360):
        theta = math.radians(degree)
        x =400+200*math.cos(theta)
        y =300+200*math.sin(theta)

        draw_character(x, y, 0.04)
    pass
    
def move_top():
    print("top")
    for x in range(50,750,5):
        draw_character(x, 550, 0.04)
    pass

def draw_character(x, y, frame_delay=0.05):
    clear_canvas()
    character.draw(x,y)
    update_canvas()
    delay(frame_delay)

def move_right():
    print("right")
    for y  in range(550,50,-5):
        draw_character(750, y, 0.04)
    pass

def move_bottom():
    print("bottom")
    for x in range(750,50,-5):
        draw_character(x, 50, 0.04)
    pass

def move_left():
    print("left")
    for y in range(50,550,5):
        draw_character(50, y, 0.04)
    pass

def move_rectangle():
    print("RECTANGLE")  
    move_top()
    move_right()
    move_bottom()
    move_left()
    pass

def move_one():
    print("one")
    n = 100
    for step in range(n+1):
        t = step/n
        x = 100+(700-100)*t
        y = 100+(100-100)*t
        draw_character(x, y, 0.04)
    pass

def move_two():
    print("two")
    n = 100
    for step in range(n+1):
        t=step/n
        x=700+(400-700)*t
        y=100+(500-100)*t
        draw_character(x, y, 0.04)
    pass

def move_three():
    print("three")
    n = 100
    for step in range(n+1):
        t=step/n
        x=400+(100-400)*t
        y=500+(100-500)*t
        draw_character(x, y, 0.04)
    pass

def move_triangle():
    print("TRIANGLE")
    move_one()
    move_two()
    move_three()
    pass

while True:
    move_circle()
    move_rectangle()
    move_triangle()
    pass

close_canvas()