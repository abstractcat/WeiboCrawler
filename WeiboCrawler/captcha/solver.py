__author__ = 'chi'

import matplotlib.pyplot as plt
from skimage import io
from skimage.color import rgb2gray
import numpy as np
from scipy.misc import imresize
class CaptchaSolver():
    def __init__(self,img):
        self.img=rgb2gray(img)

    def segment(self):
        (M,N)=self.img.shape
        vertical_count=[0 for i in range(N)]
        horizonal_count=[0 for i in range(M)]
        for j in range(N):
            for i in range(M):
                if self.img[i,j]<1:
                    vertical_count[j]+=1
                    horizonal_count[i]+=1
        left=0
        right=N-1
        while vertical_count[left]<10:
            left+=1
        while vertical_count[right]<10:
            right-=1
        bottom=0
        top=M-1
        while horizonal_count[bottom]<10:
            bottom+=1
        while horizonal_count[top]<10:
            top-=1

        #get the image without margin
        img=self.img[bottom:top]
        img=np.array(map(lambda x:x[left:right],img))
        img=imresize(img,(M,N))
        plt.imshow(img,cmap=plt.cm.gray)
        plt.show()



if __name__=='__main__':
    for i in range(0,100):
        filename='../pics/%s.png'%i
        img = io.imread(filename)
        solver=CaptchaSolver(img)
        solver.segment()