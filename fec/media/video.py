import cv
import cv2
from multiprocessing.pool import ThreadPool
import image_processing as imp
from collections import deque
from abc import ABCMeta, abstractmethod
from collections import deque


class VideoStreamClassifyBase(object):
    __metaclass__ = ABCMeta

    def __init__(self, classifier, frame_skip=20):
        self._classifier = classifier
        self._frame_skip = None
        self.frame_skip = frame_skip
        self._classifications = []

        self.thread_num = None
        self.thread_pool = None
        self._setup_multithreaded()
        self.tasks = deque()

    def get_classifications(self):
        return self._classifications

    def _setup_multithreaded(self):
        self.thread_num = cv2.getNumberOfCPUs()
        self.thread_pool = ThreadPool(self.thread_num)

    def process_frame(self, frame, frame_count):
        while len(self.tasks) > 0 and self.tasks[0].ready():
            self._classifications(self.tasks.popleft().get())

        if len(self.tasks) < self.thread_num and\
           frame_count % self.frame_skip == 0:
            task_func = self._classifier
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

            self.process_frame(frame, frame_count)

        self.clean_up()

    def stop(self):
        pass

    def clean_up(self):
        if self._capture:
            self._capture.release()

    def get_classifications(self):
        pass

VideoStreamClassifyBase.register(VideoFileClassifier)


if __name__ == '__main__':
    v = CameraClassifier(None)
    v.start()
