# -*- coding: utf-8 -*-

from random import random
from math import cos, pi

WIDTH = 10
HEIGHT = 16
MAX_TMP = 40
TMP_1 = 26
BLOCK_SIZE_H = 15
MAX_ENERGY = 10

class FailedException(BaseException):
    pass

const = lambda x: lambda *y: x

def tic_orange(self, time):
    self.tmp = self.tmp - 1
    if self.tmp == TMP_1:
        if not self.is_bottom:
            if self.down.color == block.RED:
                raise FailedException
            else:
                self.down.color = block.ORANGE
                self.down.tmp   = MAX_TMP
    elif self.tmp == 0:
        self.color = block.WHITE

def tic_blue(self, time):
    if self.tmp < MAX_TMP:
        if time % 4 == 0:
            self.tmp = self.tmp + 1
    elif not self.is_top:
        if self.up.color == block.BLUE_FALLING:
            if self.up.tmp < self.up.tmp2:
                if time % 4 == 0:
                    self.up.tmp2 = self.up.tmp2 + 1
            else:
                self.up.color = block.BLUE
                self.up.tmp2 = 0
                self.color = block.BLUE_STATIC
        elif self.up.color == block.WHITE:
            self.up.color = block.BLUE
            self.color = block.BLUE_STATIC
    else:
        self.tmp = MAX_TMP

def tic_blue_falling(self, time):
    if not (self.down.color == block.BLUE and self.tmp <= self.tmp2):
        self.tmp = self.tmp - 1
    if self.tmp <= 0:
        self.tmp = self.tmp2 = 0
        self.color = block.WHITE
    if self.tmp < TMP_1 and self.down.color == block.WHITE:
        self.down.color = block.BLUE_FALLING
        self.down.tmp = MAX_TMP
        self.down.tmp2  = self.tmp2

def tic_shining(self, time):
    if self.tmp > 0:
        if time % 2 == 0:
            self.tmp = self.tmp - 1
    else:
        self.color = self.tmp2

def tic_blue_transiting(self, time):
    if self.tmp2 > 0:
        if time % 2 == 0:
            self.tmp2 = self.tmp2 - 1
    else:
        self.tmp2 = self.tmp
        self.color = block.BLUE_FALLING

tic_white = tic_red = tic_blue_static = const(None)

tic_functions = [tic_white, tic_red, tic_orange, tic_blue, tic_blue_static,
                 tic_blue_falling, tic_shining, tic_blue_transiting]

def vertically_flipped_block(color, front, tmp):
    h0 = BLOCK_SIZE_H*cos(tmp/MAX_TMP*2*pi)
    if h0 >= 0:
        c = front
        h = h0
    else:
        c = color
        h = -h0
    return c, lambda x, y: (x - BLOCK_SIZE_H, y - h, x + BLOCK_SIZE_H, y + h)

static_block = lambda color: (color, lambda x, y:(x-BLOCK_SIZE_H, y-BLOCK_SIZE_H, x+BLOCK_SIZE_H, y+BLOCK_SIZE_H))

colors = [(128,128,128), (255,165,0)]

apr_red = const(static_block((255, 10, 10)))

apr_white = const(static_block((128,128,128)))

apr_orange = lambda self: vertically_flipped_block((255,165,0),(128,128,128),
                                                   self.tmp)

apr_blue = apr_blue_falling = apr_blue_transiting = lambda self: \
    vertically_flipped_block((64,64,255), (128,128,128), self.tmp)

apr_blue_static = const(static_block((10,10,255)))

apr_shining = lambda self: static_block([(255,255,255),(64,64,64)][self.tmp%2])

apr_functions = [apr_white, apr_red, apr_orange, apr_blue, apr_blue_static,
                 apr_blue_falling, apr_shining, apr_blue_transiting]

class block:
    WHITE = 0
    RED = 1
    ORANGE = 2
    BLUE = 3
    BLUE_STATIC = 4
    BLUE_FALLING = 5
    SHINING = 6
    BLUE_TRANSITING = 7
    
    @property
    def color(self):
        return self._color
    
    @color.setter
    def color(self, value):
        self._color = value
        self.tic_function = tic_functions[value]
        self.rep_function = apr_functions[value]
    
    def __init__(self):
        self.color = block.WHITE
        self.tmp   = 0
        self.tmp2  = 0
        
    def tic(self, time):
        self.tic_function(self, time)
        
    @property
    def appearance(self):
        return self.rep_function(self)
    
class base_game:
    
    def __init__(self):
        self.blocks = [[block() for x in range(1, WIDTH+1)] for y in range(HEIGHT+1)]
        self.family = lambda x, y: self.blocks[y][x-1]
        for y in range(HEIGHT+1):
            for x in range(1, WIDTH+1):
                b = self.family(x, y)
                b.is_far_left  = x == 1
                b.is_far_right = x == WIDTH
                b.is_bottom    = y == 0
                b.is_top       = y == HEIGHT
                
                b.left  = b.is_far_left  or self.family(x-1, y)
                b.right = b.is_far_right or self.family(x+1, y)
                b.up    = b.is_top       or self.family(x, y+1)
                b.down  = b.is_bottom    or self.family(x, y-1)
        self.cursor = self.family(4, 0)
        self.cursor.color = block.RED
        self.cursor.tmp = MAX_TMP
        
        self.energy_bar = [block() for x in range(MAX_ENERGY)];
        for i in range(MAX_ENERGY):
            b = self.energy_bar[i]
            b.is_bottom = i == 0
            b.is_top    = i == MAX_ENERGY-1
            b.up   = b.is_top    or self.energy_bar[i+1]
            b.down = b.is_bottom or self.energy_bar[i-1] 
        self.energy_bar[0].color = block.BLUE
        self.time= 0
    
    def update(self):
        self.time = self.time + 1
        for s in self.blocks:
            for t in s:
                t.tic(self.time)
        for u in self.energy_bar:
            u.tic(self.time)
        if self.time % MAX_TMP == 0:
            for x in range(1, WIDTH+1):
                b = self.family(x, HEIGHT)
                if b.color == block.WHITE:
                    if random() < 1/7:
                        b.color = block.ORANGE
                        b.tmp = MAX_TMP
        
    def move_cursor_left(self):
        if not self.cursor.is_far_left:
            self.cursor.color = block.WHITE
            self.cursor.tmp = 0
            self.cursor = self.cursor.left
            self.cursor.color = block.RED
            self.cursor.tmp = MAX_TMP
        
    def move_cursor_right(self):
        if not self.cursor.is_far_right:
            self.cursor.color = block.WHITE
            self.cursor.tmp = 0
            self.cursor = self.cursor.right
            self.cursor.color = block.RED
            self.cursor.tmp = MAX_TMP
        
    def use_energy(self, n):
        e = [b.color for b in self.energy_bar].index(block.BLUE)
        if e >= n:
            self.energy_bar[e-n].color = block.SHINING
            self.energy_bar[e-n].tmp = 5
            self.energy_bar[e-n].tmp2 = block.BLUE
            for b in self.energy_bar[e-n+1:e]:
                b.color = block.SHINING
                b.tmp = 5
                b.tmp2 = block.WHITE
            self.energy_bar[e].color = block.BLUE_TRANSITING
            self.energy_bar[e].tmp2 = 5
        else:
            print('current energy (', e, '/', MAX_ENERGY, ') is insufficient')
        
    def __repr__(self):
        """
        game.__repr__()
        This method is mainly designed for testing
        """
        CLIST = ['W ', 'R ', 'O ', 'B+', 'B=', 'B-', 'S^', 'B^']
        s = "game object at time %d\n" % self.time 
        s = s + '-'*61 + '\n'
        for y in range(HEIGHT+1):
            s = s + '| '
            for x in range(1, WIDTH+1):
                b = self.family(x, y)
                s = s + "%s%2d| "%(CLIST[b.color], b.tmp)
            if y < MAX_ENERGY:
                b = self.energy_bar[y]
                s = s + ' '*4
                s = s + '|%s%2d %2d|'%(CLIST[b.color], b.tmp, b.tmp2)
            s = s + '\n'
        return s
            
if __name__ == '__main__':
    g = base_game()
    step = lambda n : const(g)([g.update() for i in range(n)])
    ml = lambda: const(g)(g.move_cursor_left())
    mr = lambda: const(g)(g.move_cursor_right())
    use = lambda n : const(g)(g.use_energy(n))
    