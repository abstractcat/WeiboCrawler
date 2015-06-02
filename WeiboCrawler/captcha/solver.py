__author__ = 'chi'

from skimage import io
from skimage.color import rgb2gray
import numpy as np
from scipy.misc import imresize
from sknn.mlp import Classifier, Convolution, Layer


class CaptchaSolver():
    def demargin(self, img, threshold):
        (M, N) = img.shape
        vertical_count = [0 for i in range(N)]
        horizonal_count = [0 for i in range(M)]
        for j in range(N):
            for i in range(M):
                if img[i, j] < 1.0:
                    vertical_count[j] += 1
                    horizonal_count[i] += 1
        # print(vertical_count)
        # print(horizonal_count)

        left = 0
        right = N - 1
        while vertical_count[left] < threshold:
            left += 1
        while vertical_count[right] < threshold:
            right -= 1
        bottom = 0
        top = M - 1
        while horizonal_count[bottom] < threshold:
            bottom += 1
        while horizonal_count[top] < threshold:
            top -= 1

        # get the image without margin
        img = img[bottom:top]
        img = np.array(map(lambda x: x[left:right], img))
        return img

    def preprocess(self, img):
        img = rgb2gray(img)
        img = self.demargin(img, 10)
        img = imresize(img, (26, 78))
        return img

    def neuralnetwork(self, X_train, y_train, X_test, y_test):
        nn = Classifier(
            layers=[
                Layer("Maxout", units=800, pieces=10),
                Layer("Softmax")],
            learning_rate=0.00005,
            n_iter=500)
        nn.fit(X_train, y_train)
        score = nn.score(X_test, y_test)
        print(score)

    def load_label(self, fname, start, end):
        f = open(fname)
        labels = f.readlines()
        labels = labels[start:end]
        labels = map(lambda x: x.strip().split('\t')[1], labels)

        letters = set()
        for label in labels:
            for letter in label:
                letters.add(letter)
        letters = list(letters)
        letters.sort()
        letter_dic = dict()
        for i in range(len(letters)):
            letter_dic[letters[i]] = i

        def label2index(ls, ldic):
            idx = []
            for l in ls:
                idx.append(ldic[l])
            return idx

        labels = np.array(map(lambda x: label2index(x, letter_dic), labels))
        labels = np.reshape(labels, labels.size)

        # print(labels)
        # print(letter_dic)
        return (labels, letter_dic)

    def load_X(self, dirname, start, end):
        X = []
        for i in range(start, end):
            for j in range(1, 6):
                img = io.imread(dirname + str(i) + '-' + str(j) + '.png')
                X.append(img)
        X = np.array(X)
        return X


if __name__ == '__main__':
    solver = CaptchaSolver()
    start = 0
    end = 550
    (labels, letter_dic) = solver.load_label('../scripts/pin.txt', start, end)
    X = solver.load_X('../split/', start, end)

    print(X.shape)
    print(labels.shape)

    X_train = X[:2500]
    y_train = labels[:2500]
    X_test = X[2500:]
    y_test = labels[2500:]
    solver.neuralnetwork(X_train, y_train, X_test, y_test)
