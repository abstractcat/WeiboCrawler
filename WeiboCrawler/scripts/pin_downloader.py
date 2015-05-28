#!/usr/bin/env python
#coding=utf8

import os
import sys
import urllib
import urllib2
import cookielib
import base64
import re
import hashlib
import json
import rsa
import binascii
import time
import random
import cStringIO
import numpy
import matplotlib.pyplot as plt
from PIL import Image

if __name__ == '__main__':
    for i in range(1000):
        url="http://login.sina.com.cn/cgi/pin.php?s=02271679&p=xd-e174b0d9f37780767be2f700faf79bfac60d"
        #download the pin image
        file = cStringIO.StringIO(urllib2.urlopen(url).read())
        img = Image.open(file)
        img.save('../pics/'+str(i)+'.png')