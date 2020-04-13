from turtle import *
from math import *
'''
    file structure:
        num
        px
        py
        vx
        vy
        g
        c
        s
        k
'''
with open('SUGE.cfg') as file:
    f = file.readlines()
    for i in range(1, 6):
        f[i] = list(map(float, f[i].split()))
    num = range(int(f[0]))
    p = [Vec2D(f[1][i], f[2][i]) for i in num]
    v = [Vec2D(f[3][i], f[4][i]) for i in num]
    g = f[5]
    c = f[6].split()
    s = float(f[7])
    k = int(f[8])
#p = [Vec2D(0, 0), Vec2D(100, 0), Vec2D(50, sqrt(3) * 50)]
#v = [Vec2D(0, -10), Vec2D(0, 10), Vec2D(-5 * sqrt(3), 5)]
#g = [10000, 10000, 10000]
#p = [Vec2D(50, 50), Vec2D(-50, 0), Vec2D(50, -100), Vec2D(50, 300)]
#v = [Vec2D(-5, 2.5), Vec2D(5, -2.5), Vec2D(0, 2.5), Vec2D(10, -2.5)]
#g = [10000, 10000, 10000, 0]
#c = ['white', 'yellow', 'red', 'cyan']
#num = range(4)
t = []
arr = []
cnt = 0
bgcolor('black')
title('SUG Engine')
for i in num:
    t.append(Turtle())
    t[i].pencolor(c[i])
    t[i].speed(0)
    t[i].penup()
    t[i].goto(p[i])
    t[i].shape('circle')
    t[i].shapesize(stretch_wid = 0.3)
    t[i].dot(5)
    t[i].pendown()
while True:
    arr.clear()
    for i in num:
        for j in num:
            if i < j and (g[i] != 0 or g[j] != 0) and \
               t[i].isvisible() and t[j].isvisible() and abs(p[j] - p[i]) < 1:
                arr.append((i, j))
    for i, j in arr:
        x = i if g[i] > g[j] else j
        y = j if g[i] > g[j] else i
        print(x, y, v[x])
        t[y].ht()
        t[y].penup()
        v[x] += v[y] * (g[y] / g[x])
        g[x] += g[y]
        g[y] = 0
        print(v[x])
    for i in num:
        for j in num:
            if i == j:
                continue
            v[i] += ((p[j] - p[i]) * g[j] * abs(p[j] - p[i]) ** -3) * s
    for i in num:
        p[i] += v[i] * s
        if cnt % k == 0:
            t[i].goto(p[i])
    cnt += 1
