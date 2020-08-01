from turtle import *
from math import *
'''
    SUG Engine v0.2.2
    file structure:
        num
        position-x
        position-y
        velicity-x
        velocity-y
        gravity
        radius
        color
        simulate_acc
        display_acc
'''
class Star:
    def __init__(self, position, velocity, gravity, radius,
                 color, painter = None):
        self.position = position
        self.velocity = velocity
        self.gravity = gravity
        self.radius = radius
        self.painter = painter or Turtle()
        self.painter.pencolor(color)
        self.painter.speed(0)
        self.painter.penup()
        self.goto()
        self.painter.shape('circle')
        self.painter.shapesize(stretch_wid = radius)
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
    def remove_star(self, star_no):
        self.num -= 1
        return self.stars.pop(star_no)
    def simulate(self):
        new = self.stars.copy()
        collede_list = []
        for i in range(self.num):
            for j in range(self.num):
                if i < j and \
                   abs(self.stars[i].position -
                       self.stars[j].position) < \
                       self.stars[i].radius + \
                       self.stars[j].radius:
                    collede_list.append((i, j))
        for i, j in collede_list:
            x = i if self.stars[i].gravity > self.stars[j].gravity else j
            y = j if self.stars[i].gravity > self.stars[j].gravity else i
            self.stars[y].painter.ht()
            self.stars[y].painter.penup()
            self.stars[x].velocity = 1 / (self.stars[x].gravity +
                                          self.stars[y].gravity) * \
                                          (self.stars[x].velocity *
                                           self.stars[x].gravity +
                                           self.stars[y].velocity *
                                           self.stars[y].gravity)
            self.stars[x].position = 1 / (self.stars[x].gravity +
                                          self.stars[y].gravity) * \
                                          (self.stars[x].position *
                                           self.stars[x].gravity +
                                           self.stars[y].position *
                                           self.stars[y].gravity)
            self.stars[x].gravity += self.stars[y].gravity
            self.stars[y].gravity = 0
        for i in range(self.num):
            for j in range(self.num):
                if i == j:
                    continue
                new[i].velocity += ((self.stars[j].position - 
                                     self.stars[i].position) *
                                    self.stars[j].gravity * 
                                    abs(self.stars[j].position -
                                        self.stars[i].position) ** -3) * \
                                    self.simulate_acc
            new[i].position += new[i].velocity * self.simulate_acc
            if self.cnt % self.display_acc == 0:
                new[i].goto()
        self.stars = new
        self.cnt += 1
with open('SUGE.cfg') as file:
    f = file.readlines()
    for i in range(1, 7):
        f[i] = list(map(float, f[i].split()))
    num = int(f[0])
    position = [Vec2D(f[1][i], f[2][i]) for i in range(num)]
    velocity = [Vec2D(f[3][i], f[4][i]) for i in range(num)]
    gravity = f[5]
    radii = f[6]
    color = f[7].split()
    simulate_acc = float(f[8])
    display_acc = int(f[9])
gravity_system = Gravity_system(simulate_acc, display_acc)
bgcolor('black')
title('SUG Engine')
for i in range(num):
    gravity_system.add_star(Star(position[i], velocity[i],
                                 gravity[i], radii[i], color[i]))
while True:
    gravity_system.simulate()
