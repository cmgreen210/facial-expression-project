from classifier_base import ClassifierBase
import os
import graphlab as gl


class GraphLabClassifier(ClassifierBase):
    def __init__(self, model_path):
        if not os.path.exists(model_path):
            raise ValueError("Model path does not exist!")

        self._model = gl.load_model(model_path)
        self._num_class = self._model['num_classes']

    def fit(self, x, y):
        pass

    def predict(self, x):
        return self._model.predict(x)

    def predict_proba(self, x):
        return self._model.predict_topk(x, k=self._num_class)
