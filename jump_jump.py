#!/usr/bin/env python
# -*- coding: utf-8 -*-


import math
import os
from PIL import Image, ImageTk
import random
import time
import Tkinter


def get_screen():
    cmd = 'adb shell screencap -p /sdcard/img_tmp/tmp.png'
    os.system(cmd)
    cmd = 'adb pull /sdcard/img_tmp/tmp.png .'
    os.system(cmd)

    image = Image.open('./tmp.png')
    image.thumbnail((540, 960), Image.ANTIALIAS)
    return image


def jump(t):
    # random press position
    pos_x = random.randint(0, 9) * 10 + 320
    pos_y = random.randint(0, 9) * 10 + 410
    cmd = 'adb shell input swipe %d %d %d %d %d' % (pos_x,
                                                    pos_y,
                                                    pos_x,
                                                    pos_y,
                                                    t)

    print cmd
    os.system(cmd)

    time.sleep(1)


def compute_time(dist):
    return dist* 1.392


def compute_dist(pos_1, pos_2):
    return math.sqrt( (pos_2[0] - pos_1[0])**2 + (pos_2[1] - pos_1[1])**2 )


GET_SELF = 1
GET_GOAL = 2

class MainWindow():

    def __init__(self, main):

        # canvas for image
        self.canvas_ = Tkinter.Canvas(main, width=540, height=960)
        self.canvas_.pack()

        image = get_screen()
        self.image_tk_ = ImageTk.PhotoImage(image)
        self.image_on_canvas_ = self.canvas_.create_image(image.size[0]//2,
                                                          image.size[1]//2,
                                                          image=self.image_tk_)

        #mouseclick event
        self.canvas_.bind("<Button 1>", self.click_handle)

        self.status_ = GET_SELF
        self.pos_ = (0, 0)

    def refresh_image(self, image):
        self.image_tk_ = ImageTk.PhotoImage(image)
        self.canvas_.itemconfig(self.image_on_canvas_, image=self.image_tk_)

    def click_handle(self, event):
        if self.status_ == GET_SELF:
            self.pos_ = (event.x, event.y)
            self.status_ = GET_GOAL
        elif self.status_ == GET_GOAL:
            goal_pos = (event.x, event.y)
            dist = 2 * compute_dist(self.pos_, goal_pos)
            print dist

            jump(compute_time(dist))
            image = get_screen()

            self.refresh_image(image)
            self.status_ = GET_SELF

#----------------------------------------------------------------------

if __name__ == "__main__":
    root = Tkinter.Tk()
    MainWindow(root)
    root.mainloop()
