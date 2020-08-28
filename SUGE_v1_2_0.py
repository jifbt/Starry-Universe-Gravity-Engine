'''
    SUG Engine v1.2.0
    SUGE.py  -n number -px position-x -py position-y
            -vx velocity-x -vy velocity-y -g gravity[1]
            [-r radii<0.3>] -c gravity[1]
            [-sac simulate-accuracy<0.001>]
            [-dfq display-frequncy<1000>]
            [-bg background_color<black>]
    SUGE.py [-f file-path<"SUGE.json">]
    [1] accept length 1/number object(s).
        -gAll, -rAll, -cAll are aliases for -g, -r, -c. 
    file structure:
        num
        position-x
        position-y
        velocity-x
        velocity-y
        gravity
        [radius]
        color
        [simulate_acc]
        [display_freq]
        [background_color]
'''
from turtle import *
from _tkinter import TclError
import sys
import json
class Star:
    '''
        A 2D celestial body with initial position and velocity,
        gravity(mass), radius and color.
        Painter is used if given or else it will use a new painter.
    '''
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
    '''
        A set of celestial bodys given as Star objects.
        The initial celestial bodys can be given if needed.
    '''
    def __init__(self, similate_acc = 0.001, display_freq = 1000,
                 background_color = 'black', num = 0, stars = None):
        self.num = num
        self.stars = stars or []
        self.simulate_acc = similate_acc
        self.display_freq = display_freq
        self.background_color = background_color
        bgcolor(background_color)
        title('SUG Engine')
        delay(0)
        self.cnt = 0
    def add_star(self, star):
        '''
            Add a star to the set.
        '''
        self.num += 1
        self.stars.append(star)
    def remove_star(self, star_no):
        '''
            Remove a star to the set.
        '''
        self.num -= 1
        return self.stars.pop(star_no)
    def simulate(self):
        '''
            Simulate for one step.
        '''
        self.stars = self.stars.copy()
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
                if i == j or self.stars[j].gravity == 0:
                    continue
                self.stars[i].velocity += ((self.stars[j].position - 
                                     self.stars[i].position) *
                                    self.stars[j].gravity * 
                                    abs(self.stars[j].position -
                                        self.stars[i].position) ** -3) * \
                                    self.simulate_acc
            self.stars[i].position += self.stars[i].velocity * self.simulate_acc
            if self.cnt % self.display_freq == 0:
                self.stars[i].goto()
        self.cnt += 1

def parse_args():
    '''
        return argument split by words begin with '-' from command line.
    '''
    args = {}
    for i in sys.argv[1:]:
        if i.startswith('-') and not i[1].isdigit():
            key_now = i
            args[i] = []
        else:
            args[key_now].append(i)
    return args
def get(obj, num, key, default = None, ls = True):
    '''
        return values from .json objects.
    '''
    if key not in obj:
        return default
    elif not ls or len(obj[key]) == num:
        return obj[key]
    else:
        return [obj[key]] * num
def get2(obj, num, key, default = None, ls = True, cls = float, hasAlias = False):
    '''
        return values from command line.
    '''
    if key not in obj:
        if '{}All'.format(key) in obj and hasAlias:
            return cls(obj['{}All'.format(key)]) * num
        else:
            return default
    elif not ls:
        return cls(obj[key][0])
    elif len(obj[key]) == num:
        return list(map(cls, obj[key]))
    else:
        print([cls(obj[key][0])] * num)
        return [cls(obj[key][0])] * num
def main():
    args = parse_args()
    keys = list(args.keys())
    if ['-ver'] == keys:
        print(__doc__.splitlines()[1][4:])
        return
    elif ['-help'] == keys:
        print(__doc__)
        return
    elif ['f'] == keys or [] == keys:
        path = args['f'][0] if keys else 'SUGE.json'
        obj = json.load(open(path))
        num = obj['num']
        position = [Vec2D(obj['px'][i], obj['py'][i]) for i in range(num)]
        velocity = [Vec2D(obj['vx'][i], obj['vy'][i]) for i in range(num)]
        gravity = get(obj, num, 'g')
        radii = get(obj, num, 'r', [0.3] * num)
        color = get(obj, num, 'c')
        simulate_acc = get(obj, num, 'sac', 0.001, False)
        display_freq = get(obj, num, 'dfq', 1000, False, int)
        background_color = get(obj, num, 'bg', 'black', False)
    else:
        obj = args
        print(obj)
        num = int(args['-num'][0])
        position = [Vec2D(float(obj['-px'][i]),
                          float(obj['-py'][i])) for i in range(num)]
        velocity = [Vec2D(float(obj['-vx'][i]),
                          float(obj['-vy'][i])) for i in range(num)]
        gravity = get2(args, num, '-g', hasAlias = True)
        radii = get2(args, num, '-r', [0.3] * num, hasAlias = True)
        color = get2(args, num, '-c', cls = str, hasAlias = True)
        simulate_acc = get2(args, num, '-sac', 0.001, False)
        display_freq = get2(args, num, '-dfq', 1000, False)
        background_color = get2(args, num, '-bg', 'black', False, str)
    gravity_system = Gravity_system(simulate_acc, display_freq, background_color)
    for i in range(num):
        gravity_system.add_star(Star(position[i], velocity[i],
                                     gravity[i], radii[i], color[i]))
    while True:
        gravity_system.simulate()
if __name__ == '__main__':
    try:
        main()
    except TclError:
        print('Simulator closed successfully by user.')
