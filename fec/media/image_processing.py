import cv2
import numpy as np
import time
import os
from fec.classifier import face_detector


class ImageProcessor(object):
    def __init__(self):
        pass

    def process_image(self, image, *args):
        #  self.save_image(image)
        return image

    def save_image(self, image):
        file_name = os.path.dirname(__file__)
        dir_name = os.path.join(file_name, 'tmp')
        if not os.path.exists(dir_name):
            os.mkdir(dir_name)
        file_name = os.path.join(dir_name,
                                 'test_' + str(int(100000 *
                                                   time.time())) + '.png')
        cv2.imwrite(file_name, image)


class GrayScaleProcessor(ImageProcessor):
    def __init__(self):
        pass

    def process_image(self, image, *args):

        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        return gray


class ResizeProcessor(ImageProcessor):
    def __init__(self, dim=(48, 48), interp=cv2.INTER_AREA):
        self.dim = dim
        self.interp = interp

    def process_image(self, image, *args):
        dst = cv2.resize(image, self.dim,
                         interpolation=self.interp)
        return dst


class FaceDetectorProcessor(ImageProcessor):

    def __init__(self, cascade_file='haarcascade_frontalface_alt.xml',
                 return_largest=True, scale_x=1.1, scale_y=1.1):
        self.detector = FaceDetector(cascade_file,
                                     return_largest=return_largest)

        self.preprocessor = GrayScaleProcessor()
        self.postprocessor = ResizeProcessor()
        self.scale_x = scale_x
        self.scale_y = scale_y

    def process_image(self, image, *args):
        gray = self.preprocessor.process_image(image, *args)

        face = self.detector.detect_face(image)
        if len(face) == 0:
            return image
        x, y, w, h = face[0]
        w *= self.scale_x
        h *= self.scale_y

        gray = gray[y:y+h, x:x+w]
        gray = self.postprocessor.process_image(gray)
        self.save_image(gray)
        return image


def run_face_detector(image):
    detector = FaceDetectorProcessor()
    detector.process_image(image)
