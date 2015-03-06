from fec.classifier.gl_classifier import GraphLabClassifier
from fec.media.video import VideoFileClassifier
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


def run_video_classifier(video_path, frame_skip=5):
    model = get_classifier()

    video = VideoFileClassifier(model.predict_proba, video_path,
                                frame_skip=frame_skip)
    video.start()
    video.stop()

    images = video.get_final_images()
    classifications = video.get_classifications()

    return classifications, images


if __name__ == '__main__':
    print run_video_classifier('/Users/chris/face-emotion-classifier'
                               '/tmp_video/vid.mov')
