import cv
import cv2
from multiprocessing.pool import ThreadPool
import image_processing as imp
from collections import deque


class VideoStream(object):

    def __init__(self, video_source=0, frame_skip=20):
        self.video_source = video_source
        self.capture = None
        self.frame_skip = frame_skip

        self.clf_proc = None

        self.threadn = None
        self.thread_pool = None
        self._setup_multithreaded()

        self.image_processor = imp.ImageProcessor()
        self.tasks = None

    def start(self):

        self.capture = cv2.VideoCapture(self.video_source)

        frame_count = 0
        self.tasks = deque()
        while self.capture.isOpened():

            ret, frame = self.capture.read()
            frame_count += 1
            cv2.imshow('video', frame)

            while len(self.tasks) > 0 and self.tasks[0].ready():
                proc_imag = self.tasks.popleft().get()
                #  cv2.imshow('video', proc_imag)

            if len(self.tasks) < self.threadn and\
               frame_count % self.frame_skip == 0:
                task_func = self.image_processor.process_image
                task = self.thread_pool.apply_async(task_func,
                                                    (frame.copy(),))
                self.tasks.append(task)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        self.clean_up()

    def _display_image(self, name, image):
        cv2.imshow(name, image)
        return

    def clean_up(self):
        if self.capture:
            self.capture.release()

        cv.DestroyAllWindows()

    def _setup_multithreaded(self):
        self.threadn = cv2.getNumberOfCPUs()
        self.thread_pool = ThreadPool(self.threadn)

if __name__ == '__main__':
    v = VideoStream(frame_skip=15)
    v.image_processor = imp.FaceDetectorProcessor()
    v.start()
