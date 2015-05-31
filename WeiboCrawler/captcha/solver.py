__author__ = 'chi'

from skimage import io
from skimage.color import rgb2gray
import numpy as np
from scipy.misc import imresize
from sklearn.linear_model import ARDRegression, LinearRegression


class CaptchaSolver():
    def preprocess(self, img):
        img = rgb2gray(img)
        (M, N) = img.shape
        vertical_count = [0 for i in range(N)]
        horizonal_count = [0 for i in range(M)]
        for j in range(N):
            for i in range(M):
                if img[i, j] < 1:
                    vertical_count[j] += 1
                    horizonal_count[i] += 1
        left = 0
        right = N - 1
        while vertical_count[left] < 10:
            left += 1
        while vertical_count[right] < 10:
            right -= 1
        bottom = 0
        top = M - 1
        while horizonal_count[bottom] < 10:
            bottom += 1
        while horizonal_count[top] < 10:
            top -= 1

        # get the image without margin
        img = img[bottom:top]
        img = np.array(map(lambda x: x[left:right], img))
        img = imresize(img, (26, 78))
        return img

    def train_splitter(self, X, Y):
        clf = ARDRegression(compute_score=True)
        clf.fit(X, Y)
        print(clf.coef_)
        f = open('split_coef.txt', 'w')
        f.write(clf.coef_)
        f.close()

def load_split_train_data(n):
    X = []
    for i in range(n):
        img = io.imread('../grey/' + str(i) + '.png')
        (h, w) = img.shape
        w = 30
        img = map(lambda x: x[:w], img)
        x = list(np.reshape(img, w * h))
        X.append(x)

    f = open('../scripts/split.txt')
    Y = f.readlines()[:n]
    Y = map(lambda x: float(x.split('\t')[1]), Y)
    f.close()
    return (X, Y)


if __name__ == '__main__':
    (X, Y) = load_split_train_data(5)
    solver = CaptchaSolver()
    solver.train_splitter(X, Y)
