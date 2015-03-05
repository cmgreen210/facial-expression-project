from fec.classifier.gl_classifier import GraphLabClassifier
import os


_model = None
_model_path = 'model'


def get_classifier():
    global _model

    if _model is None:
        this_dir, _ = os.path.split(os.path.abspath(__file__))
        p = os.path.join(this_dir, 'classifier')
        _model = GraphLabClassifier(p)

    return _model
