__author__ = 'chi'

from skimage import io
import matplotlib.pyplot as plt
from WeiboCrawler.captcha.solver import CaptchaSolver
from scipy.misc import imresize
import numpy as np

def split(i, coord, label):
    img = io.imread('../grey/' + str(i) + '.png',as_grey=True)
    img=np.array(img).astype(float)
    img/=255.0
    solver=CaptchaSolver()
    threshold=3
    img1 = solver.demargin(img[:, 0:coord[0]],threshold)
    img2 = solver.demargin(img[:, coord[0]:coord[1]],threshold)
    img3 = solver.demargin(img[:, coord[1]:coord[2]],threshold)
    img4 = solver.demargin(img[:, coord[2]:coord[3]],threshold)
    img5 = solver.demargin(img[:, coord[3]:],threshold)

    img1=imresize(img1,(25,20))
    img2=imresize(img2,(25,20))
    img3=imresize(img3,(25,20))
    img4=imresize(img4,(25,20))
    img5=imresize(img5,(25,20))

    io.imsave('../split/'+str(i)+'-1.png',img1)
    io.imsave('../split/'+str(i)+'-2.png',img2)
    io.imsave('../split/'+str(i)+'-3.png',img3)
    io.imsave('../split/'+str(i)+'-4.png',img4)
    io.imsave('../split/'+str(i)+'-5.png',img5)

'''
    fig = plt.subplot(2, 3, 1)
    fig.set_title(label[0])
    fig.imshow(img1, cmap=plt.cm.gray)
    fig = plt.subplot(2, 3, 2)
    fig.set_title(label[1])
    fig.imshow(img2, cmap=plt.cm.gray)
    fig = plt.subplot(2, 3, 3)
    fig.set_title(label[2])
    fig.imshow(img3, cmap=plt.cm.gray)
    fig = plt.subplot(2, 3, 4)
    fig.set_title(label[3])
    fig.imshow(img4, cmap=plt.cm.gray)
    fig = plt.subplot(2, 3, 5)
    fig.set_title(label[4])
    fig.imshow(img5, cmap=plt.cm.gray)
    plt.show()
'''


def main():
    # image splitting data
    f = open('split.txt')
    coords = f.readlines()
    coords = map(lambda x: x.strip().split('\t')[1:], coords)
    f.close()

    # pin label data
    f = open('pin.txt')
    labels = f.readlines()
    labels = map(lambda x: x.strip().split('\t')[1], labels)

    for i in range(0, 550):
        coord = coords[i]
        coord = map(lambda x: int(round(float(x))), coord)
        label = labels[i]
        #print(coord)
        #print(label)
        split(i, coord, label)


if __name__ == '__main__':
    main()
