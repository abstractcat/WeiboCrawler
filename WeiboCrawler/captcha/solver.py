__author__ = 'chi'

from skimage import io
from skimage.color import rgb2gray
import numpy as np
from scipy.misc import imresize
import matplotlib.pyplot as plt
from sklearn import linear_model
from sklearn.feature_extraction.image import img_to_graph
from sklearn.kernel_approximation import AdditiveChi2Sampler
from sklearn.preprocessing import PolynomialFeatures

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
        clf = linear_model.Ridge (alpha = .5)
        clf.fit(X, Y)
        # print(ols.coef_)
        f = open('split_coef.txt', 'w')
        f.write(str(clf.coef_))
        f.close()
        plt.plot(clf.coef_, 'b-', label="Ridge estimate")
        plt.show()
        return clf


def feature(img):
    (h, w) = img.shape
    x = [0 for i in range(h+w)]
    for m in range(h):
        for n in range(w):
            if img[m, n] < 255:
                x[m] += 1
                x[h + n] += 1
    return x

def split_combine(img,pos):
    img_left=map(lambda x:x[:pos],img)
    img_right=map(lambda x:x[pos:],img)
    img=np.concatenate((img_right,img_left), axis=1)
    return img

def load_split_train_data(start, end):
    X = []
    for i in range(start, end):
        img = io.imread('../grey/' + str(i) + '.png')
        #x = feature(img)
        x=np.reshape(img,img.size)
        X.append(x)
    poly = PolynomialFeatures(degree=2)
    X=poly.fit_transform(X)
    X=list(X)
    f = open('../scripts/split.txt')
    Y = f.readlines()[start:end]
    Y = map(lambda x: float(x.split('\t')[1]), Y)
    f.close()
    return (X, Y)


if __name__ == '__main__':
    (train_start, train_end) = (0, 1000)
    (X, Y) = load_split_train_data(train_start, train_end)
    (test_start, test_end) = (1000, 1050)
    (X_test, Y_test) = load_split_train_data(test_start, test_end)

    solver = CaptchaSolver()
    clf = solver.train_splitter(X, Y)


    #test
    poly = PolynomialFeatures(degree=2)
    for i in range(test_start, test_end):
        print(str(i) + '.png')
        img = io.imread('../grey/' + str(i) + '.png')
        #x_test = feature(img)
        x_test=np.reshape(img,img.size)
        x_test = poly.fit_transform(x_test)

        lines = []
        for j in range(0, 4):
            predict_y = int(round(clf.predict(x_test)))
            lines.append(predict_y)
            fig, ax = plt.subplots()
            ly=ax.axvline(color='k')
            ly.set_xdata(predict_y)
            plt.imshow(img,cmap=plt.cm.gray)
            plt.draw()
            plt.show()
            #split and combine img
            img=split_combine(img,predict_y)
            #x_test=feature(img)
            x_test=np.reshape(img,img.size)
            x_test = poly.fit_transform(x_test)
