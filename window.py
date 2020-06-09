# -*- coding: utf-8 -*-

import tkinter as tk
import tkinter.font as tkfont
import tkinter.messagebox as msgbox

from math import cos, pi

from PIL import Image, ImageDraw, ImageTk

import game

class window:
    SIZE_X = 600
    SIZE_Y = 700
    IM_X = 600
    IM_Y = 600
    REFRESH = 25
    def __init__(self):
        self.root = tk.Toplevel()
        self.root.title('Simulater')
        #self.root.resizable(0, 0)
        
        self.game = game.base_game()
        
        font = tkfont.Font(self.root, size=-18, weight=tkfont.BOLD)
        self.canvas = tk.Canvas(self.root, width=window.SIZE_X, height=window.SIZE_Y, bd=0, bg='black')
        self.canvas.pack(side=tk.LEFT)
        self.root.bind('<KeyPress>', self.on_key)
        self.im = Image.new('RGB', (self.IM_X, self.IM_Y+50), (10, 10, 10))
        self.imd = ImageDraw.Draw(self.im)
        tkimg = ImageTk.PhotoImage(self.im)
        self._label = tk.Label(self.root, image=tkimg)
        self._label.image = tkimg #hack a refrance to make python2.7 happy
        self._image = self.canvas.create_image(self.IM_X//2, self.IM_Y//2, image=tkimg)
        self.time = 0
        self.score = 0
        #self.time_id = self.canvas.create_text((self.SIZE_X-100, self.IM_Y+20), text = '%4ds %3dms' % (self.time//1000, self.time%1000), fill='green', font=font)
        self.drawing = False
        self.draw()
        self.root.mainloop()
        
    def draw(self):
        self.canvas.after(window.REFRESH, self.draw)
        if self.drawing:
            print('jammed at T+%d' % self.game.time)
            return
        self.drawing = True
        
        try:
            self.game.update()
        except game.FailedException:
            msgbox.showinfo("Game Over", "Your score is %d" % self.score)
            
        self.imd.rectangle((0, 0, self.IM_X, self.IM_Y), fill=(0,0,0))
        
        for y in range(game.HEIGHT+1):
            for x in range(1, game.WIDTH+1):
                b = self.game.family(x, y)
                color, fpos = b.appearance
                self.imd.rectangle(fpos(x*32, window.IM_Y-y*32), color)
        
        for y in range(game.MAX_ENERGY):
            b = self.game.energy_bar[y]
            color, fpos = b.appearance
            self.imd.rectangle(fpos(game.WIDTH*32+64, window.IM_Y-y*32), color)
            
        tkimg = ImageTk.PhotoImage(self.im)
        self._label = tk.Label(self.root, image=tkimg)
        self._label.image = tkimg
        self.canvas.itemconfig(self._image, image=tkimg)
        
        self.drawing = False
        
    def on_key(self, event):
        if event.keycode == 37:
            self.game.move_cursor_left()
        elif event.keycode == 39:
            self.game.move_cursor_right()
        elif event.keycode == 38:
            self.game.use_energy(1)

if __name__ == '__main__':
    window()
