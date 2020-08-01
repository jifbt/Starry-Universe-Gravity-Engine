'''
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
from turtle import *
from _tkinter import TclError
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
    painter = []
    arr = []
    cnt = 0
    bgcolor(background_color)
    title('SUG Engine')
    delay(0)
    for i in num:
        painter.append(Turtle())
        painter[i].pencolor(color[i])
        painter[i].speed(0)
        painter[i].penup()
        painter[i].goto(position[i])
        painter[i].shape('circle')
        painter[i].shapesize(stretch_wid = radius[i])
        painter[i].dot(5)
        painter[i].pendown()
    while True:
        arr.clear()
        for i in num:
            for j in num:
                if i < j and (gravity[i] != 0 or gravity[j] != 0) and \
                   painter[i].isvisible() and painter[j].isvisible() and abs(position[j] - position[i]) < 1:
                    arr.append((i, j))
        for i, j in arr:
            x = i if gravity[i] > gravity[j] else j
            y = j if gravity[i] > gravity[j] else i
            painter[y].ht()
            painter[y].penup()
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
                painter[i].goto(position[i])
        cnt += 1
if __name__ == '__main__':
    try:
        main()
    except TclError:
        print('Simulator closed successfully by user.')
