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
        t[y].ht()
        t[y].penup()
        v[x] = 1 / (g[x] + g[y]) * (v[x] * g[x] + v[y] * g[y])
        p[x] = 1 / (g[x] + g[y]) * (p[x] * g[x] + p[y] * g[y])
        g[x] += g[y]
        g[y] = 0
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
