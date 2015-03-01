from abc import ABCMeta, abstractmethod
import numpy as np


class ClassifierBase(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def fit(self, x, y):
        pass

    @abstractmethod
    def predict(self, x):
        pass


class DummyClassifier(ClassifierBase):
    def __init__(self, n):
        self._n = n

    def fit(self, x, y):
        pass

    def predict(self, x):
        return np.random.randint(0, self._n, size=x.shape[0])
