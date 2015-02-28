from django.db import models
from django.core.exceptions import ValidationError


def validate_request_type(value):
    """
    Validates that the request type is either 0 or 1
    """
    if value != 0 and value != 1:
        raise ValidationError('Invalid classification type: {0}'.format(value))


class ClassificationRequest(models.Model):
    """
    Stores a user request for face classification.
    """
    timestamp = models.DateTimeField(auto_now=True)

    type = models.PositiveIntegerField(help_text="0 for video, 1 for image,\
                                                 any other undefined",
                                       validators=[validate_request_type])


def validate_image_csv(value, height=48, width=48, separator=','):
    """Validates that the image values are stored correctly"""
    n = height * width
    l = value.split(separator)
    if len(l) != n:
        raise ValidationError('Image csv is not of right size!')


class ImageClassification(models.Model):
    """
    Stores the information for a single image frame
    classification, related to :model:`emotion.ClassificationRequest`.

    The 48x48 pixel image is stored row-wise as a csv string.
    """
    request = models.ForeignKey('ClassificationRequest')

    # String of pixels comma separated (48 x 48) image
    image = models.TextField(validators=[validate_image_csv])

    # Rank
    rank1 = models.PositiveIntegerField()
    rank1_prob = models.FloatField(default=0.0)

    rank2 = models.PositiveIntegerField()
    rank2_prob = models.FloatField(default=0.0)

    rank3 = models.PositiveIntegerField()
    rank3_prob = models.FloatField(default=0.0)

    rank4 = models.PositiveIntegerField()
    rank4_prob = models.FloatField(default=0.0)

    rank5 = models.PositiveIntegerField()
    rank5_prob = models.FloatField(default=0.0)

    rank6 = models.PositiveIntegerField()
    rank6_prob = models.FloatField(default=0.0)

    rank7 = models.PositiveIntegerField()
    rank7_prob = models.FloatField(default=0.0)
