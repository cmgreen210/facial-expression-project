import cv
import cv2
from multiprocessing.pool import ThreadPool
import image_processing as imp
from collections import deque
from abc import ABCMeta, abstractmethod
from collections import deque
from fec.media.image_processing import FaceDetectorProcessor
import os
import graphlab as gl
import shutil


class VideoStreamClassifyBase(object):
    __metaclass__ = ABCMeta

    def __init__(self, classifier, frame_skip=20,
                 image_processor=FaceDetectorProcessor()):
        self._classifier = classifier
        self._frame_skip = None
        self.frame_skip = frame_skip
        self._classifications = []
        self.images = []
        self.thread_num = None
        self.thread_pool = None
        self._setup_multithreaded()
        self.tasks = deque()
        self.image_processor = image_processor

        self.original_images = None
        self.transformed_image = None

    def get_classifications(self):
        return self._classifications

    def _setup_multithreaded(self):
        self.thread_num = cv2.getNumberOfCPUs()
        self.thread_pool = ThreadPool(self.thread_num)

    def process_frame(self, frame, frame_count):
        while len(self.tasks) > 0 and self.tasks[0].ready():
            self.images.append(self.tasks.popleft().get())

        if len(self.tasks) < self.thread_num and\
           frame_count % self.frame_skip == 0:
            task_func = self.image_processor.process_image
            task = self.thread_pool.apply_async(task_func,
                                                (frame.copy(),))
            self.tasks.append(task)

    @property
    def classifier(self):
        return self._classifier

    @classifier.setter
    def classifier(self, classifier):
        self._classifier = classifier

    @property
    def frame_skip(self):
        return self._frame_skip

    @frame_skip.setter
    def frame_skip(self, frame_skip):
        if frame_skip <= 0:
            raise ValueError('Frame skip most be positive!')

        self._frame_skip = frame_skip

    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def stop(self):
        pass

    @abstractmethod
    def clean_up(self):
        pass


class CameraClassifier(VideoStreamClassifyBase):
    def __init__(self, classifier, frame_skip=20, source=0, name=""):
        super(CameraClassifier, self).__init__(classifier, frame_skip)
        self._source = source
        self._capture = None
        self._name = name

    def start(self):

        self._capture = cv2.VideoCapture(self._source)
        frame_count = 0
        while self._capture.isOpened():
            ret, frame = self._capture.read()
            frame_count += 1

            if self.stop():
                break

            self._display_image(frame)

            self.process_frame(frame, frame_count)

        self.clean_up()

    def stop(self):
        return cv2.waitKey(1) & 0xFF == ord('q')

    def clean_up(self):
        if self._capture:
            self._capture.release()

        cv.DestroyAllWindows()

    def get_classifications(self):
        pass

    def _display_image(self, image):
        cv2.imshow(self._name, image)
        return


VideoStreamClassifyBase.register(CameraClassifier)


class VideoFileClassifier(VideoStreamClassifyBase):
    def __init__(self, classifier, source, frame_skip=20, name=""):
        super(VideoFileClassifier, self).__init__(classifier, frame_skip)
        self._source = source
        self._capture = None
        self._name = name

        this_dir, _ = os.path.split(os.path.abspath(__file__))
        self.tmp_dir = os.path.join(this_dir, 'tmp')
        if os.path.exists(self.tmp_dir):
            shutil.rmtree(self.tmp_dir)
        os.mkdir(self.tmp_dir)
        os.mkdir(os.path.join(self.tmp_dir,
                              'class'))
        os.mkdir(os.path.join(self.tmp_dir,
                              'orig'))

    def start(self):

        self._capture = cv2.VideoCapture(self._source)
        frame_count = 0
        while self._capture.isOpened():
            ret, frame = self._capture.read()
            frame_count += 1

            if not ret:
                break
            self.process_frame(frame, frame_count)

        self.clean_up()

    def stop(self):
        pass

    def clean_up(self):
        if self._capture:
            self._capture.release()

        if self.images is not None:
            count = 0
            for im in self.images:
                original_im = im[0]
                orig_dir = os.path.join(self.tmp_dir, 'orig')
                file_name = os.path.join(orig_dir,
                                         'orig_' + str(count) + '.png')
                cv2.imwrite(file_name, original_im)

                class_im = im[1]
                class_dir = os.path.join(self.tmp_dir, 'class')
                file_name = os.path.join(class_dir,
                                         'class_' + str(count) + '.png')
                cv2.imwrite(file_name, class_im)
                count += 1

            x = gl.image_analysis.load_images(class_dir)
            x.rename({'image': 'images'})
            if self.classifier is not None:
                self._classifications = self.classifier(x)

            self.original_images = gl.image_analysis.load_images(orig_dir)
            self.original_images.rename({'image': 'images'})
            self.transformed_image = x

    def get_classifications(self):
        return self._classifications

VideoStreamClassifyBase.register(VideoFileClassifier)


if __name__ == '__main__':
    v = VideoFileClassifier(None, '/Users/chris/face-emotion-classifier'
                                  '/tmp_video/vid.mov')
    v.start()
    v.stop()
