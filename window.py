# -*- coding: utf-8 -*-

import tkinter as tk
import tkinter.font as tkfont
import tkinter.messagebox as msgbox

#from math import cos, pi

#from PIL import Image, ImageDraw, ImageTk

import game

def color_num(rgb):
    return '#%02x%02x%02x' % rgb

class window:
    SIZE_X = 600
    SIZE_Y = 700
    IM_X = 600
    IM_Y = 600
    REFRESH = 25
    def __init__(self):
        self.root = tk.Tk()#tk.Toplevel()
        self.root.title('Simulater')
        #self.root.resizable(0, 0)
        
        self.game = game.base_game()
        
        font = tkfont.Font(self.root, size=18, weight=tkfont.BOLD)
        self.canvas = tk.Canvas(self.root, width=window.SIZE_X, height=window.SIZE_Y, bd=0, bg='black')
        self.canvas.pack(side=tk.LEFT)
        self.root.bind('<KeyPress>', self.on_key)
        self.rects_id = [self.canvas.create_rectangle(0,0,0,0) for _
                         in range((game.HEIGHT+1)*game.WIDTH + game.MAX_ENERGY)]
        self.score_text_id = self.canvas.create_text(370, 200, text="SCORE", font=font, fill="#233333", anchor=tk.W)
        self.score_id = self.canvas.create_text(370, 230, text="", font=font, fill="#233333", anchor=tk.W)
        self.level_id = self.canvas.create_text(370, 160, text="LEVEL 1", font=font, fill="#233388", anchor=tk.W)
        #self.im = Image.new('RGB', (self.IM_X, self.IM_Y+50), (10, 10, 10))
        #self.imd = ImageDraw.Draw(self.im)
        #tkimg = ImageTk.PhotoImage(self.im)
        #self._label = tk.Label(self.root, image=tkimg)
        #self._label.image = tkimg #hack a refrance to make python2.7 happy
        #self._image = self.canvas.create_image(self.IM_X//2, self.IM_Y//2, image=tkimg)
        self.time = 0
        self.score = 0
        self.score_blink_tmp = 0
        def add_score(n):
            self.score = self.score + n
            if n >= 10:
                self.score_blink_tmp += 16
        self.add_score = add_score
        self.paused = False
        #self.time_id = self.canvas.create_text((self.SIZE_X-100, self.IM_Y+20), text = '%4ds %3dms' % (self.time//1000, self.time%1000), fill='green', font=font)
        self.drawing = False
        self.draw()
        self.root.mainloop()
        
    def draw(self):
        self.canvas.after(window.REFRESH, self.draw)
        if self.drawing:
            #print('jammed at T+%d' % self.game.time)
            return
        self.drawing = True
        
        if self.game.time == 500:
            self.game = game.lv2_game(self.game)
            self.canvas.itemconfig(self.level_id, text="LEVEL 2", fill='#23cc88')
            self.add_score(100)
        elif self.game.time == 1000:
            self.game = game.lv3_game(self.game)
            self.canvas.itemconfig(self.level_id, text="LEVEL 3", fill='#23cccc')
            self.add_score(100)
        elif self.game.time == 1500:
            self.game = game.lv4_game(self.game)
            self.canvas.itemconfig(self.level_id, text="LEVEL 4", fill='#ffcccc')
            self.add_score(100)
        
        try:
            self.game.update(scorecallback=self.add_score)
        except game.FailedException:
            msgbox.showinfo("Game Over", "Your score is %d" % self.score)
            
        #self.imd.rectangle((0, 0, self.IM_X, self.IM_Y), fill=(0,0,0))
        self.canvas.itemconfig(self.score_id, text="%d" % self.score, fill=['#233333', '#ffaaaa'][(self.score_blink_tmp//4) % 2])
        if self.score_blink_tmp > 0:
            self.score_blink_tmp = self.score_blink_tmp - 1
        
        i = 0
        
        for y in range(game.HEIGHT+1):
            for x in range(1, game.WIDTH+1):
                b = self.game.family(x, y)
                color, fpos = b.appearance
                self.canvas.coords(self.rects_id[i], fpos(x*32, window.IM_Y-y*32))
                self.canvas.itemconfig(self.rects_id[i], fill=color_num(color))
                i = i + 1
                #self.imd.rectangle(fpos(x*32, window.IM_Y-y*32), color)
        
        for y in range(game.MAX_ENERGY):
            b = self.game.energy_bar[y]
            color, fpos = b.appearance
            self.canvas.coords(self.rects_id[i], fpos(game.WIDTH*32+64, window.IM_Y-y*32))
            self.canvas.itemconfig(self.rects_id[i], fill=color_num(color))
            i = i + 1
            #self.imd.rectangle(fpos(game.WIDTH*32+64, window.IM_Y-y*32), color)
            
        #tkimg = ImageTk.PhotoImage(self.im)
        #self._label = tk.Label(self.root, image=tkimg)
        #self._label.image = tkimg
        #self.canvas.itemconfig(self._image, image=tkimg)
        
        self.drawing = False
        
    def on_key(self, event):
        if event.keycode == 37:
            self.game.move_cursor_left()
        elif event.keycode == 38:
            self.game.powerup_line(scorecallback=self.add_score)
        elif event.keycode == 39:
            self.game.move_cursor_right()
        elif event.keycode == 40:
            self.game.powerup_mono(scorecallback=self.add_score)
        elif event.keycode == 32:
            self.game.powerup_ninja(scorecallback=self.add_score)
        else:
            print(event.keycode)

if __name__ == '__main__':
    w = window()
