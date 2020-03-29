# -*- coding: utf-8 -*-

from random import random


WIDTH = 10
HEIGHT = 16
MAX_TMP = 20

class FailedException(BaseException):
    pass

tic_white = lambda *_:None

def tic_orange(self, family):
    self.tmp = self.tmp - 1
    if self.tmp == 0:
        self.color = block.WHITE
        if not self.is_bottom:
            block_down = family(*self.id_down)
            if block_down.is_cursor:
                raise FailedException
            else:
                block_down.color = block.ORANGE
                block_down.tmp   = MAX_TMP

tic_functions = [tic_white, tic_orange]
colors = [(128,128,128), (255,165,0)]

class block:
    WHITE = 0
    ORANGE = 1
    
    @property
    def color(self):
        return self._color
    
    @color.setter
    def color(self, value):
        self._color = value
        self.tic_function = tic_functions[value]
    
    def __init__(self):
        self.color = block.WHITE
        self.tmp   = 0
        self.is_cursor = False
        
    def tic(self, family):
        self.tic_function(self, family)
                
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
                
                b.id_left  = b.is_far_left  or (x-1, y)
                b.id_right = b.is_far_right or (x+1, y)
                b.id_up    = b.is_top       or (x, y+1)
                b.id_down  = b.is_bottom    or (x, y-1)
        self.cursor = (4, 0)
        self.family(*self.cursor).is_cursor = True
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
        if not self.family(*self.cursor).is_far_left:
            self.family(*self.cursor).is_cursor = False
            x, y = self.cursor
            self.cursor = x-1, y
            self.family(*self.cursor).is_cursor = True
        
    def move_cursor_right(self):
        if not self.family(*self.cursor).is_far_right:
            self.family(*self.cursor).is_cursor = False
            x, y = self.cursor
            self.cursor = x+1, y
            self.family(*self.cursor).is_cursor = True
        
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
                s = s + "%c%2d%c| "%("WO???"[b.color], b.tmp, " ^"[b.is_cursor])
            s = s + '\n'
        return s
            
