from classifier_base import ClassifierBase
import os
import graphlab as gl
import numpy as np


class GraphLabClassifierFromFile(ClassifierBase):
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


class GraphLabClassifierFromNetBuilder(ClassifierBase):
    def __init__(self, net_builder, h=48, w=48, depth=1,
                 target='label', feat_name='images',
                 max_iterations=50, verbose=True, chkpt_dir=''):
        self._net_builder = net_builder
        self._model = None

        self._feat_means = None
        self._feat_std = None

        self._h = h
        self._w = w
        self._d = depth

        self._target = target
        self._feat_name = feat_name

        # Fit parameters
        self._max_iterations = max_iterations,
        self._verbose = verbose
        self._chkpt_dir = chkpt_dir

    def _create_images(self, x):
        sarray = gl.SArray(x)
        images = sarray.pixel_array_to_image(self._w, self._h, self._d,
                                             allow_rounding=True)
        return images

    def _scale_features(self, x):

        row_means = np.mean(x, axis=1)
        x -= row_means[:, np.newaxis]

        x -= self._feat_means
        x /= self._feat_std

        # Scale back to [0, 255]
        x_min = np.min(x)
        x_max = np.max(x)

        return 255 * (x - x_min) / (x_max - x_min)

    def _assemble_full_dataset(self, x, y):
        images = self._create_images(x)
        sf = gl.SFrame({self._feat_name: images,
                        self._target: y})
        return sf

    def fit(self, x, y, **kwargs):

        self._feat_means = np.mean(x, axis=0)
        self._feat_std = np.std(x, axis=0)

        x = self._scale_features(x)
        dataset = self._assemble_full_dataset(x, y)

        # Time to train the model
        self._model = gl.neuralnet_classifier.create(
            dataset,
            target=self._target,
            max_iterations=self._max_iterations,
            model_checkpoint_path=self._chkpt_dir,
            verbose=self._verbose,
            **kwargs
        )

        return

    def predict(self, x):
        return self._model.predict(x)

    def predict_proba(self, x, k=3):
        return self._model.predict_topk(x, k=k)
