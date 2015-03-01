from abc import ABCMeta, abstractmethod
import numpy as np


class ClassifierBase(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def fit(self, X, y):
        pass

    @abstractmethod
    def predict(self, X):
        pass


class DummyClassifier(ClassifierBase):
    def __init__(self, n):
        self._n = n

    def fit(self, X, y):
        pass

    def predict(self, X):
        return np.random.randint(0, self._n, size=X.shape[0])
