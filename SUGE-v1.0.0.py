'''
    file structure:
        num
        position-x
        position-y
        velocity-x
        velocoty-y
        gravity
        radii
        color
        simulate_acc
        display_freq
        background_color
'''
from turtle import *
from _tkinter import TclError
import json
def get(obj, num, key, default = None, ls = True):
    if key not in obj and default:
        return default
    if isinstance(obj[key], list) or not ls:
        return obj[key]
    else:
        return [obj[key]] * num
def main():
    obj = json.load(open('SUGE.json'))
    num = obj['num']
    position = [Vec2D(obj['px'][i], obj['py'][i]) for i in range(num)]
    velocity = [Vec2D(obj['vx'][i], obj['vy'][i]) for i in range(num)]
    gravity = get(obj, num, 'g')
    radii = get(obj, num, 'r', [0.3] * num)
    color = get(obj, num, 'c')
    simulate_acc = get(obj, num, 'sac', 0.001, False)
    display_freq = get(obj, num, 'dfq', 1000, False)
    background_color = get(obj, num, 'bg', 'black', False)
    painter = []
    arr = []
    cnt = 0
    bgcolor(background_color)
    title('SUG Engine')
    delay(0)
    for i in range(num):
        painter.append(Turtle())
        painter[i].pencolor(color[i])
        painter[i].speed(0)
        painter[i].penup()
        painter[i].goto(position[i])
        painter[i].shape('circle')
        painter[i].shapesize(stretch_wid = radii[i])
        painter[i].dot(5)
        painter[i].pendown()
    while True:
        arr.clear()
        for i in range(num):
            for j in range(num):
                if i < j and (gravity[i] != 0 or gravity[j] != 0) and \
                   painter[i].isvisible() and painter[j].isvisible() \
                   and abs(position[j] - position[i]) < 1:
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
        for i in range(num):
            for j in range(num):
                if i == j or gravity[j] == 0:
                    continue
                velocity[i] += ((position[j] - position[i]) * gravity[j] * abs(position[j] - position[i]) ** -3) * simulate_acc
        for i in range(num):
            position[i] += velocity[i] * simulate_acc
            if cnt % display_freq == 0:
                painter[i].goto(position[i])
        cnt += 1
if __name__ == '__main__':
    try:
        main()
    except TclError:
        print('Simulator closed successfully by user.')
