from django.db import models


class ClassificationRequest(models.Model):
    """
    Stores a user request for face classification.
    """
    timestamp = models.DateTimeField(auto_now=True)

    type = models.PositiveIntegerField(help_text="0 for video, 1 for image,\
                                                 any other undefined")


class ImageClassification(models.Model):
    """
    Stores the information for a single image frame
    classification, related to :model:`emotion.ClassificationRequest`.

    The 48x48 pixel image is stored row-wise as a csv string.
    """
    request = models.ForeignKey('ClassificationRequest')

    # String of pixels comma separated (48 x 48) image
    image = models.TextField()

    # Rank 
    rank1 = models.PositiveIntegerField()
    rank1_prob = models.CharField(max_length=15)

    rank2 = models.PositiveIntegerField()
    rank2_prob = models.CharField(max_length=15)

    rank3 = models.PositiveIntegerField()
    rank3_prob = models.CharField(max_length=15)

    rank4 = models.PositiveIntegerField()
    rank4_prob = models.CharField(max_length=15)

    rank5 = models.PositiveIntegerField()
    rank5_prob = models.CharField(max_length=15)

    rank6 = models.PositiveIntegerField()
    rank6_prob = models.CharField(max_length=15)

    rank7 = models.PositiveIntegerField()
    rank7_prob = models.CharField(max_length=15)
