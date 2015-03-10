from django.db import models
from django.core.exceptions import ValidationError
import os
import string
import random
from PIL import Image
from cStringIO import StringIO
from django.core.files.base import ContentFile
import cv2


def validate_request_type(value):
    """
    Validates that the request type is either 0 or 1
    """
    if value != 0 and value != 1:
        raise ValidationError('Invalid classification type: {0}'.format(value))


def create_rand_string(size=10, chars=string.ascii_letters + string.digits):
    return ''.join(random.SystemRandom().choice(chars) for _ in xrange(size))


class ClassificationRequest(models.Model):
    """
    Stores a user request for face classification.
    """
    timestamp = models.DateTimeField(auto_now=True)

    type = models.PositiveIntegerField(help_text="0 for video, 1 for image,\
                                                 any other undefined",
                                       validators=[validate_request_type])

    rand_string = models.CharField(max_length=10)


def gray_scale_file(instance, filename):
    rand_string = instance.request.rand_string
    image_rank = instance.image_rank
    return os.path.join(rand_string,
                        str(image_rank) + "-gray.png")


def original_image_file(instance, filename):
    rand_string = instance.request.rand_string
    image_rank = instance.image_rank
    return os.path.join(rand_string,
                        str(image_rank) + "-frame.png").encode('utf-8')


class ImageClassification(models.Model):
    """
    Stores the information for a single image frame
    classification, related to :model:`emotion.ClassificationRequest`.

    The 48x48 pixel image is stored row-wise as a csv string.
    """
    request = models.ForeignKey('ClassificationRequest')

    # Grayscale image used for classification
    gray_image = models.ImageField(upload_to=gray_scale_file)

    # Origianl Image
    image = models.ImageField(upload_to=original_image_file)

    image_rank = models.IntegerField()

    # Rank
    rank1 = models.PositiveIntegerField()
    rank1_prob = models.FloatField(default=0.0)

    rank2 = models.PositiveIntegerField()
    rank2_prob = models.FloatField(default=0.0)

    rank3 = models.PositiveIntegerField()
    rank3_prob = models.FloatField(default=0.0)


def _save_img_helper(img_field, image, format='jpeg'):
    f = StringIO()
    image.save(f, format)
    s = f.getvalue()
    img_field.save('', ContentFile(s), True)


def add_video_image_models(predictions, images, max_image=6):
    clf_request = ClassificationRequest(rand_string=create_rand_string(),
                                        type=0)
    clf_request.save()

    best_predictions = predictions.sort(sort_columns='score', ascending=False)
    image_dict = {}

    rank = 1
    count = 0
    for row in best_predictions:
        if count == max_image:
            break
        image_id = row['row_id']

        if image_id in image_dict:
            continue

        image_dict[image_id] = rank

        rank += 1
        count += 1

    image_classifiers = []
    for img, rank in image_dict.iteritems():
        sf = best_predictions.filter_by(img, column_name='row_id')

        classes = sf['class']
        prob = sf['score']
        ic = ImageClassification(
            request=clf_request,
            image_rank=rank,
            rank1=classes[0],
            rank2=classes[1],
            rank3=classes[2],
            rank1_prob=prob[0],
            rank2_prob=prob[1],
            rank3_prob=prob[2],
        )

        image_data = (images[0][img], images[1][img])
        image = Image.fromarray(cv2.cvtColor(image_data[0], cv2.COLOR_BGR2RGB))
        gray_image = Image.fromarray(image_data[1])

        _save_img_helper(ic.image, image)
        _save_img_helper(ic.gray_image, gray_image)

        ic.save()

        image_classifiers.append(ic)
    return clf_request, image_classifiers


def add_image_models(predictions, original, scaled):
    clf_request = ClassificationRequest(rand_string=create_rand_string(),
                                        type=1)
    clf_request.save()

    best_predictions = predictions.sort(sort_columns='score',
                                        ascending=False)
    classes = best_predictions['class']
    prob = best_predictions['score']
    ic = ImageClassification(
        request=clf_request,
        image_rank=1,
        rank1=classes[0],
        rank2=classes[1],
        rank3=classes[2],
        rank1_prob=prob[0],
        rank2_prob=prob[1],
        rank3_prob=prob[2],
    )

    _save_img_helper(ic.image, Image.fromarray(original.pixel_data))
    _save_img_helper(ic.gray_image,
                     Image.fromarray(scaled.pixel_data))

    ic.save()

    return clf_request, ic
