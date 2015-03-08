from fec.classifier.gl_classifier import GraphLabClassifierFromFile
from fec.media.video import VideoFileClassifier
from fec.media.image import ImageFileClassifier
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
        _image_clf = ImageFileClassifier(clf.predict_proba)

    return _image_clf


def run_video_classifier(video_path, frame_skip=5):
    """

    :param video_path:
    :param frame_skip:
    :return: sframe with cols: (row_id, class, score)
    """
    model = get_classifier()

    video = VideoFileClassifier(model.predict_proba, video_path,
                                frame_skip=frame_skip)
    video.start()
    video.stop()

    images = video.get_final_images()
    classifications = video.get_classifications()

    return classifications, images


def run_image_classifier(image_path):

    image_classifier = get_image_classifier()

    out = image_classifier.classify(image_path)
    return out


if __name__ == '__main__':
    path = '/Users/chris/face-emotion-classifier/'
    path += 'tmp_video/vid.mov'
    c, i = run_video_classifier(path)
