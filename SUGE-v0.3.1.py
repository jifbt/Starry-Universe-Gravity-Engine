'''
    SUG Engine v0.3.0
    SUGE.py [-v version] -n number -px position-x -py position-y
            -vx velocity-x -vy velocity-y [-g gravity|-gAll gravity]
            [-r radii<default:0.3>|-rAll radii] [-c color|-cAll color]
            [-sac simulate-accuracy<0.001>]
            [-dfq display-frequncy<1000>]
            [-bg background_color<black>]
    SUGE.py [-f file-path<"SUGE.cfg">] [-v version<"auto">]
            
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
import re
valid_version = ('0.1.0', '0.1.1', '0.2.2', '0.2.3')
trans = {7: '0.1.0', 9: '0.1.1', 10: '0.2.2', 11: '0.2.3'}
keys_map = {'0.1.0': ['-n', '-px', '-py', '-vx', '-vy', '-g', '-c'],
            '0.1.1': ['-n', '-px', '-py', '-vx', '-vy',
                      '-g', '-c', '-sac', '-dfq'],
            '0.2.2': ['-n', '-px', '-py', '-vx', '-vy',
                      '-g', '-r', '-c', '-sac', '-dfq'],
            '0.2.3': ['-n', '-px', '-py', '-vx', '-vy',
                      '-g', '-r', '-c', '-sac', '-dfq', '-bg']}
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
    def __init__(self, similate_acc, display_freq,
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
        self.num += 1
        self.stars.append(star)
    def remove_star(self, star_no):
        self.num -= 1
        return self.stars.pop(star_no)
    def simulate(self):
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
def subseq(*args):
    for i in range(len(args) - 1):
        if not all((j in args[i + 1] for j in args[i])):
            return False
        if not all((args[i + 1].index(args[i][j]) <
                    args[i + 1].index(args[i][j + 1])
                    for j in range(len(args[i]) - 1))):
            return False
    return True
def parse_args():
    args = {'' : []}
    lens = {'' : 0}
    keys = ['']
    tmp = ''
    for i in sys.argv[1:]:
        if i.startswith('-') and not i[1].isdigit():
            tmp = i
            args[i] = []
            lens[i] = 0
            keys.append(i)
        else:
            args[tmp].append(i)
            lens[tmp] += 1
    keys_ = keys.copy()
    for i in keys_:
        if lens[i] == 0:
            args.pop(i)
            lens.pop(i)
            keys.remove(i)
    return args, lens, keys
def main():
    args, lens, keys = parse_args()
    if ['--ver'] == keys:
        print(__doc__.splitlines()[1][4:])
        return 0
    elif ['--help'] == keys:
        print(__doc__)
        return 0
    elif subseq(['-n', '-px', '-py', '-vx', '-vy'], keys,
       ['-v', '-n', '-px', '-py', '-vx', '-vy', '-g', '-gAll', '-r',
        '-rAll', '-c', '-cAll', '-sac', '-dfq', '-bg']) and \
       ('-g' in keys) ^ ('-gAll' in keys) and not \
       (('-r' in keys) and ('-rAll' in keys)) and \
       ('-c' in keys) ^ ('-cAll' in keys):
        if lens['-n'] != 1 or lens.get('-v', 1) != 1:
            return 1
        num = int(args['-n'][0])
        version = args.get('-v', ['auto'])[0]
        has_version = 1 if '-v' in keys else 0
        count = len(keys) - has_version
        keys_ = keys.copy()
        if has_version:
            keys_.remove('-v')
        if version not in valid_version and version != 'auto':
            return 2
        for i, j in zip(('-gAll', '-rAll', '-cAll'), ('-g', '-r', '-c')):
            if i in keys:
                if lens[i] != 1:
                    return 2
                value = version
                keys.remove(i)
                keys.add(j)
                args.pop(i)
                args[j] = [value] * num
                lens.pop(i)
                lens[j] = num
        if 'auto' != version != trans[count]:
            return 2
        if version == 'auto':
            version = trans[count]
        print(repr(num))
        if keys_map[version] != keys_:
            return 2
        if lens['-px'] != num or lens['-py'] != num or \
           lens['-vx'] != num or lens['-vy'] != num or \
           lens['-g'] != num or lens.get('-r', num) != num or \
           lens['-c'] != num or lens.get('-sac', 1) != 1 or \
           lens.get('-dfq', 1) != 1 or lens.get('-bg', 1) != 1:
            return 1
        position = [Vec2D(float(args['-px'][i]), float(args['-py'][i]))
                    for i in range(num)]
        velocity = [Vec2D(float(args['-vx'][i]), float(args['-vy'][i]))
                    for i in range(num)]
        gravity = list(map(float, args['-g']))
        if version not in ('0.1.0', '0.1.1'):
            radii = list(map(float, args['-r']))
        else:
            radii = [0.3] * num
        color = args['-c']
        if version != '0.1.0':
            simulate_acc = float(args['-sac'][0])
            display_freq = int(args['-dfq'][0])
        else:
            simulate_acc = 0.001
            display_freq = 1000
        if version not in ('0.1.0', '0.1.1', '0.2.2'):
            background_color = args['-bg'][0]
        else:
            background_color = 'black'
    elif subseq(keys, ['-f', '-v']):
        if lens.get('-v', 1) != 1 or lens.get('-f', 1) != 1:
            return 1
        version = args.get('-v', ['auto'])[0]
        path = args.get('-f', ['SUGE.cfg'])[0]
        if version not in valid_version and version != 'auto':
            return 2
        with open(path) as file:
            f = file.readlines()
            l = len(f)
            offset = 0
            if ' ' in f[0]:
                ver_tmp = f[0].split()[1]
                if 'auto' != version != ver_tmp:
                    return 2
                if ver_tmp not in valid_version:
                    return 2
                version = ver_tmp if version == 'auto' else version
            if 'auto' != version != trans[l]:
                return 2
            version = trans[l] if version == 'auto' else version
            if version in ('0.1.0', '0.1.1'):
                offset -= 1
            for i in range(1, 6 if version in ('0.1.0', '0.1.1') else 7):
                f[i] = list(map(float, f[i].split()))
            num = int(f[0].split()[0])
            position = [Vec2D(f[1][i], f[2][i]) for i in range(num)]
            velocity = [Vec2D(f[3][i], f[4][i]) for i in range(num)]
            gravity = f[5]
            if version not in ('0.1.0', '0.1.1'):
                radii = f[6]
            else:
                radii = [0.3] * num
            color = f[7 + offset].split()
            if version != '0.1.0':
                simulate_acc = float(f[8 + offset])
                display_freq = int(f[9 + offset])
            else:
                simulate_acc = 0.001
                display_freq = 1000
            if version not in ('0.1.0', '0.1.1', '0.2.2'):
                background_color = f[10]
            else:
                background_color = 'black'
    else:
        return 1
    gravity_system = Gravity_system(simulate_acc, display_freq, background_color)
    for i in range(num):
        gravity_system.add_star(Star(position[i], velocity[i],
                                     gravity[i], radii[i], color[i]))
    while True:
        gravity_system.simulate()
if __name__ == '__main__':
    try:
        res = main()
        if isinstance(res, int):
            val, arg = res, ''
        elif isinstance(res, tuple):
            val, arg = res
        out = {'value': val, 'argument': arg}
        if val == 0:
            pass
        elif val == 1:
            print('Error: 1[invalid argumant]:', arg,
                  parse_args(), file = sys.stderr)
        elif val == 2:
            print('Error: 2[invalid version]:', arg, file = sys.stderr)
        else:
            print('Error:', out, file = sys.stderr)
    except TclError:
        print('Simulator closed successfully by user.')
    except Exception as exc:
        raise
