__author__ = 'chi'

from skimage import io
import numpy as np
from sknn.mlp import Classifier, Convolution, Layer


class CaptchaSolver():
    def neuralnetwork(self, X_train, y_train, X_test, y_test):
        nn = Classifier(
            layers=[Layer("Sigmoid", units=500), Layer("Linear")],
            learning_rate=0.0001,
            n_iter=500
        )
        nn.fit(X_train, y_train)
        p_predict= nn.predict_proba(X_test)
        y_predict=nn.predict(X_test)
        for i in range(0,len(y_test)):
            if y_test[i]==1:
                print(y_test[i],y_predict[i],p_predict[i])

    def load_y(self, character):
        f = open('label.txt')
        labels = f.readlines()
        labels = map(lambda x: x.strip().split('\t')[1], labels)
        y = map(lambda x: int(character in x), labels)
        y = np.array(y)

        print(labels)
        print(y)

        return y

    def load_X(self):
        X = []
        for i in range(0, 1050):
            img = io.imread('../grey/' + str(i) + '.png')
            X.append(img)
        X = np.array(X)
        return X


if __name__ == '__main__':
    solver = CaptchaSolver()

    X = solver.load_X()
    y = solver.load_y('A')

    # 500 for training
    X_train = X[:500]
    y_train = y[:500]

    # 550 for test
    X_test = X[550:]
    y_test = y[550:]

    print(float(sum(y_test))/float(len(y_test)))
    solver.neuralnetwork(X_train, y_train, X_test, y_test)
