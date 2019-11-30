from turtle import *
p = [Vec2D(0, 0), Vec2D(-100, 0), Vec2D(-100, 30)]
v = [Vec2D(0, 0), Vec2D(0, -1000), Vec2D(0, -1000)]
g = [100000000, 100000, 100000]
c = ['white', 'yellow', 'red']
t = []
bgcolor('black')
title('GUGE Simulator')
for i in range(len(p)):
    t.append(Turtle())
    t[i].pencolor(c[i])
    t[i].hideturtle()
    t[i].speed(0)
    t[i].penup()
    t[i].goto(p[i])
    t[i].dot(5)
    t[i].pendown()
cnt = 0
while True:
    for i in range(len(p)):
        for j in range(len(p)):
            if i == j:
                continue
            v[i] += ((p[j] - p[i]) * g[j] * abs(p[j] - p[i]) ** -3) * 0.01
        p[i] += v[i] * 0.01
    for i in range(len(p)):
        t[i].goto(p[i])
