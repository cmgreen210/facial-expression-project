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
        self._n = None

    def fit(self, x, y):
        self._n = x.shape[1]

    def predict(self, x):
        if self._n is None:
            raise StandardError('You must call fit before predict!')
        return np.random.randint(0, self._n, size=x.shape[0])

ClassifierBase.register(DummyClassifier)
