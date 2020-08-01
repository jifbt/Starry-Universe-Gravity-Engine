from turtle import *
from math import *
from _tkinter import TclError
'''
    SUG Enging v0.1.7
    file structure:
        num
        position-x
        position-y
        velocity-x
        velocoty-y
        gravity
        radius
        color
        simulate_acc
        display_freq
        background_color
'''
def main():
    with open('SUGE.cfg') as file:
        f = file.readlines()
        for i in range(1, 7):
            f[i] = list(map(float, f[i].split()))
        num = range(int(f[0]))
        position = [Vec2D(f[1][i], f[2][i]) for i in num]
        velocity = [Vec2D(f[3][i], f[4][i]) for i in num]
        gravity = f[5]
        radius = f[6]
        color = f[7].split()
        simulate_acc = float(f[8])
        display_freq = int(f[9])
        background_color = f[10]
    t = []
    arr = []
    cnt = 0
    bgcolor(background_color)
    title('SUG Engine')
    delay(0)
    for i in num:
        t.append(Turtle())
        t[i].pencolor(color[i])
        t[i].speed(0)
        t[i].penup()
        t[i].goto(position[i])
        t[i].shape('circle')
        t[i].shapesize(stretch_wid = radius[i])
        t[i].dot(5)
        t[i].pendown()
    while True:
        arr.clear()
        for i in num:
            for j in num:
                if i < j and (gravity[i] != 0 or gravity[j] != 0) and \
                   t[i].isvisible() and t[j].isvisible() and abs(position[j] - position[i]) < 1:
                    arr.append((i, j))
        for i, j in arr:
            x = i if gravity[i] > gravity[j] else j
            y = j if gravity[i] > gravity[j] else i
            t[y].ht()
            t[y].penup()
            velocity[x] = 1 / (gravity[x] + gravity[y]) * (velocity[x] * gravity[x] + velocity[y] * gravity[y])
            position[x] = 1 / (gravity[x] + gravity[y]) * (position[x] * gravity[x] + position[y] * gravity[y])
            gravity[x] += gravity[y]
            gravity[y] = 0
        for i in num:
            for j in num:
                if i == j or gravity[j] == 0:
                    continue
                velocity[i] += ((position[j] - position[i]) * gravity[j] * abs(position[j] - position[i]) ** -3) * simulate_acc
        for i in num:
            position[i] += velocity[i] * simulate_acc
            if cnt % display_freq == 0:
                t[i].goto(position[i])
        cnt += 1
if __name__ == '__main__':
    try:
        main()
    except TclError:
        print('Simulator closed successfully by user.')
