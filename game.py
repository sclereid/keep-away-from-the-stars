# -*- coding: utf-8 -*-

from random import random
from math import cos, pi
from functools import lru_cache, partial

WIDTH = 10
HEIGHT = 16
MAX_TMP = 40
TMP_1 = 26
BLOCK_SIZE_H = 15
MAX_ENERGY = 10

class FailedException(BaseException):
    pass

class InsufficientEnergyException(BaseException):
    def __init__(self, e):
        self.e = e

const = lambda x: lambda *y, **k: x

def tic_orange(self, **kw):
    self.tmp = self.tmp - 1
    if self.tmp == TMP_1:
        if not self.is_bottom:
            if self.down.color == block.RED:
                self.down.tmp2 = block.ORANGE
            elif self.down.color == block.WHITE:
                self.down.color = block.ORANGE
                self.down.tmp   = MAX_TMP
    elif self.tmp == 0:
        self.color = block.WHITE

def tic_blue(self, **kw):
    if self.tmp < MAX_TMP:
        if kw['time'] % 4 == 0:
            self.tmp = self.tmp + 1
    elif not self.is_top:
        if self.up.color == block.BLUE_FALLING:
            #if self.up.tmp < self.up.tmp2:
            #    if kw['time'] % 4 == 0:
            #        self.up.tmp2 = self.up.tmp2 + 1
            #else:
            self.up.color = block.BLUE
            self.up.tmp2 = 0
            self.color = block.BLUE_STATIC
        elif self.up.color == block.WHITE:
            self.up.color = block.BLUE
            self.color = block.BLUE_STATIC
    else:
        self.tmp = MAX_TMP

def tic_blue_falling(self, **kw):
    if not (self.down.color == block.BLUE and self.tmp <= self.tmp2):
        self.tmp = self.tmp - 1
    if self.tmp <= 0:
        self.tmp = self.tmp2 = 0
        self.color = block.WHITE
    if self.tmp < TMP_1 and self.down.color == block.WHITE:
        self.down.color = block.BLUE_FALLING
        self.down.tmp = MAX_TMP
        self.down.tmp2  = self.tmp2

def tic_shining(self, **kw):
    if self.tmp > 0:
        if kw['time'] % 2 == 0:
            self.tmp = self.tmp - 1
    else:
        self.color = self.tmp2

def tic_blue_transiting(self, **kw):
    if self.tmp2 > 0:
        if kw['time'] % 2 == 0:
            self.tmp2 = self.tmp2 - 1
    else:
        self.tmp2 = self.tmp
        self.color = block.BLUE_FALLING

def tic_green(self, **kw):
    self.tmp = self.tmp - 1
    if self.tmp == TMP_1:
        if not self.is_top:
            if self.up.color == block.WHITE:
                self.up.color = block.GREEN
                self.up.tmp   = MAX_TMP
            else:
                self.color = block.GREEN_FADING
                self.tmp = MAX_TMP
    elif self.tmp == 0:
        self.color = block.WHITE
        
def tic_green_fading(self, **kw):
    if kw['time'] % 3 == 0:
        self.tmp = self.tmp - 1
    if self.tmp == 0:
        self.color = block.WHITE
        
def tic_yellow(self, **kw):
    self.tmp = self.tmp - 1
    if self.tmp == TMP_1:
        if not (self.is_top or self.up.color == block.BISTRE):
            self.up.color = block.YELLOW
            self.up.tmp   = MAX_TMP
    elif self.tmp == 0:
        self.color = block.WHITE

def tic_bistre(self, **kw):
    self.tmp = self.tmp - 1
    if self.tmp == TMP_1:
        if not self.is_bottom:
            if self.down.color == block.RED:
                self.down.tmp2 = block.BISTRE
            elif True:
                self.down.color = block.BISTRE
                self.down.tmp   = MAX_TMP
    elif self.tmp == 0:
        self.color = block.WHITE 

def tic_grey(self, **kw):
    self.tmp = self.tmp - 1
    if self.tmp == 0:
        self.color = block.WHITE

def tic_red(self, **kw):
    if self.tmp2 != block.WHITE:
        self.tmp = self.tmp - 1
        if self.tmp == 0:
            raise FailedException

def tic_brass(self, **kw):
    if not self.is_top and self.up.color == block.WHITE:
        self.up.color = block.BRASS
        self.up.tmp = self.tmp
        #self.color = block.WHITE
        #self.tmp = 0
    else:
        self.tmp = self.tmp - 1
        if self.tmp == 0:
            self.color = block.WHITE

tic_white = tic_blue_static = const(None)

tic_functions = [tic_white, tic_red, tic_orange, tic_blue, tic_blue_static,
                 tic_blue_falling, tic_shining, tic_blue_transiting, tic_green,
                 tic_green_fading, tic_yellow, tic_bistre, tic_grey, tic_brass]

@lru_cache()
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

@lru_cache()
def transiting_block(color_0, color_max, tmp):
    r0, g0, b0 = color_0
    rm, gm, bm = color_max
    m = tmp/MAX_TMP
    l = 1.0 - m
    return static_block((round(l*r0+m*rm), round(l*g0+m*gm), round(l*b0+m*bm)))

colors = [(128,128,128), (255,165,0)]

apr_red = lambda self: vertically_flipped_block((255,10,10), block.flippable_color_list[self.tmp2], self.tmp)

apr_white = const(static_block((128,128,128)))

apr_orange = lambda self: vertically_flipped_block((255,165,0),(128,128,128), self.tmp)

apr_blue = apr_blue_falling = apr_blue_transiting = lambda self: \
    vertically_flipped_block((64,64,255), (128,128,128), self.tmp/2)

apr_blue_static = const(static_block((10,10,255)))

apr_shining = lambda self: static_block([(255,255,255),(64,64,64)][self.tmp%2])

apr_green = lambda self: vertically_flipped_block((0,102,0), (128,128,128), self.tmp)

apr_green_fading = lambda self: transiting_block((128,128,128), (0,102,0), self.tmp)

apr_yellow = lambda self: vertically_flipped_block((255,255,0), (128,128,128), self.tmp)

apr_bistre = lambda self: vertically_flipped_block((61,43,31),(128,128,128), self.tmp)

apr_grey = lambda self: vertically_flipped_block((64,64,64), (128,128,128), self.tmp)

apr_brass = lambda self: transiting_block((128,128,128), (205,149,117), self.tmp*2)

apr_functions = [apr_white, apr_red, apr_orange, apr_blue, apr_blue_static,
                 apr_blue_falling, apr_shining, apr_blue_transiting, apr_green,
                 apr_green_fading, apr_yellow, apr_bistre, apr_grey, apr_brass]


class block:
    WHITE = 0
    RED = 1
    ORANGE = 2
    BLUE = 3
    BLUE_STATIC = 4
    BLUE_FALLING = 5
    SHINING = 6
    BLUE_TRANSITING = 7
    GREEN = 8
    GREEN_FADING = 9
    YELLOW = 10
    BISTRE = 11
    GREY = 12
    BRASS = 13
    
    flippable_color_list = {WHITE:(128,128,128), ORANGE:(255,165,0), BISTRE:(61,43,31)}
    
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
        
    def tic(self, t):
        self.tic_function(self, time=t)
        
    @property
    def appearance(self):
        return self.rep_function(self)

class base_game:
    LEVEL = 1
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
        self.cursor.tmp = MAX_TMP // 2
        
        self.energy_bar = [block() for x in range(MAX_ENERGY)]
        for i in range(MAX_ENERGY):
            b = self.energy_bar[i]
            b.is_bottom = i == 0
            b.is_top    = i == MAX_ENERGY-1
            b.up   = b.is_top    or self.energy_bar[i+1]
            b.down = b.is_bottom or self.energy_bar[i-1] 
        self.energy_bar[0].color = block.BLUE
        self.time= 0
    
    def update(self, scorecallback=const(None)):
        self.time = self.time + 1
        for s in self.blocks:
            for t in s:
                t.tic(self.time)
        for u in self.energy_bar:
            u.tic(self.time)
        if self.time % (MAX_TMP//4) == 0:
            scorecallback(1)
        if self.time % MAX_TMP == 0:
            for x in range(1, WIDTH+1):
                b = self.family(x, HEIGHT)
                if b.color == block.WHITE:
                    if random() < 2/7:
                        b.color = block.ORANGE
                        b.tmp = MAX_TMP
                    elif random() < 1/20:
                        b.color = block.BISTRE
                        b.tmp = MAX_TMP
        
    def move_cursor_left(self, failcallback=lambda:print('Cannot move left')):
        if not self.cursor.is_far_left \
            and self.cursor.left.color == self.cursor.tmp2 == block.WHITE:
            self.cursor.color = block.WHITE
            self.cursor.tmp = 0
            self.cursor = self.cursor.left
            self.cursor.color = block.RED
            self.cursor.tmp = MAX_TMP // 2
            self.cursor.tmp2 = block.WHITE
        else:
            failcallback()
        
    def move_cursor_right(self, failcallback=lambda:print('Cannot move right')):
        if not self.cursor.is_far_right \
            and self.cursor.right.color == self.cursor.tmp2 == block.WHITE:
            self.cursor.color = block.WHITE
            self.cursor.tmp = 0
            self.cursor = self.cursor.right
            self.cursor.color = block.RED
            self.cursor.tmp = MAX_TMP // 2
            self.cursor.tmp2 = block.WHITE
        else:
            failcallback()
        
    def use_energy(self, n):
        try:
            e = [b.color for b in self.energy_bar].index(block.BLUE)
        except ValueError:
            raise InsufficientEnergyException(-1)
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
            raise InsufficientEnergyException(e)
    
    def powerup_mono(self, scorecallback=partial(print, "Increase score by"), failcallback=lambda:"energy is insufficient"):
        try:
            self.use_energy(2)
            self.cursor.up.color = block.GREEN
            self.cursor.up.tmp = MAX_TMP
            scorecallback(25)
        except InsufficientEnergyException:
            try:
                self.use_energy(1)
                self.cursor.up.color = block.BRASS
                self.cursor.up.tmp = MAX_TMP // 2
            except InsufficientEnergyException:
                failcallback()
            
    def powerup_line(self, scorecallback=partial(print, "Increase score by"), failcallback=lambda:"energy is insufficient"):
        try:
            self.use_energy(3)
            self.cursor.up.color = block.YELLOW
            self.cursor.up.tmp = MAX_TMP
            scorecallback(50)
        except InsufficientEnergyException:
            failcallback()
        
    def powerup_ninja(self, scorecallback=partial(print, "Increase score by"), failcallback=lambda:"energy is insufficient"):
        try:
            self.use_energy(4)
            for y in range(HEIGHT+1):
                for x in range(1, WIDTH+1):
                    b = self.family(x, y)
                    if b.color == block.ORANGE:
                        b.color = block.GREY
            scorecallback(70)
        except InsufficientEnergyException as isee:
            if isee.e == -1:
                k = [b.color for b in self.energy_bar].index(block.SHINING)
                if k+4 < MAX_ENERGY and self.energy_bar[k+3].color == block.SHINING:
                    self.energy_bar[k].tmp += MAX_TMP
                    for y in range(HEIGHT+1):
                        for x in range(1, WIDTH+1):
                            b = self.family(x, y)
                            if b.color == block.BISTRE:
                                b.color = block.ORANGE
                            elif b.color == block.ORANGE:
                                b.color = block.GREY
            else:
                failcallback()
        
    def __repr__(self):
        """
        game.__repr__()
        This method is mainly designed for testing
        """
        CLIST = ['W ', 'R ', 'O ', 'B+', 'B=', 'B-', 'S^', 'B^', 'G ', 'G-',
                 'Y ', 'BI', 'GR', 'BR']
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

class derived_game(base_game):
    def __init__(self, g):
        #for attr in ['blocks', 'family', 'cursor', 'energy_bar', 'time']:
        #    exec("self.%s = g.%s" % (attr, attr))
        for k in vars(g):
            self.__setattr__(k, g.__getattribute__(k))
        for y in range(HEIGHT+1):
            for x in range(1, WIDTH+1):
                b = self.family(x, y)
                if not (b.color == block.WHITE or b.color == block.RED):
                    b.color = block.GREY
                    b.tmp2 = 0

class lv2_game(derived_game):
    LEVEL = 2    
    def update(self, scorecallback=const(None)):
        self.time = self.time + 1
        for s in self.blocks:
            for t in s:
                t.tic(self.time)
        for u in self.energy_bar:
            u.tic(self.time)
        if self.time % (MAX_TMP//3) == 0:
            scorecallback(1)
        if self.time % MAX_TMP == 0:
            for x in range(1, WIDTH+1):
                b = self.family(x, HEIGHT)
                if b.color == block.WHITE:
                    if random() < 3/7:
                        b.color = block.ORANGE
                        b.tmp = MAX_TMP
                    elif random() < 1/15:
                        b.color = block.BISTRE
                        b.tmp = MAX_TMP

class lv3_game(derived_game):
    LEVEL = 23
    def update(self, scorecallback=const(None)):
        base_game.update(self, scorecallback)
        base_game.update(self, scorecallback)

class lv4_game(derived_game):
    LEVEL = 23
    def update(self, scorecallback=const(None)):
        lv2_game.update(self, scorecallback)
        lv2_game.update(self, scorecallback)

if __name__ == '__main__':
    g = base_game()
    step = lambda n=1 : const(g)([g.update() for i in range(n)])
    ml = lambda: const(g)(g.move_cursor_left())
    mr = lambda: const(g)(g.move_cursor_right())
    use = lambda n : const(g)(g.use_energy(n))
    