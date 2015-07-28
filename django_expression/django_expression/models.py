from django.db import models
from django.core.exceptions import ValidationError
import os
import string
import random
from PIL import Image
from cStringIO import StringIO
from django.core.files.base import ContentFile


emotion_dictionary = {3: 'happy',
                      4: 'sad',
                      5: 'surprised'}


def validate_request_type(value):
    """
    Validates that the request type is either 0 or 1
    """
    if value != 0 and value != 1:
        raise ValidationError('Invalid classification type: {0}'.format(value))


def create_rand_string(size=10, chars=string.ascii_letters + string.digits):
    """Create a random string

    :param size: length of random string
    :param chars: character set to chosse from
    :return: random string
    """
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


def gray_scale_file(instance, suffix="-gray.png"):
    """Grayscale image upload_to callback

    :param instance: ImageField instance
    :param suffix: file path suffix
    :return: path to upload image to
    """
    rand_string = instance.request.rand_string
    image_rank = instance.image_rank
    return os.path.join(rand_string,
                        str(image_rank) + suffix)


def original_image_file(instance, suffix="-frame.png"):
    """Image upload_to callback

    :param instance: ImageField instance
    :param suffix: file path suffix
    :return: path to upload image to
    """
    rand_string = instance.request.rand_string
    image_rank = instance.image_rank
    return os.path.join(rand_string,
                        str(image_rank) + suffix).encode('utf-8')


class ImageClassification(models.Model):
    """
    Stores the information for a single image frame
    classification, related to :model:`django_expression.ClassificationRequest`.

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


def _image_emotion_score(image_clf):
    global emotion_dictionary
    out_dict = {}
    out_dict[emotion_dictionary[image_clf.rank1]] = image_clf.rank1_prob
    out_dict[emotion_dictionary[image_clf.rank2]] = image_clf.rank2_prob
    out_dict[emotion_dictionary[image_clf.rank3]] = image_clf.rank3_prob
    return out_dict


def add_image_models(predictions, original, scaled):
    """Add ImageClassification model to database

    :param predictions: SFrame predictions from GraphLab classifier
    :param original: array - image
    :param scaled: GraphLab image
    :return: tuple ClassificationRequest, url to image, and prediction probs
    """
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
        rank1_prob=100 * prob[0],
        rank2_prob=100 * prob[1],
        rank3_prob=100 * prob[2],
    )

    _save_img_helper(ic.image, Image.fromarray(original))
    _save_img_helper(ic.gray_image,
                     Image.fromarray(scaled.pixel_data))

    ic.save()
    scores = _image_emotion_score(ic)
    return clf_request, ic.image.url, scores
