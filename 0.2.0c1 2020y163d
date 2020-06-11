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
class Star:
    def __init__(self, position, velocity, gravity, color, painter = None):
        self.position = position
        self.velocity = velocity
        self.gravity = gravity
        self.painter = painter or Turtle()
        self.painter.pencolor(color)
        self.painter.speed(0)
        self.painter.penup()
        self.goto()
        self.painter.shape('circle')
        self.painter.shapesize(stretch_wid = 0.3)
        self.painter.pendown()
    def goto(self):
        self.painter.goto(self.position)
    def copy(self):
        return __class__(self.position.copy(),
                         self.velocity.copy(),
                         self.gravity,
                         self.turtle)
class Gravity_system:
    def __init__(self, similate_acc, display_acc, num = 0, stars = None):
        self.num = num
        self.stars = stars or []
        self.simulate_acc = similate_acc
        self.display_acc = display_acc
        self.cnt = 0
    def add_star(self, star):
        self.num += 1
        self.stars.append(star)
    def remove_atar(self, star_no):
        self.num -= 1
        return self.stars.pop(star_no)
    def simulate(self):
        new = self.stars.copy()
        for i in range(self.num):
            for j in range(self.num):
                if i == j:
                    continue
                new[i].velocity += ((self.stars[j].position - self.stars[i].position) \
                                    * self.stars[j].gravity * \
                                    abs(self.stars[j].position - self.stars[i].position) ** -3) * \
                                    self.simulate_acc
            new[i].position += new[i].velocity * self.simulate_acc
            if self.cnt % self.display_acc == 0:
                new[i].goto()
                print(i)
        self.stars = new
        self.cnt += 1
with open('SUGE.cfg') as file:
    f = file.readlines()
    for i in range(1, 6):
        f[i] = list(map(float, f[i].split()))
    num = int(f[0])
    position = [Vec2D(f[1][i], f[2][i]) for i in range(num)]
    velocity = [Vec2D(f[3][i], f[4][i]) for i in range(num)]
    gravity = f[5]
    color = f[6].split()
    simulate_acc = float(f[7])
    display_acc = int(f[8])
gravity_system = Gravity_system(simulate_acc, display_acc)
bgcolor('black')
title('SUG Engine')
for i in range(num):
    gravity_system.add_star(Star(position[i], velocity[i], gravity[i], color[i]))
while True:
    gravity_system.simulate()
