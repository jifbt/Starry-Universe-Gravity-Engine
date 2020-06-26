from turtle import *
p, v = Vec2D(-300, 0), Vec2D(500, 300)
bgcolor('black')
pencolor('white')
speed(0)
hideturtle()
dot(5, 'yellow')
write('Sun', False, 'center', ('Arial', 16, 'normal'))
penup()
goto(p)
pendown()
while True:
    v = v + (p * -100000000 * abs(p) ** -3) * 0.01
    p = p + v * 0.01
    goto(p)
