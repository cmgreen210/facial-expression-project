from fec.classifier.gl_classifier import GraphLabClassifierFromFile
from fec.media.image import ImageFileClassifier
from fec.media.image_processing import FaceDetectorProcessor
import os


_model = None
_model_path = 'model'

_image_clf = None


def get_classifier():
    global _model

    if _model is None:
        this_dir, _ = os.path.split(os.path.abspath(__file__))
        p = os.path.join(this_dir, 'classifier')
        _model = GraphLabClassifierFromFile(p)

    return _model


def get_image_classifier():
    global _image_clf

    if _image_clf is None:
        clf = get_classifier()
        face_processor = FaceDetectorProcessor(rect_color=(49, 176, 213))
        _image_clf = ImageFileClassifier(clf.predict_proba, face_processor)

    return _image_clf


def run_image_classifier(image_path):

    image_classifier = get_image_classifier()

    out = image_classifier.classify(image_path)
    return out


if __name__ == '__main__':
    pass