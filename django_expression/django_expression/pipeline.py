from fec.classifier.gl_classifier import GraphLabClassifierFromFile
from fec.media.image import ImageFileClassifier
from fec.media.image_processing import FaceDetectorProcessor
import os


_model = None
_model_path = 'classifier'

_image_clf = None


def get_classifier():
    """Get the GraphLabClassifierFromFile object at '/classifier/'

    :return: GraphLabClassifierFromFile object
    """
    global _model

    if _model is None:
        this_dir, _ = os.path.split(os.path.abspath(__file__))
        p = os.path.join(this_dir, _model_path)
        _model = GraphLabClassifierFromFile(p)

    return _model


def get_image_classifier():
    """Get ImageFileClassifier object

    :return: object
    """
    global _image_clf

    if _image_clf is None:
        clf = get_classifier()
        face_processor = FaceDetectorProcessor(rect_color=(49, 176, 213))
        _image_clf = ImageFileClassifier(clf.predict_proba, face_processor)

    return _image_clf


def run_image_classifier(image_path):
    """Classify image saved at input path

    :param image_path: path to image
    :return: tuple image classifier output
    """
    image_classifier = get_image_classifier()

    out = image_classifier.classify(image_path)
    return out
