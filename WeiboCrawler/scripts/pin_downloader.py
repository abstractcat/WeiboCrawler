#!/usr/bin/env python
#coding=utf8

import urllib2
import cStringIO
from PIL import Image
from skimage.color import rgb2gray
from skimage import io
import matplotlib.pyplot as plt

def download(i):
    url="http://login.sina.com.cn/cgi/pin.php?s=02271679&p=xd-e174b0d9f37780767be2f700faf79bfac60d"
    #download the pin image
    file = cStringIO.StringIO(urllib2.urlopen(url).read())
    img = Image.open(file)
    img.save('../pics/'+str(i)+'.png')

def preprocess(i):
    img = io.imread('../pics/'+str(i)+'.png')
    grey_img = rgb2gray(img)
    io.imsave('../grey/'+str(i)+'.png',grey_img)
    #plt.imshow(grey_img,cmap=plt.cm.gray)
    #plt.show()

if __name__ == '__main__':
    for i in range(0,1050):
        #download(i)
        preprocess(i)
