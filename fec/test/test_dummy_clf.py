import unittest
from fec.classifier.classifier_base import DummyClassifier
import numpy as np


class DummyClassifierTest(unittest.TestCase):
    def test_dummy_classifier(self):
        n = 10
        dummy = DummyClassifier(n)

        size = (100, 4)
        x = np.random.random(size)
        predict = dummy.predict(x)
        self.assertEqual(predict.shape[0], size[0])
        self.assertTrue(np.all(predict < n))
        self.assertTrue(np.all(predict >= 0))
