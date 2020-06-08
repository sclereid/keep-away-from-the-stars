# -*- coding: utf-8 -*-

from random import random
from math import cos, pi

WIDTH = 10
HEIGHT = 16
MAX_TMP = 40
BLOCK_SIZE_H = 15

class FailedException(BaseException):
    pass

tic_white = tic_red = lambda *_:None

def tic_orange(self, family):
    self.tmp = self.tmp - 1
    if self.tmp == MAX_TMP//3*2:
        if not self.is_bottom:
            if self.down.color == block.RED:
                raise FailedException
            else:
                self.down.color = block.ORANGE
                self.down.tmp   = MAX_TMP
    elif self.tmp == 0:
        self.color = block.WHITE

tic_functions = [tic_white, tic_red, tic_orange]

def vertically_flipped_block(color, front, tmp):
    h0 = BLOCK_SIZE_H*cos(tmp/MAX_TMP*2*pi)
    if h0 >= 0:
        c = front
        h = h0
    else:
        c = color
        h = -h0
    return c, lambda x, y: (x - BLOCK_SIZE_H, y - h, x + BLOCK_SIZE_H, y + h)

colors = [(128,128,128), (255,165,0)]

apr_red = lambda self: ((255,10,10),
    lambda x, y:(x-BLOCK_SIZE_H, y-BLOCK_SIZE_H, x+BLOCK_SIZE_H, y+BLOCK_SIZE_H))

apr_white = lambda self: ((128,128,128),
    lambda x, y:(x-BLOCK_SIZE_H, y-BLOCK_SIZE_H, x+BLOCK_SIZE_H, y+BLOCK_SIZE_H))

apr_orange = lambda self: vertically_flipped_block((255,165,0),(128,128,128),
                                                   self.tmp)

apr_functions = [apr_white, apr_red, apr_orange]

class block:
    WHITE = 0
    RED = 1
    ORANGE = 2
    
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
        
    def tic(self, family):
        self.tic_function(self, family)
        
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
        self.time= 0
    
    def update(self):
        self.time = self.time + 1
        for s in self.blocks:
            for t in s:
                t.tic(self.family)
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
        
    def __repr__(self):
        """
        game.__repr__()
        This method is mainly designed for testing
        """
        s = "game object at time %d\n" % self.time 
        s = s + '-'*61 + '\n'
        for y in range(HEIGHT+1):
            s = s + '| '
            for x in range(1, WIDTH+1):
                b = self.family(x, y)
                s = s + "%c%2d| "%("WRO??"[b.color], b.tmp)
            s = s + '\n'
        return s
            
if __name__ == '__main__':
    g = base_game()
    step = lambda n : ([g.update() for i in range(n)], g)[-1]
    