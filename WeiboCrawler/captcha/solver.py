__author__ = 'chi'

from PIL import Image
import numpy as np
import scipy as sp
import matplotlib.pyplot as plt

class CaptchaSolver():
    def __init__(self,img):
        self.img=img
        
def main():
    f=open('../pics/130.png','rb')
    img=Image.open(f)
    CaptchaSolver(img)

if __name__ == '__main__':
    main()