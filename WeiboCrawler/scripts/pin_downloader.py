#!/usr/bin/env python
#coding=utf8

import urllib2
import cStringIO
from PIL import Image
from WeiboCrawler.captcha.solver import CaptchaSolver
from skimage import io
import matplotlib.pyplot as plt

class Cursor:
    def __init__(self, ax):
        self.ax = ax
        self.ly = ax.axvline(color='k')  # the vert line

    def mouse_move(self, event):
        if not event.inaxes: return

        x, y = event.xdata, event.ydata
        # update the line positions
        self.ly.set_xdata(x )
        plt.draw()

def download(i):
    url="http://login.sina.com.cn/cgi/pin.php?s=02271679&p=xd-e174b0d9f37780767be2f700faf79bfac60d"
    #download the pin image
    file = cStringIO.StringIO(urllib2.urlopen(url).read())
    img = Image.open(file)
    img.save('../pics/'+str(i)+'.png')

def preprocess(i):
    img = io.imread('../pics/'+str(i)+'.png')
    solver=CaptchaSolver()
    grey_img=solver.preprocess(img)
    io.imsave('../grey/'+str(i)+'.png',grey_img)
    print(grey_img.shape)
    fig, ax = plt.subplots()
    cursor = Cursor(ax)
    #cursor = SnaptoCursor(ax, t, s)
    plt.connect('motion_notify_event', cursor.mouse_move)
    plt.imshow(grey_img,cmap=plt.cm.gray)

    def onclick(event):
        f=open('split.txt','a')
        print(event.xdata)
        f.write(str(i)+'\t'+str(event.xdata)+'\n')
        f.close()
        plt.close()
    cid = fig.canvas.mpl_connect('button_press_event', onclick)
    plt.show()

if __name__ == '__main__':
    for i in range(1000,1050):
        download(i)
        preprocess(i)